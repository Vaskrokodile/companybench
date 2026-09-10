"""Reference agent harness (spec §5.3, §23, §37): budgets, context tier, retries.

Core Standard: 4M gen / 40M input / 40k tools; window 32 calls + 24k gen.
Opening extra window costs attention + ≥1 sim hour. Deterministic retrieval.
Same capped retry for all submissions; state unchanged until accepted.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..kernel.clock import TIER_BUDGETS, InferenceBudget


@dataclass
class HarnessConfig:
    tier: str = "core_standard"
    scaffold_hash: str = "reference_v1"
    context_input_limit: int = 64_000
    workspace_mib: int = 256
    max_retries: int = 3


def budget_for(tier: str) -> InferenceBudget:
    b = TIER_BUDGETS[tier]
    return InferenceBudget(gen_limit=b["gen_limit"], input_limit=b["input_limit"],
                           tool_limit=b["tool_limit"])
