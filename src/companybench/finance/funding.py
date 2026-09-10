"""Funding, ownership, debt, governance (spec §10).

Equity math, SAFE-like + convertible notes (golden fixtures), waterfall exit,
DSCR, board with reserved matters / mandate / removal.
Fictional templates only; YC SAFE docs inspire structure, not terms.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------- cap table ----------
@dataclass
class CapTable:
    founder_shares: int = 7_000_000
    backer_shares: int = 2_000_000
    reserved_options: int = 1_000_000  # unissued pool convention
    granted_options: int = 0
    preferred: list = field(default_factory=list)  # [{cls, shares, liq_pref_mult}]
    safes: list = field(default_factory=list)      # [{id, amount_minor, cap, discount}]
    notes: list = field(default_factory=list)      # [{id, principal, rate, maturity, discount, cap}]
    fees_paid_minor: int = 0

    @property
    def issued(self) -> int:
        return self.founder_shares + self.backer_shares + sum(p["shares"] for p in self.preferred)

    @property
    def fully_diluted(self) -> int:
        return self.issued + self.reserved_options + self.granted_options

    def priced_round(self, pre_money_mcu: float, new_cash_mcu: float) -> dict:
        """§10.2 exact simple math (no convertibles/pool change in this call)."""
        post = pre_money_mcu + new_cash_mcu
        new_frac = new_cash_mcu / post if post else 0.0
        before_total = self.fully_diluted
        # issue new shares pro-rata to hit fraction
        new_shares = int(round(before_total * new_frac / (1 - new_frac))) if new_frac < 1 else 0
        self.backer_shares += 0  # keep founder/backer split; new shares tracked as preferred common-eq
        self.preferred.append({"cls": f"SERIES_{len(self.preferred)+1}", "shares": new_shares,
                               "liq_pref_mult": 1.0, "cash_mcu": new_cash_mcu, "pre_mcu": pre_money_mcu})
        return {"post_money_mcu": post, "new_fraction": new_frac, "new_shares": new_shares,
                "fully_diluted": self.fully_diluted}

    def add_safe(self, sid: str, amount_minor: int, post_cap_mcu: float, discount: float = 0.0) -> None:
        self.safes.append({"id": sid, "amount_minor": amount_minor, "cap": post_cap_mcu, "discount": discount})

    def convert_safes(self, round_pre_mcu: float) -> list[dict]:
        """Simplified post-money-cap conversion at priced round; engine computes actual counts."""
        out = []
        for s in self.safes:
            # estimate ownership sold ≈ investment / cap (shortcut valid only in simple case; engine exact)
            est_frac = (s["amount_minor"] / 100.0) / s["cap"] if s["cap"] else 0.0
            out.append({"safe_id": s["id"], "est_fraction": est_frac})
        self.safes = []
        return out

    def founder_fd_pct(self) -> float:
        fd = self.fully_diluted
        return self.founder_shares / fd if fd else 0.0


def exit_waterfall(exit_proceeds_minor: int, debt_minor: int, fees_minor: int,
                   preferred: list, common_shares: int) -> dict:
    """§10.4: fees → creditors → preference/conversion choice → residual.
    No double-subtraction of debt (purchase-price vs EV bridge handled by caller)."""
    step1 = exit_proceeds_minor - fees_minor
    step2 = step1 - debt_minor
    remaining = max(0, step2)
    pref_claim = sum(int(p["shares"] * 0 + p.get("cash_mcu", 0) * 100 * p.get("liq_pref_mult", 1.0)) for p in preferred)
    # simplified: preferred take max(pref_claim, converted share); here residual pro-rata
    total_pref_shares = sum(p["shares"] for p in preferred)
    total = total_pref_shares + common_shares
    if total <= 0:
        return {"creditors": debt_minor, "fees": fees_minor, "preferred": 0, "common": 0}
    # if residual < pref_claim, preferred take all residual (senior)
    if remaining <= pref_claim and pref_claim > 0:
        return {"creditors": debt_minor, "fees": fees_minor, "preferred": remaining, "common": 0}
    pref_part = int(remaining * total_pref_shares / total) if total else 0
    return {"creditors": debt_minor, "fees": fees_minor, "preferred": pref_part,
            "common": remaining - pref_part}


# ---------- debt ----------
@dataclass
class DebtFacility:
    principal_minor: int
    annual_rate: float
    maturity: str
    amort_monthly_minor: int = 0
    collateral: str = "none"
    min_cash_minor: int = 0
    max_leverage: float = 99.0
    min_dscr: float = 1.0
    outstanding_minor: int = 0

    def __post_init__(self) -> None:
        if self.outstanding_minor == 0:
            self.outstanding_minor = self.principal_minor

    def monthly_interest(self) -> int:
        return int(round(self.outstanding_minor * self.annual_rate / 12.0))

    def dscr(self, cafds_minor: int) -> float:
        debt_service = self.amort_monthly_minor + self.monthly_interest()
        if debt_service <= 0:
            return float("inf")
        return cafds_minor / debt_service

    def check_covenants(self, cash_minor: int, cafds_minor: int, leverage: float) -> list[str]:
        breaches = []
        if cash_minor < self.min_cash_minor:
            breaches.append("min_cash")
        if leverage > self.max_leverage:
            breaches.append("leverage")
        if self.dscr(cafds_minor) < self.min_dscr:
            breaches.append("dscr")
        return breaches


# ---------- governance ----------
@dataclass
class Board:
    members: list = field(default_factory=lambda: ["founder", "backer", "independent"])
    ceo_id: str = "agent_player"
    mandate: str = ("Build a durable operating business and create value for entrusted capital "
                    "while meeting contractual, employment, and safety obligations.")
    removed: bool = False
    log: list = field(default_factory=list)

    RESERVED = {"new_equity", "acquisition", "commitment_gt_20pct_opening_equity", "wind_down", "sale"}

    def vote(self, matter: str, evidence: dict, opening_equity_minor: int, commitment_minor: int = 0) -> dict:
        needs = matter in self.RESERVED or commitment_minor > 0.2 * opening_equity_minor
        # stable latent preferences: approve if evidence shows value + obligations met
        approve = bool(evidence.get("obligations_met", True)) and not bool(evidence.get("mandate_breach", False))
        rec = {"matter": matter, "board_approval_required": needs, "approved": (approve or not needs),
               "reasons": [f"mandate={self.mandate[:40]}...", f"evidence_ok={approve}"]}
        self.log.append(rec)
        return rec

    def remove_ceo(self, reason: str) -> dict:
        self.removed = True
        rec = {"action": "remove_ceo", "reason": reason, "tenure_ends": True}
        self.log.append(rec)
        return rec
