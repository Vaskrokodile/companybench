"""Incidents, crises, recovery (spec §21): 8 classes, ~30 templates.

Each event: trigger, hidden cause, affected entities, observable signals,
response window, mitigations, cash/ops consequences, termination. Severity
follows exposure — no position, no same loss. Correlated via shared drivers.
Recovery measured: detection/response delay, containment cost, restoration,
customer recovery, recurrence. Crisis density fits attention budget.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IncidentTemplate:
    id: str
    cls: str  # liquidity|demand|people|technical|supply|governance|contract|physical
    title: str
    signals: list
    window_days: int
    mitigations: list
    loss_mcu_range: tuple
    termination: str


TEMPLATES: list[IncidentTemplate] = [
    IncidentTemplate("liq_delayed_receivable", "liquidity", "Major customer pays 60 days late",
                     ["aging report", "cash forecast dip"], 21,
                     ["bridge line", "renegotiate terms", "factoring"], (20_000, 300_000),
                     "cash collected or written down"),
    IncidentTemplate("liq_collateral_call", "liquidity", "Wholesale collateral call after price spike",
                     ["margin notice", "exposure report"], 2,
                     ["post cash/LC", "reduce position", "negotiate"], (50_000, 2_000_000),
                     "call met or position closed"),
    IncidentTemplate("liq_funding_fail", "liquidity", "Lead investor withdraws before close",
                     ["dataroom stalls", "partner delay"], 45,
                     ["bridge", "cut burn", "new pipeline"], (0, 500_000),
                     "round closed / plan reset"),
    IncidentTemplate("dem_churn_wave", "demand", "Churn wave after price increase",
                     ["usage decline", "NPS drop", "tickets"], 60,
                     ["rollback/discount", "fix onboarding", "win-back"], (10_000, 400_000),
                     "retention stabilizes 2 closes"),
    IncidentTemplate("dem_budget_freeze", "demand", "Enterprise budget freeze delays procurement",
                     ["pipeline stalls"], 90, ["midmarket pivot", "phased deal"], (0, 250_000),
                     "deal won/lost or quarter ends"),
    IncidentTemplate("dem_substitution", "demand", "Competitor substitutes core seat",
                     ["loss notes", "price undercut"], 60, ["reprice", "differentiate"], (15_000, 500_000),
                     "share stabilizes"),
    IncidentTemplate("ppl_resignation", "people", "Critical lead resigns pre-launch",
                     ["workload spike", "1:1 flags"], 30,
                     ["retention package", "succession", "contractor"], (10_000, 200_000),
                     "role backfilled + handover"),
    IncidentTemplate("ppl_burnout", "people", "Team burnout after crunch",
                     ["velocity drop", "sick leave"], 45, ["hire", "descope", "recovery sprint"],
                     (5_000, 120_000), "workload normalized"),
    IncidentTemplate("ppl_weak_hire", "people", "Key hire misfires probation",
                     ["missed acceptance", "peer flags"], 90, ["PIP", "replace"], (20_000, 150_000),
                     "role performing or exited"),
    IncidentTemplate("tech_outage", "technical", "Production outage (region/dependency)",
                     ["error budget burn", "status page"], 3,
                     ["failover", "rollback", "credits"], (5_000, 300_000), "SLO restored 14d"),
    IncidentTemplate("tech_regression", "technical", "Model/product regression in deployment",
                     ["heldout drop", "complaints"], 21, ["rollback", "fix eval"], (10_000, 250_000),
                     "hidden eval passes"),
    IncidentTemplate("tech_migration_fail", "technical", "Customer migration fails midway",
                     ["stuck jobs", "data diff"], 14, ["rehearse", "dual-run", "compensate"],
                     (10_000, 200_000), "migration accepted"),
    IncidentTemplate("sup_gpu_shortage", "supply", "Accelerator allocation cut/delayed",
                     ["supplier notice", "queue slip"], 60, ["reserve alt", "efficient model", "stage"],
                     (15_000, 600_000), "capacity secured or plan rescoped"),
    IncidentTemplate("sup_equip_delay", "supply", "Equipment/transformer delivery slips 6 months",
                     ["milestone miss"], 90, ["alt vendor", "resequence"], (30_000, 800_000),
                     "delivered or project sold"),
    IncidentTemplate("sup_fuel_disruption", "supply", "Fuel/availability squeeze lifts spot",
                     ["forward curve", "outage notices"], 30, ["hedge", "pass-through"], (20_000, 900_000),
                     "curve normalizes or hedged"),
    IncidentTemplate("gov_board_clash", "governance", "Board blocks spend after missed reporting",
                     ["reporting flag"], 30, ["submit plan", "accept covenant"], (0, 100_000),
                     "approval granted"),
    IncidentTemplate("gov_investor_conflict", "governance", "Investor demands restrictive exclusivity",
                     ["term sheet clause"], 21, ["negotiate", "walk away"], (0, 300_000),
                     "terms signed/declined"),
    IncidentTemplate("con_rights_dispute", "contract", "Dataset rights revoked for commercial training",
                     ["legal notice"], 45, ["license", "filter/retrain", "settle"], (25_000, 700_000),
                     "rights cleared or asset ring-fenced"),
    IncidentTemplate("con_service_claim", "contract", "Customer files SLA/service claim",
                     ["claim letter"], 30, ["remediate", "credit", "dispute"], (5_000, 250_000),
                     "claim settled"),
    IncidentTemplate("con_permit_condition", "contract", "Permit conditioned on costly upgrade",
                     ["regulator notice"], 120, ["redesign", "appeal", "sell rights"], (50_000, 1_000_000),
                     "permit granted/denied"),
    IncidentTemplate("phy_generator_outage", "physical", "Forced generator outage in heat wave",
                     ["telemetry", "price spike"], 7, ["reserves", "buy spot", "curtail flex"],
                     (20_000, 800_000), "unit returned"),
    IncidentTemplate("phy_grid_constraint", "physical", "Interconnector derated during peak",
                     ["constraint notice"], 14, ["reroute", "storage dispatch"], (15_000, 500_000),
                     "limit restored"),
    IncidentTemplate("phy_storage_fault", "physical", "Battery string fault halves usable energy",
                     ["BMS alarm"], 21, ["isolate string", "warranty"], (10_000, 300_000),
                     "capacity restored"),
    IncidentTemplate("ai_contamination", "technical", "Dataset contamination discovered post-train",
                     ["audit flags"], 30, ["decontaminate", "retrain slice"], (30_000, 500_000),
                     "clean eval passes"),
    IncidentTemplate("ai_checkpoint_loss", "technical", "Checkpoint recovery fails after preemption",
                     ["job log"], 7, ["frequent ckpt", "reserved capacity"], (5_000, 120_000),
                     "run resumed"),
    IncidentTemplate("sec_breach", "technical", "Security breach via integration token",
                     ["IDS alert"], 14, ["rotate", "audit", "notify"], (20_000, 600_000),
                     "review passed + monitoring 30d"),
    IncidentTemplate("receivable_default", "liquidity", "Major account insolvent owing 90d",
                     ["credit watch"], 45, ["provision", "collections", "insure"], (30_000, 500_000),
                     "recovered/written off"),
    IncidentTemplate("integration_break", "technical", "Key platform integration breaks",
                     ["error spike"], 14, ["pin version", "rebuild"], (5_000, 150_000),
                     "integration green 14d"),
    IncidentTemplate("bundling_attack", "demand", "Incumbent bundles your flagship feature free",
                     ["win-loss notes"], 90, ["verticalize", "reprice", "partner"], (20_000, 600_000),
                     "cohort NRR recovers or pivot done"),
    IncidentTemplate("connection_delay", "contract", "Load connection slips 14 months",
                     ["TSO study"], 120, ["stage supply", "conditional dates"], (40_000, 900_000),
                     "energized or contract restructured"),
]


def by_class(cls: str) -> list[IncidentTemplate]:
    return [t for t in TEMPLATES if t.cls == cls]
