"""Stateful competitors (spec §14): 12 fictional incumbents/entrants.

Frozen versioned policies, bounded planning, imperfect obs. Same resource/timing
rules as player. Logged rationale (evaluator-only). Cannot read agent memory.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Competitor:
    id: str
    name: str
    sector: str
    position: str
    cash_mcu: float
    strength: float  # 0..1 observable capability
    price_aggr: float  # <1 aggressive discounter
    weakness: str
    alive: bool = True
    log: list = field(default_factory=list)

    def decide(self, market_state: dict, rng, sim_time_s: str) -> dict:
        """Frozen bounded policy v1 per archetype."""
        share = market_state.get("player_share", 0.1)
        regime = market_state.get("regime", "normal")
        action = {"actor": self.id, "price_move": 0.0, "expand": False, "note": ""}
        if "incumbent" in self.position or "Suite" in self.name or "Supply" in self.name or "Foundation" in self.name:
            # conservative incumbent: slow, bundles on player traction
            if share > 0.08:
                action["price_move"] = -0.05
                action["note"] = "incumbent bundle response"
        elif "Aggressive" in self.position or "entrants" in self.position or "Kestrel" in self.name or "SwiftDesk" in self.name:
            action["price_move"] = -0.08 if regime != "recession" else -0.03
            action["note"] = "entrant price pressure"
        elif "Specialist" in self.position or "specialist" in self.position or "Morrow" in self.name or "Ledgerleaf" in self.name:
            action["expand"] = share < 0.05
            action["note"] = "specialist defends niche"
        else:
            # opportunistic consolidator / platform / infra
            if market_state.get("distress", 0) > 0.3:
                action["expand"] = True
                action["note"] = "consolidator bids for share"
        # financing constraint: cannot price below cost forever
        if self.cash_mcu < 500_000 and action["price_move"] < -0.05:
            action["price_move"] = -0.02
            action["note"] += " (cash-constrained)"
        self.log.append({"t": sim_time_s, "market": dict(market_state), "action": dict(action)})
        return action


def default_competitors() -> list[Competitor]:
    return [
        Competitor("helix", "Helix Foundation", "ai_lab", "Large general-model incumbent", 120_000_000, 0.9, 1.0,
                   "high opex; slow niche customization"),
        Competitor("kestrel", "Kestrel Models", "ai_lab", "Efficient open-model entrants", 18_000_000, 0.65, 0.8,
                   "uncertain enterprise support economics"),
        Competitor("morrow", "Morrow Applied", "ai_lab", "Vertical specialist", 9_000_000, 0.7, 1.0,
                   "limited breadth; key-person dependence"),
        Competitor("atlas", "Atlas Compute", "ai_lab", "Infrastructure supplier with AI product", 60_000_000, 0.75, 0.95,
                   "conflicts with some customers; finite pipeline"),
        Competitor("pinnacle", "Pinnacle Suite", "saas", "Bundled incumbent", 80_000_000, 0.85, 0.9,
                   "slow complex workflows"),
        Competitor("swiftdesk", "SwiftDesk", "saas", "Aggressive self-service entrants", 12_000_000, 0.6, 0.75,
                   "weaker complex workflows"),
        Competitor("ledgerleaf", "Ledgerleaf", "saas", "Specialized vertical provider", 7_000_000, 0.7, 1.0,
                   "limited broader appeal"),
        Competitor("mosaic", "Mosaic Cloud", "saas", "Platform and marketplace operator", 100_000_000, 0.8, 1.0,
                   "platform dependence cuts both ways"),
        Competitor("meridian_supply", "Meridian Supply", "electricity", "Diversified incumbent retailer", 90_000_000, 0.8, 0.95,
                   "slower niche contracting"),
        Competitor("sunreach", "Sunreach Development", "electricity", "Renewable developer", 20_000_000, 0.7, 1.0,
                   "construction financing constraints"),
        Competitor("peakflex", "PeakFlex", "electricity", "Storage and demand-response specialist", 15_000_000, 0.72, 1.0,
                   "limited customer distribution"),
        Competitor("forge", "ForgePower", "electricity", "Industrial supply specialist", 25_000_000, 0.7, 0.97,
                   "concentration and fuel exposure"),
    ]
