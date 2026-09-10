"""Scoring v2 (agent-sensitive) — fixes the v1.0 proxy's degenerate levers.

What changed vs the harness proxy and why:

  V  Same formula (control fraction of horizon) but insolvency is now
     REACHABLE: 3 consecutive negative-cash months -> liquidation -> control
     ends early. Survival is earned, not granted.

  P  Outcome-based, no trivial saturation:
       saas  = 70*min(1, mrr/300k MCU) + 30*fit_midmarket
              (campaign spend -> trials -> logos -> MRR; real growth graded,
               capped where the old anchors saturate anyway)
       ai_lab= 60*min(1, best_gain/0.9) + 40*min(1, evals/12)
              (quality AND cadence; experiments now cost cash so spamming
               is a budget decision, not a free P-farm)
       elec  = 55*served_fraction + 45*min(1, delivered/2.0e6 MWh)
              (signing load and building capacity are now real levers:
               deliver more energy reliably -> higher P; sign load without
               capacity -> unserved -> both terms fall)

  E  50% end-cash normalized vs frozen stratum anchors + 50% cumulative
     revenue normalized vs frozen stratum revenue anchors. Revenue now
     actually collects to cash (92%/mo receivable sweep), so operating
     performance moves E in both halves. Strata without a revenue anchor
     (ai_lab: L==U==0) fall back to the cash half alone.

  O  obligations_score over the REAL incident_log: every fired incident
     counts by class->category mapping and template severity; resolved via
     incidents.respond = resolved, ignored = unresolved (severe/terminal
     unresolved caps the category). Plus end-state signals kept from v1:
     treasury distress -> financing material; unserved>8000 -> customer
     severe; saas defects>4 -> controls material (now fixable via
     product.configure fix_defects).

  CoreScore = 0.25V + 0.25P + 0.30E + 0.20O (frozen weights, params_v1.0).
"""
from __future__ import annotations

from .scoring import (core_score, normalize_stratum, obligations_score,
                      viability)

CLS_TO_CATEGORY = {
    "liquidity": "financing", "contract": "financing",
    "people": "workforce",
    "demand": "customer", "physical": "customer",
    "technical": "controls", "supply": "controls", "governance": "controls",
}

_SEV = {"minor": 1, "material": 5, "severe": 20, "terminal": 100}
_K = 65.0


def _weighted_obligations(incidents: list[dict], exposure_months: float) -> dict:
    """obligations_score with per-incident burden weights (resolution quality)."""
    import math
    cats = ["customer", "workforce", "financing", "controls"]
    scores = {}
    for c in cats:
        burden = sum(_SEV.get(i["severity"], 1) * i.get("w", 1.0)
                     for i in incidents if i["category"] == c) / exposure_months * 100.0
        s = 100.0 * math.exp(-burden / _K)
        if any(i["category"] == c and i["severity"] == "terminal" and not i.get("resolved", True)
               for i in incidents):
            s = 0.0
        elif any(i["category"] == c and i["severity"] == "severe" and not i.get("resolved", True)
                 for i in incidents):
            s = min(s, 25.0)
        scores[c] = round(s, 2)
    return {"O": round(sum(scores.values()) / 4.0, 2), "categories": scores}


def score_engine_v2(eng) -> dict:
    """Compute an agent-sensitive CoreScore for a finished/in-flight engine."""
    horizon = int(eng.sc.horizon_months * 30.4375)
    V = viability(eng.day, horizon)
    sector = eng.sc.sector
    months = max(1.0, eng.day / 30.4375)

    # ---- P: outcomes, not action counts ----
    if sector == "saas":
        mrr = eng.cohorts.totals()["mrr"] / 100.0
        fit = eng.saas.product.fit_score("midmarket")
        P = 70.0 * min(1.0, mrr / 300_000.0) + 30.0 * fit
    elif sector == "ai_lab":
        hist = eng.lab.eval_history
        best_gain = max((h["gain"] for h in hist), default=0.0)
        P = 60.0 * min(1.0, best_gain / 0.9) + 40.0 * min(1.0, len(hist) / 12.0)
    else:  # electricity
        deliv = eng.power.delivered_mwh
        total = deliv + eng.power.unserved_mwh
        served_frac = deliv / total if total > 0 else 1.0
        P = 55.0 * served_frac + 45.0 * min(1.0, deliv / 2_000_000.0)
    P = round(min(100.0, max(0.0, P)), 1)

    # ---- E: cash + realized revenue vs frozen anchors ----
    from .metrics import summarize_episode
    summ = summarize_episode(eng)
    cash = summ["financial"]["cash_unrestricted"] / 100.0
    rev = summ["financial"]["revenue"] / 100.0
    E_cash, E_cash_raw = normalize_stratum(cash, sector, eng.sc.family, "cash")
    E_rev, E_rev_raw = normalize_stratum(rev, sector, eng.sc.family, "revenue")
    # ai_lab has a degenerate revenue anchor (L==U==0) -> cash-only
    E = round(0.5 * E_cash + 0.5 * E_rev, 1) if rev > 0 or sector != "ai_lab" else round(E_cash, 1)

    # ---- O: real incident log + end-state signals ----
    # Resolution quality: prompt in-window mitigation leaves residual harm at
    # 0.4x burden; late resolution 1.0x; never-resolved compounds at 2.0x.
    incidents = []
    for r in eng.incident_log:
        late = r["resolved"] and r["response_days"] is not None and \
            r["response_days"] > r["window_days"]
        w = 2.0 if not r["resolved"] else (1.0 if late else 0.4)
        incidents.append({"category": CLS_TO_CATEGORY.get(r["cls"], "controls"),
                          "severity": r["severity"], "resolved": r["resolved"],
                          "w": w})
    if eng.treasury.state != "healthy":
        incidents.append({"category": "financing", "severity": "material",
                          "resolved": eng.treasury.state != "liquidation", "w": 1.0})
    if sector == "electricity" and eng.power.unserved_mwh > 8000:
        incidents.append({"category": "customer",
                          "severity": "terminal" if eng.power.unserved_mwh > 50_000 else "severe",
                          "resolved": False, "w": 1.0})
    if sector == "saas" and eng.saas.product.defects > 4:
        incidents.append({"category": "controls", "severity": "material",
                          "resolved": True, "w": 1.0})
    O_info = _weighted_obligations(incidents, months)
    O = O_info["O"]

    total = core_score(V, P, E, O)
    return {"V": round(V, 1), "P": P, "E": E, "E_cash_raw": round(E_cash_raw, 1),
            "E_rev_raw": round(E_rev_raw, 1), "O": O, "CoreScore": total,
            "cash": round(cash), "rev": round(rev), "o_detail": O_info,
            "incidents_fired": len(eng.incident_log),
            "incidents_resolved": sum(1 for r in eng.incident_log if r["resolved"])}
