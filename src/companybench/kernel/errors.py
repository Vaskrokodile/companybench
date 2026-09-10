"""Error codes + typed exceptions (spec §22.5)."""
from __future__ import annotations


class ToolError(Exception):
    def __init__(self, code: str, message: str, retryable: bool = False) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.retryable = retryable


CODES = {
    "INVALID_ARGUMENT",
    "STALE_REVISION",
    "INSUFFICIENT_AUTHORITY",
    "CAPACITY_UNAVAILABLE",
    "DEADLINE_PASSED",
    "COUNTERPARTY_REJECTED",
    "CONDITIONS_NOT_MET",
    "UNSUPPORTED_PRIMITIVE",
    "BUDGET_EXHAUSTED",
}


def err(code: str, message: str, retryable: bool = False) -> ToolError:
    assert code in CODES, code
    return ToolError(code, message, retryable)
