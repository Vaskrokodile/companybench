"""Scenario manifests (spec §20, §41): 3 sectors × 4 families × seeds.

Families: build_discover | scale_finance | compete_adapt | compound_stress.
Difficulty L1..L5. Opening sheets/teams/ownership per §41.2-41.4 (MCU thousands).
Production loader must reject ranked runs with uncalibrated anchors.
"""
from __future__ import annotations

from dataclasses import dataclass, field

SECTORS = ["ai_lab", "saas", "electricity"]
FAMILIES = ["build_discover", "scale_finance", "compete_adapt", "compound_stress"]

OPENING_MCU_THOUSANDS = {
    "ai_lab": {"cash": 8000, "restricted": 0, "receivables": 100, "prepaid": 500,
               "equip": 400, "dev_rights": 0, "payables": 200, "deferred": 100, "debt": 0,
               "equity": 8700, "employees": 12, "burn_month": 300},
    "saas": {"cash": 1500, "restricted": 0, "receivables": 24, "prepaid": 36,
             "equip": 90, "dev_rights": 0, "payables": 50, "deferred": 100, "debt": 0,
             "equity": 1500, "employees": 6, "burn_month": 85},
    "electricity": {"cash": 12000, "restricted": 3000, "receivables": 2000, "prepaid": 0,
                    "equip": 500, "dev_rights": 1500, "payables": 2000, "deferred": 0,
                    "debt": 2000, "equity": 15000, "employees": 14, "burn_month": 220},
}

STARTING_TEAMS = {
    "ai_lab": ["CEO", "researcher x4", "ml_engineer x3", "data lead", "product lead",
               "commercial lead", "operations lead"],
    "saas": ["CEO", "engineer x3", "product/design lead", "customer/commercial lead"],
    "electricity": ["CEO", "procurement/trading x3", "project/engineering x3", "commercial x2",
                    "operations x2", "finance", "credit/risk", "compliance"],
}

FAMILY_DESC = {
    "ai_lab": {
        "build_discover": "Find a valuable domain with limited compute",
        "scale_finance": "Demand grows faster than serving capacity",
        "compete_adapt": "Open-model improvement compresses pricing",
        "compound_stress": "Compute disruption + funding slowdown",
    },
    "saas": {
        "build_discover": "Discover repeatable customer fit",
        "scale_finance": "Growth stresses onboarding and systems",
        "compete_adapt": "Incumbent bundles a competing feature",
        "compound_stress": "Renewal weakness + receivable delay",
    },
    "electricity": {
        "build_discover": "Select a profitable supply/development niche",
        "scale_finance": "Large-load opportunity strains collateral + project finance",
        "compete_adapt": "New supply changes spreads + bargaining",
        "compound_stress": "Price shock + construction/connection delay",
    },
}

DIFFICULTY = {
    1: "Mechanics: stable demand, simple contracts, transparent reports",
    2: "Management: hiring delays, cohorts, working capital, realistic rivals",
    3: "Strategy: mutually exclusive bets, ambiguous info, nonlinear scaling",
    4: "Frontier: regime shifts, latent discoverable risks, delayed liabilities",
    5: "Generalization: unseen institution/tech/contract combos, documented primitives",
}


@dataclass
class Scenario:
    id: str
    sector: str
    family: str
    seed: int
    difficulty: int
    horizon_months: int = 60
    opening: dict = field(default_factory=dict)
    paired_world: str | None = None  # energy datacenter variants
    notes: str = ""

    def manifest(self) -> dict:
        return {"benchmark": "CompanyBench", "specification_version": "0.1.0",
                "manifest_status": "illustrative_uncalibrated",
                "track": "assigned_sector_core", "horizon_months": self.horizon_months,
                "start_date": "2031-01-01", "currency": "MCU",
                "sector": self.sector, "family": self.family, "seed": self.seed,
                "difficulty": self.difficulty, "opening": self.opening,
                "rules": {"jurisdiction": "meridian_v1", "accounting": "companybench_accrual_v1",
                          "tax_rate": 0.25},
                "evaluation": {"discount_rate_annual": 0.10,
                               "score_weights": {"V": 0.25, "P": 0.25, "E": 0.30, "O": 0.20}},
                "visibility": {"public": ["rules", "tool_schemas", "milestone_rules",
                                          "budget_rules", "initial_dossier"],
                               "private": ["world_seed", "latent_states", "future_shocks",
                                           "competitor_private_state"]}}


def all_core_scenarios(seeds_per_family: int = 10, horizon: int = 60) -> list[Scenario]:
    out = []
    for s in SECTORS:
        for f in FAMILIES:
            for seed in range(seeds_per_family):
                diff = 2 + (seed % 3)  # L2-L4 spread in Core
                out.append(Scenario(f"{s}_{f}_s{seed:02d}", s, f, seed, diff, horizon,
                                    dict(OPENING_MCU_THOUSANDS[s]),
                                    paired_world=None,
                                    notes=FAMILY_DESC[s][f]))
    return out


def pilot_matrix() -> list[Scenario]:
    """24-episode pilot: 2 worlds per sector/family, 1 replicate (spec §30.2)."""
    out = []
    for s in SECTORS:
        for f in FAMILIES:
            for seed in (0, 1):
                out.append(Scenario(f"{s}_{f}_s{seed:02d}", s, f, seed, 3, 60,
                                    dict(OPENING_MCU_THOUSANDS[s]), notes=FAMILY_DESC[s][f]))
    return out


def long_horizon(sector: str, family: str, seed: int, months: int = 120) -> Scenario:
    return Scenario(f"{sector}_{family}_lh{seed}", sector, family, seed, 4, months,
                    dict(OPENING_MCU_THOUSANDS[sector]), notes="Long Horizon 120-month compounding")
