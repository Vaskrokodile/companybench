"""Event sourcing: immutable log + hash chain + snapshots (spec §33.3, §34.2).

Every accepted action and transition is an immutable event with causal parents.
State = deterministic projection of ordered log + versioned initial state.
Snapshots accelerate restart but are validated against replay hashes.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _digest(prev: str, canon_payload: str) -> str:
    return "sha256:" + hashlib.sha256((prev + canon_payload).encode()).hexdigest()


@dataclass
class Event:
    event_id: str
    schema_version: str
    occurred_at: str
    recorded_at: str
    event_type: str
    actor_id: str
    entity_ids: list
    causal_parent_ids: list
    payload: dict
    visibility: str
    previous_event_hash: str
    event_hash: str = ""


class EventLog:
    def __init__(self, schema_version: str = "1.0") -> None:
        self.schema_version = schema_version
        self.events: list[Event] = []
        self._prev_hash = "sha256:genesis"
        self._seq = 0

    def append(self, occurred_at: datetime, event_type: str, actor_id: str,
               entity_ids: list | None = None, causal_parent_ids: list | None = None,
               payload: dict | None = None, visibility: str = "company_authorized") -> Event:
        self._seq += 1
        eid = f"event_{self._seq:06d}"
        iso = occurred_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        body = {
            "event_id": eid, "occurred_at": iso, "event_type": event_type,
            "actor_id": actor_id, "entity_ids": entity_ids or [],
            "causal_parent_ids": causal_parent_ids or [], "payload": payload or {},
        }
        h = _digest(self._prev_hash, _canon(body))
        ev = Event(event_id=eid, schema_version=self.schema_version, occurred_at=iso,
                   recorded_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                   event_type=event_type, actor_id=actor_id, entity_ids=entity_ids or [],
                   causal_parent_ids=causal_parent_ids or [], payload=payload or {},
                   visibility=visibility, previous_event_hash=self._prev_hash, event_hash=h)
        self.events.append(ev)
        self._prev_hash = h
        return ev

    @property
    def head_hash(self) -> str:
        return self._prev_hash

    def to_dicts(self) -> list[dict]:
        return [e.__dict__ for e in self.events]

    def verify_chain(self) -> bool:
        prev = "sha256:genesis"
        for e in self.events:
            body = {"event_id": e.event_id, "occurred_at": e.occurred_at, "event_type": e.event_type,
                    "actor_id": e.actor_id, "entity_ids": e.entity_ids,
                    "causal_parent_ids": e.causal_parent_ids, "payload": e.payload}
            if e.previous_event_hash != prev:
                return False
            if e.event_hash != _digest(prev, _canon(body)):
                return False
            prev = e.event_hash
        return True


@dataclass
class Snapshot:
    state_version: int
    as_of: str
    state_hash: str
    blob: dict


def state_hash_of(obj: dict) -> str:
    return "sha256:" + hashlib.sha256(_canon(obj).encode()).hexdigest()


class SnapshotStore:
    def __init__(self) -> None:
        self.snaps: list[Snapshot] = []

    def put(self, state_version: int, as_of: str, blob: dict) -> Snapshot:
        s = Snapshot(state_version, as_of, state_hash_of(blob), copy.deepcopy(blob))
        self.snaps.append(s)
        return s
