"""SaaS sector (spec §16): Harbor Software — calibrated.

Churn bases and sales cycles now from params_v1.0 (SRC-01/02). Hazard bases
are logit(mean_monthly_prob) so sigmoid(base) = mean churn.
"""
from __future__ import annotations

from dataclasses import dataclass, field

try:
    from ..calibration.registry import get as _get
    SEGMENTS = {
        "smb": {"desc": "Fast self-service; low ACV; frequent churn",
                "acv_mcu": 1_200, "sales_cycle_days": int(_get("saas.smb_sales_cycle_days")),
                "churn_base": float(_get("saas.smb_churn_base")), "wtp_mcu": 1_500},
        "midmarket": {"desc": "Demos+integrations; moderate contracts",
                      "acv_mcu": 12_000, "sales_cycle_days": int(_get("saas.midmarket_sales_cycle_days")),
                      "churn_base": float(_get("saas.midmarket_churn_base")), "wtp_mcu": 15_000},
        "enterprise": {"desc": "Security/legal; multi-team rollout; annual",
                       "acv_mcu": 120_000, "sales_cycle_days": int(_get("saas.enterprise_sales_cycle_days")),
                       "churn_base": float(_get("saas.enterprise_churn_base")), "wtp_mcu": 150_000},
        "regulated": {"desc": "Controls+workflows+references",
                      "acv_mcu": 80_000, "sales_cycle_days": int(_get("saas.regulated_sales_cycle_days")),
                      "churn_base": float(_get("saas.regulated_churn_base")), "wtp_mcu": 100_000},
    }
except Exception:
    SEGMENTS = {
        "smb": {"desc": "Fast self-service; low ACV; frequent churn", "acv_mcu": 1_200,
                "sales_cycle_days": 14, "churn_base": -3.317, "wtp_mcu": 1_500},
        "midmarket": {"desc": "Demos+integrations; moderate contracts", "acv_mcu": 12_000,
                      "sales_cycle_days": 75, "churn_base": -4.185, "wtp_mcu": 15_000},
        "enterprise": {"desc": "Security/legal; multi-team rollout; annual", "acv_mcu": 120_000,
                       "sales_cycle_days": 200, "churn_base": -4.955, "wtp_mcu": 150_000},
        "regulated": {"desc": "Controls+workflows+references", "acv_mcu": 80_000,
                      "sales_cycle_days": 260, "churn_base": -4.701, "wtp_mcu": 100_000},
    }

COMPONENTS = ["core_workflow", "collaboration", "reporting", "integrations",
              "access_control", "auditability", "automation", "performance",
              "migration", "billing", "support_tooling"]

MIN_REQUIREMENTS = {
    "smb": {"core_workflow"},
    "midmarket": {"core_workflow", "reporting", "integrations"},
    "enterprise": {"core_workflow", "access_control", "auditability", "support_tooling", "migration"},
    "regulated": {"core_workflow", "access_control", "auditability", "reporting"},
}

COMPLEMENT_PENALTY = {("auditability", "access_control"): 0.85}


@dataclass
class ProductState:
    shipped: dict = field(default_factory=dict)
    defects: int = 5
    tech_debt_h: float = 0.0
    capacity_units: float = 1000.0
    load_units: float = 200.0
    uptime_30d: float = 0.999
    cloud_mcu_month: float = 4_000.0

    def __post_init__(self) -> None:
        for c in COMPONENTS:
            self.shipped.setdefault(c, 0)

    def meets(self, segment: str) -> tuple[bool, list]:
        missing = [c for c in MIN_REQUIREMENTS[segment] if self.shipped.get(c, 0) < 1]
        return (len(missing) == 0, missing)

    def fit_score(self, segment: str) -> float:
        req = MIN_REQUIREMENTS[segment]
        have = sum(min(3, self.shipped.get(c, 0)) for c in req) / (3 * len(req))
        for (a, b), pen in COMPLEMENT_PENALTY.items():
            if self.shipped.get(a, 0) > 0 and self.shipped.get(b, 0) == 0:
                have *= pen
        quality = max(0.0, 1.0 - self.defects * 0.02 - self.tech_debt_h / 2000.0)
        return max(0.0, min(1.0, 0.6 * have + 0.4 * quality))

    def outage_prob_month(self) -> float:
        util = self.load_units / max(1.0, self.capacity_units)
        base = 0.01 + max(0.0, util - 0.7) * 0.25 + self.defects * 0.002 + self.tech_debt_h / 50000.0
        return min(0.5, base)


def mrr_arr_policy(active_subs_mcu_month: float) -> dict:
    return {"mrr": active_subs_mcu_month, "arr": active_subs_mcu_month * 12}


def cohort_example() -> dict:
    start, churn, contraction, expansion, new = 100_000, 5_000, 3_000, 12_000, 20_000
    end = start - churn - contraction + expansion + new
    grr = (start - churn - contraction) / start
    nrr = (start - churn - contraction + expansion) / start
    return {"end_mrr": end, "grr": grr, "nrr": nrr, "new": new}

def acquisition_example() -> dict:
    spend, new_logos = 60_000, 20
    cac = spend / new_logos
    payback = cac / (300 * 0.8)
    return {"cac": cac, "payback_months": payback, "new_mrr": 6_000}


@dataclass
class SaaSState:
    product: ProductState = field(default_factory=ProductState)
    trials: int = 20
    gtm: str = "hybrid"
    price_per_seat_mcu: float = 50.0
    discount_pct: float = 0.0
    commission_rate: float = 0.1
    csm_count: int = 0
