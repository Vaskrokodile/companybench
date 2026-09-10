"""Macro regimes (spec §14.3): versioned stochastic process, bounded persistence,
cross-variable correlation. Recession hits demand + financing together.
No shock keyed to player cash (fairness §14.4).
"""
from __future__ import annotations

from dataclasses import dataclass, field

REGIMES = ["expansion", "normal", "slowdown", "recession", "recovery"]
VERSION = "macro_v1"

# transition rows: bounded persistence (diagonal-heavy), correlated
TRANSITION = {
    "expansion": {"expansion": 0.75, "normal": 0.2, "slowdown": 0.05, "recession": 0.0, "recovery": 0.0},
    "normal": {"expansion": 0.1, "normal": 0.7, "slowdown": 0.15, "recession": 0.03, "recovery": 0.02},
    "slowdown": {"expansion": 0.02, "normal": 0.2, "slowdown": 0.55, "recession": 0.18, "recovery": 0.05},
    "recession": {"expansion": 0.0, "normal": 0.05, "slowdown": 0.2, "recession": 0.6, "recovery": 0.15},
    "recovery": {"expansion": 0.15, "normal": 0.35, "slowdown": 0.1, "recession": 0.02, "recovery": 0.38},
}

EFFECTS = {
    # demand_mult, funding_appetite, rate_delta, labor_avail, energy_cost_mult
    "expansion": {"demand": 1.12, "funding": 1.25, "rate": -0.005, "labor": 0.85, "energy": 1.05},
    "normal": {"demand": 1.0, "funding": 1.0, "rate": 0.0, "labor": 1.0, "energy": 1.0},
    "slowdown": {"demand": 0.9, "funding": 0.7, "rate": 0.005, "labor": 1.1, "energy": 0.97},
    "recession": {"demand": 0.75, "funding": 0.4, "rate": 0.01, "labor": 1.25, "energy": 0.9},
    "recovery": {"demand": 0.95, "funding": 0.9, "rate": 0.0, "labor": 1.05, "energy": 0.98},
}


@dataclass
class MacroState:
    regime: str = "normal"
    base_rate: float = 0.05
    month: int = 0
    history: list = field(default_factory=list)

    def step(self, rng, sim_time_s: str) -> str:
        row = TRANSITION[self.regime]
        u = rng.uniform("macro", "regime", sim_time_s, "transition", self.month)
        cum, nxt = 0.0, self.regime
        for k, p in row.items():
            cum += p
            if u < cum:
                nxt = k
                break
        self.regime = nxt
        self.month += 1
        self.history.append(nxt)
        return nxt

    def effects(self) -> dict:
        e = dict(EFFECTS[self.regime])
        e["rate_level"] = self.base_rate + e["rate"]
        e["regime"] = self.regime
        return e
