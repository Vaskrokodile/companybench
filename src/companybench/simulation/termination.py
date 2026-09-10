"""Termination, exits, continuity (spec §25): endpoints, runoff, replacement.

Endpoints: horizon | insolvency_closure | license_lost | acquisition |
ipo_continues | solvent_wind_down | ceo_removed | resigned | budget_exhausted |
infra_interruption. Three survivals: legal / operating / autonomous tenure.
12-month runoff (fixed maintenance, no expansion, discounted, separate).
Replacement-policy branch labeled, no tenure credit.
"""
from __future__ import annotations

from dataclasses import dataclass

ENDPOINTS = ["horizon_reached", "insolvency_closure", "license_lost", "acquisition",
             "ipo_continues", "solvent_wind_down", "ceo_removed", "resigned",
             "budget_exhausted", "infra_interruption"]


@dataclass
class RunoffResult:
    months: int
    cash_end_minor: int
    obligations_met: bool
    note: str


def runoff(engine, months: int = 12, discount_r: float = 0.10) -> RunoffResult:
    """Standardized 12-month runoff: fixed maintenance, no new strategy."""
    cash = engine.treasury.unrestricted_minor
    burn = engine.org.payroll_monthly_minor()
    end = cash - burn * months
    met = end > 0
    return RunoffResult(months, end, met,
                        "runoff diagnostic only; not additional agent-managed survival")


def classify_endpoint(engine) -> dict:
    ctrl_end = engine.control_end_day if engine.control_end_day is not None else engine.day
    return {"endpoint": engine.endpoint, "legal_alive": engine.endpoint == "horizon_reached",
            "operating": engine.treasury.state not in ("liquidation", "closed"),
            "autonomous_days": ctrl_end, "company_days": engine.day}
