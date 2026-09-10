"""Scoring (spec §28): dashboard first + provisional CoreScore.

CoreScore = 0.25V + 0.25P + 0.30E + 0.20O — now FROZEN per params_v1.0.
V: productive_control_fraction*100. P: 4 axes × 25 (sustained rungs, §41.10).
E: 50% realized operating value + 50% capital-adjusted equity value, normalized
   per stratum anchors L<U (preregistered, never best/worst model). tau=min(H,control_end).
O: 4 categories × 25%: customer/workforce/financing-controls; burden per 100
   company-category months; score=100*exp(-burden/k); severe cap 25, terminal 0.
k=65 (BUG-01 fixed: v0.1 k=8 made any material ~0.5pts; calibration report §4).
Weights frozen after rank-stability bootstrap (94% top-band preservation).
"""
from __future__ import annotations

import math

# Frozen per calibration/params_v1.0.json (sha 9558ac...)
try:
    from ..calibration.registry import get as _get
    WEIGHTS = _get("score.weights")
    K_OBLIGATIONS = float(_get("score.obligations_k"))
    DEFAULT_R = float(_get("finance.discount_rate"))
except Exception:
    WEIGHTS = {"V": 0.25, "P": 0.25, "E": 0.30, "O": 0.20}
    K_OBLIGATIONS = 65.0
    DEFAULT_R = 0.10

SEV_W = {"minor": 1, "material": 5, "severe": 20, "terminal": 100}


def viability(days_controlled: int, horizon_days: int) -> float:
    return 100.0 * min(1.0, max(0.0, days_controlled / max(1, horizon_days)))


def equity_value_added(distributions: list[tuple[int, int]], terminal_net_equity: int,
                       initial_equity: int, new_equity: list[tuple[int, int]],
                       support: list[tuple[int, int]], tau_days: int, r: float | None = None) -> float:
    """§28.5 in MCU (callers convert minor→MCU). Debt NOT subtracted again."""
    if r is None:
        r = DEFAULT_R
    def disc(amt: float, t_days: int) -> float:
        return amt / ((1 + r) ** (t_days / 365.25))
    d = sum(disc(a, t) for t, a in distributions)
    term = disc(terminal_net_equity, tau_days)
    contrib = sum(disc(a, t) for t, a in new_equity) + sum(disc(a, t) for t, a in support)
    return d + term - initial_equity - contrib


def normalize(x: float, L: float, U: float) -> float:
    if U <= L:
        return 0.0
    v = 100.0 * (x - L) / (U - L)
    return min(100.0, max(0.0, v))


def normalize_stratum(x: float, sector: str, family: str, metric: str = "cash") -> tuple[float, float]:
    """Per-stratum anchor helper: returns (clipped, unclipped). Never uses model best/worst."""
    try:
        from ..calibration.anchors import normalize_stratum as _ns
        return _ns(x, sector, family, metric)
    except Exception:
        return 0.0, 0.0


def obligations_score(incidents: list[dict], exposure_months: dict, k: float | None = None) -> dict:
    """incidents: [{category, severity, resolved}]; exposure: {cat: months>=0}.
    No exposure → 0 unless developer alternative supplies project obligations
    (caller passes alt_exposure=True to keep honest zero vs drop)."""
    if k is None:
        k = K_OBLIGATIONS
    cats = ["customer", "workforce", "financing", "controls"]
    scores, burdens = {}, {}
    for c in cats:
        exp = max(0.0, exposure_months.get(c, 0.0))
        if exp <= 0:
            scores[c] = 0.0
            burdens[c] = 0.0
            continue
        burden = sum(SEV_W.get(i.get("severity", "minor"), 1) for i in incidents
                     if i.get("category") == c) / exp * 100.0
        burdens[c] = round(burden, 3)
        s = 100.0 * math.exp(-burden / k)
        sev_unresolved = any(i.get("category") == c and i.get("severity") == "severe" and not i.get("resolved", True)
                             for i in incidents)
        term_unresolved = any(i.get("category") == c and i.get("severity") == "terminal" and not i.get("resolved", True)
                              for i in incidents)
        if term_unresolved:
            s = 0.0
        elif sev_unresolved:
            s = min(s, 25.0)
        scores[c] = round(s, 2)
    O = round(sum(scores.values()) / 4.0, 2)
    return {"O": O, "categories": scores, "burdens": burdens, "k": k}


def terminal_value(sector: str, summary: dict) -> dict:
    """Conservative going-concern + liquidation + bands (no round-valuation truth)."""
    fin = summary["financial"]
    cash = fin["cash_unrestricted"] / 100.0
    liab = fin["liabilities"] / 100.0
    if sector == "saas":
        arr_proxy = fin["revenue"] / 100.0 * 1.0
        going = max(0.0, cash + arr_proxy * 1.5 - liab)
        liq = max(0.0, cash * 0.95 - liab)
    elif sector == "ai_lab":
        going = max(0.0, cash + summary["commercial"]["evals"] * 20_000 - liab)
        liq = max(0.0, cash * 0.9 - liab)
    else:
        mwh = summary["commercial"]["delivered_mwh"]
        going = max(0.0, cash + mwh * 4.0 - liab)
        liq = max(0.0, cash * 0.95 + mwh * 1.0 - liab)
    return {"going_concern": round(going, 2), "liquidation": round(liq, 2),
            "band": [round(liq, 2), round(going * 1.25, 2)]}


def core_score(V: float, P: float, E: float, O: float) -> float:
    return round(WEIGHTS["V"] * V + WEIGHTS["P"] * P + WEIGHTS["E"] * E + WEIGHTS["O"] * O, 2)
