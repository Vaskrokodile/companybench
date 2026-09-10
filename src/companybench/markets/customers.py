"""Customers, cohorts, choice, churn, CAC/LTV (spec §12).

- Large accounts explicit; small buyers aggregated cohorts w/ heterogeneity.
- Logit demand with outside option; infeasible fail minimum requirements first.
- Cancellable hazard logistic(monthly p, converted if applied daily); annual
  contracts use renewal decisions + early-termination only.
- GRR/NRR/CAC/payback per spec; zero-base ratios null; cohort ages reported.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, x))))


# ---------- acquisition choice (spec §41.9) ----------
def choice_probs(utilities: dict[str, float]) -> dict[str, float]:
    """Logit with outside option; numerically stabilized. Infeasible excluded upstream."""
    m = max(utilities.values()) if utilities else 0.0
    exps = {k: math.exp(v - m) for k, v in utilities.items()}
    tot = sum(exps.values()) or 1.0
    return {k: v / tot for k, v in exps.items()}


def utility(price_std: float, quality: float, trust: float, switch_cost: float,
            price_sens: float = 1.0) -> float:
    return quality + trust - price_sens * price_std - switch_cost


# ---------- churn ----------
def cancel_hazard(base: float, dissat: float, pull: float, stress: float, friction: float) -> float:
    """Monthly hazard for cancellable subscriptions (explicit period)."""
    return sigmoid(base + dissat + pull + stress - friction)


def daily_from_monthly(p_monthly: float) -> float:
    return 1.0 - (1.0 - min(max(p_monthly, 0.0), 1.0)) ** (1.0 / 30.0)


# ---------- cohorts ----------
@dataclass
class Cohort:
    id: str
    start_ym: str
    mrr_start_minor: int
    mrr: int = 0
    customers: int = 0
    age_months: int = 0

    def __post_init__(self) -> None:
        if self.mrr == 0:
            self.mrr = self.mrr_start_minor


@dataclass
class CohortLedger:
    cohorts: dict[str, Cohort] = field(default_factory=dict)

    def add(self, c: Cohort) -> None:
        self.cohorts[c.id] = c

    def step(self, cid: str, churned_minor: int, contraction_minor: int,
             expansion_minor: int, new_mrr_minor: int = 0, lost_logos: int = 0) -> dict:
        c = self.cohorts[cid]
        start = c.mrr
        c.mrr = max(0, start - churned_minor - contraction_minor + expansion_minor + new_mrr_minor)
        c.customers = max(0, c.customers - lost_logos)
        c.age_months += 1
        if start <= 0:
            grr = None
            nrr = None
        else:
            grr = (start - churned_minor - contraction_minor) / start
            nrr = (start - churned_minor - contraction_minor + expansion_minor) / start
        return {"grr": grr, "nrr": nrr, "start": start, "end": c.mrr}

    def totals(self) -> dict:
        return {"mrr": sum(c.mrr for c in self.cohorts.values()),
                "customers": sum(c.customers for c in self.cohorts.values())}


def cac(attributable_spend_minor: int, new_paying: int) -> int | None:
    if new_paying <= 0:
        return None
    return attributable_spend_minor // new_paying


def cac_payback_months(cac_minor: int | None, monthly_gross_per_new_minor: int) -> float | str:
    if cac_minor is None or monthly_gross_per_new_minor <= 0:
        return "not_achieved_nonpositive_gross_profit"
    return cac_minor / monthly_gross_per_new_minor


# ---------- CRM pipeline ----------
@dataclass
class Opportunity:
    id: str
    segment: str
    value_mcu: float
    stage: str = "lead"  # lead→qualified→demo→pilot→negotiation→procurement→signed→live→paying
    months_in_stage: int = 0
    win_prob: float = 0.2


class Pipeline:
    STAGES = ["lead", "qualified", "demo", "pilot", "negotiation", "procurement", "signed", "live", "paying"]

    def __init__(self) -> None:
        self.opps: dict[str, Opportunity] = {}
        self._seq = 0

    def add(self, segment: str, value_mcu: float, win_prob: float = 0.2) -> str:
        self._seq += 1
        oid = f"opp_{self._seq:04d}"
        self.opps[oid] = Opportunity(oid, segment, value_mcu, "lead", 0, win_prob)
        return oid

    def advance(self, oid: str, to_live: bool = False, won: bool = False) -> str:
        o = self.opps[oid]
        i = self.STAGES.index(o.stage)
        o.stage = self.STAGES[min(len(self.STAGES) - 1, i + 1)]
        o.months_in_stage = 0
        return o.stage
