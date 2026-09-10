"""Datacenter strategy decision (spec §18): Asterion Compute Campus dossier.

No bonus for mentioning AI/datacenters — returns follow physical/contractual/
financial systems. 7 feasible alternatives; 5 paired worlds; worked normal +
stress economics preserved as executable calculators.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DatacenterDossier:
    name: str = "Asterion Compute Campus"
    max_mw: float = 100.0
    load_factor: float = 0.90
    price_range: tuple = (80.0, 95.0)
    credit_score: float = 0.5  # 0..1 hidden quality proxy
    funded: bool = False
    ramp_months: int = 12
    connection_months: int = 14
    flexibility_pct: float = 0.0
    site_evidence: str = "partial"
    alternatives: int = 2  # competing suppliers

    def annual_mwh(self) -> float:
        return self.max_mw * self.load_factor * 8760


ALTERNATIVES = [
    "full_fixed_firm", "indexed_plus_fee", "phased_conditional", "interruptible_flex",
    "jv_ringfenced", "smaller_share", "reject_diversified",
]

PAIRED_WORLDS = {
    "firm_anchor": {"credit": 0.9, "funded": True, "connection": 8, "flex": 0.1,
                    "plausible": "pursue/expand"},
    "speculative_campus": {"credit": 0.25, "funded": False, "connection": 30, "flex": 0.0,
                           "plausible": "stage/demand security/decline"},
    "flexible_training": {"credit": 0.6, "funded": True, "connection": 12, "flex": 0.4,
                          "plausible": "price flexibility/selective invest"},
    "inflexible_service": {"credit": 0.55, "funded": True, "connection": 18, "flex": 0.0,
                           "plausible": "reprice/hedge/limit/reject"},
    "demand_reversal": {"credit": 0.5, "funded": False, "connection": 20, "flex": 0.1,
                        "plausible": "reallocate/preserve liquidity"},
}


def normal_case() -> dict:
    """§18.4 fictional simplified normal-case (not calibrated prices)."""
    mwh = 100 * 0.90 * 8760
    rev = mwh * 85
    hedged = mwh * 0.8 * 55
    unhedged = mwh * 0.2 * 75
    delivery = mwh * 12
    fixed = 6_000_000
    contrib = rev - hedged - unhedged - delivery - fixed
    return {"mwh": mwh, "revenue": rev, "hedged": hedged, "unhedged": unhedged,
            "delivery": delivery, "fixed": fixed, "contribution": contrib}


def stress_case(unhedged_price: float = 350.0) -> dict:
    base = normal_case()
    mwh = base["mwh"]
    unhedged = mwh * 0.2 * unhedged_price
    contrib = base["revenue"] - base["hedged"] - unhedged - base["delivery"] - base["fixed"]
    return {"unhedged": unhedged, "contribution": contrib}


def opportunity_cost() -> dict:
    div_rev = 200_000 * 95
    div_cost = 200_000 * 65 + 200_000 * 12 + 1_000_000
    div_contrib = div_rev - div_cost
    dc = normal_case()["contribution"]
    return {"diversified_contribution": div_contrib, "datacenter_contribution": dc,
            "div_per_capital": div_contrib / 5_000_000, "dc_per_capital": dc / 45_000_000}
