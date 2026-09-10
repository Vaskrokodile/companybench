"""Authoritative world state + entity registry (spec §4.2).

Every object: immutable ID, schema version, effective time, observation
visibility, creation event, revision history. Contracts carry parties, signers,
effective dates, conditions precedent, cash schedules, obligations, remedies,
termination rules.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    id: str
    kind: str
    schema_version: str = "1.0"
    effective_at: str = ""
    visibility: str = "company_authorized"
    created_by_event: str = ""
    revision: int = 1
    history: list = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def bump(self, event_id: str, patch: dict) -> None:
        self.history.append({"revision": self.revision, "data": copy.deepcopy(self.data), "event": event_id})
        self.data.update(patch)
        self.revision += 1


class Registry:
    def __init__(self) -> None:
        self._items: dict[str, Entity] = {}
        self._counters: dict[str, int] = {}

    def new_id(self, prefix: str) -> str:
        self._counters[prefix] = self._counters.get(prefix, 0) + 1
        return f"{prefix}_{self._counters[prefix]:04d}"

    def put(self, e: Entity) -> Entity:
        self._items[e.id] = e
        return e

    def get(self, eid: str) -> Entity | None:
        return self._items.get(eid)

    def by_kind(self, kind: str) -> list[Entity]:
        return [e for e in self._items.values() if e.kind == kind]

    def snapshot(self) -> dict:
        return {k: {"kind": v.kind, "revision": v.revision, "data": copy.deepcopy(v.data)} for k, v in self._items.items()}


@dataclass
class WorldState:
    """Authoritative S[t] groups (spec §4.2)."""
    state_version: int = 1
    rules_version: str = "meridian_v1"
    spec_version: str = "0.1.0"
    registry: Registry = field(default_factory=Registry)

    def bump(self) -> int:
        self.state_version += 1
        return self.state_version
