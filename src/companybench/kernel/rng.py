"""Deterministic counter-based RNG field (spec §30.3).

draw = RNG(world_seed, subsystem, entity_id, simulated_time, event_type, draw_index)

Properties:
- Stable event IDs + counter generators: one extra query never rerolls history.
- Macro weather/demand/financing paired across models; hiring/churn/failure
  conditional on each model's actions via entity_id + time + index.
- Opaque to agent: seeds never exposed through the tool gateway.
"""
from __future__ import annotations

import hashlib
import math
import struct

MAX_UINT64 = (1 << 64) - 1


def _h64(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    return struct.unpack(">Q", h[:8])[0]


class StableRNG:
    """Seed-stable random field for one episode."""

    def __init__(self, world_seed: str | int) -> None:
        self.world_seed = str(world_seed)

    def key(self, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> int:
        return _h64(self.world_seed, subsystem, str(entity_id), str(sim_time), str(event_type), str(int(draw_index)))

    def uniform(self, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> float:
        """Uniform [0,1)."""
        return (self.key(subsystem, entity_id, sim_time, event_type, draw_index) >> 11) * (1.0 / (1 << 53))

    def randint(self, low: int, high: int, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> int:
        assert low < high
        span = high - low
        return low + int(self.uniform(subsystem, entity_id, sim_time, event_type, draw_index) * span)

    def normal(self, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> float:
        """Standard normal via Box-Muller on two stable uniforms."""
        u1 = max(self.uniform(subsystem, entity_id, sim_time, event_type, draw_index * 2), 1e-12)
        u2 = self.uniform(subsystem, entity_id, sim_time, event_type, draw_index * 2 + 1)
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    def choice(self, options: list, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0):
        if not options:
            raise ValueError("empty choice")
        return options[self.randint(0, len(options), subsystem, entity_id, sim_time, event_type, draw_index)]

    def bernoulli(self, p: float, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> bool:
        return self.uniform(subsystem, entity_id, sim_time, event_type, draw_index) < p

    def exponential(self, rate: float, subsystem: str, entity_id: str, sim_time: str, event_type: str, draw_index: int = 0) -> float:
        u = max(self.uniform(subsystem, entity_id, sim_time, event_type, draw_index), 1e-12)
        return -math.log(u) / rate
