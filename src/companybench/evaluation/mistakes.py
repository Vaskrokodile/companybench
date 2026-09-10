"""Mistakes & decision quality (spec §29): 10 classes, evidence records, replay.

Loss ≠ mistake: judged on knowable info at decision time. Forecast skill via
Brier + interval coverage, not single misses. Strategy labels need dominance
evidence, not hindsight.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CLASSES = ["arithmetic", "state_tracking", "execution", "capacity", "deadline",
           "process", "forecast", "strategy", "recovery", "integrity"]


@dataclass
class Mistake:
    mistake_id: str
    root_cause_id: str
    cls: str
    decision_event_id: str
    evidence_ids: list
    claim: str
    known_feasible_alternative: str = ""
    controllability: str = "high"
    severity: str = "material"  # minor|material|severe|terminal
    realized_direct_loss_minor: int = 0
    label_method: str = "rule_plus_blinded_review"
    review_status: str = "proposed"
    recovery_event_ids: list = field(default_factory=list)


def brier_score(forecasts: list[float], outcomes: list[int]) -> float:
    assert len(forecasts) == len(outcomes) and forecasts
    return sum((f - o) ** 2 for f, o in zip(forecasts, outcomes)) / len(forecasts)


def interval_coverage(intervals: list[tuple[float, float]], outcomes: list[float]) -> dict:
    hits = sum(1 for (lo, hi), y in zip(intervals, outcomes) if lo <= y <= hi)
    width = sum(hi - lo for lo, hi in intervals) / len(intervals) if intervals else 0.0
    return {"coverage": hits / len(outcomes) if outcomes else 0.0, "mean_width": width}


RULE_DETECTORS = {
    "funding_as_revenue": "booking/financing recorded in revenue accounts",
    "unsigned_as_active": "acting on indicative offer as settled cash",
    "double_capacity": "same reserved GPU/MWh share sold twice",
    "missed_deadline": "known material deadline passed with feasible options",
    "over_authority": "signed above authority without board approval",
}
