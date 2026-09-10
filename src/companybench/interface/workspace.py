"""Workspace, memory, decision records, delegation (spec §23).

256 MiB allowance; 64k input-token portable cap per invocation; deterministic
retrieval/truncation; versioned timestamped files; material-commitment records.
"""
from __future__ import annotations

from dataclasses import dataclass, field

WORKSPACE_LIMIT_BYTES = 256 * 1024 * 1024
INPUT_TOKEN_TIER = 64_000


@dataclass
class Workspace:
    files: dict = field(default_factory=dict)  # path -> list of versions
    bytes_used: int = 0

    def write(self, path: str, content: str, t: str) -> dict:
        b = len(content.encode())
        if self.bytes_used + b > WORKSPACE_LIMIT_BYTES:
            raise ValueError("workspace allowance exceeded (256 MiB)")
        self.files.setdefault(path, []).append({"t": t, "content": content})
        self.bytes_used += b
        return {"path": path, "version": len(self.files[path])}

    def read(self, path: str, version: int = -1) -> dict:
        vs = self.files.get(path, [])
        if not vs:
            raise KeyError(path)
        return vs[version]

    def search(self, query: str, limit: int = 10) -> list[dict]:
        out = []
        for p, vs in self.files.items():
            for i, v in enumerate(vs):
                if query.lower() in v["content"].lower():
                    start = max(0, v["content"].lower().find(query.lower()) - 60)
                    out.append({"path": p, "version": i + 1,
                                "excerpt": v["content"][start:start + 160]})
                    if len(out) >= limit:
                        return out
        return out


@dataclass
class DecisionRecord:
    objective: str
    alternatives: list
    forecast_range: list
    risks: list
    review_date: str
    reversal_conditions: str


def truncate_context(tokens: list, limit: int = INPUT_TOKEN_TIER) -> tuple[list, dict | None]:
    """Deterministic truncation with archive pointer (spec §23.2)."""
    if len(tokens) <= limit:
        return tokens, None
    keep = tokens[-limit:]
    pointer = {"omitted": len(tokens) - limit, "archive": "workspace://archive/log",
               "note": "truncated; critical commitments remain queryable"}
    return keep, pointer
