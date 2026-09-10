"""Simulation clocks (spec §5.1-§5.2).

Four clocks kept separate:
- simulation_time: company calendar (UTC, fictional 2031+)
- executive attention: 40h/week founding CEO budget, reserved per activity
- agent execution: model/tool latency accounting (inference budget)
- evaluation elapsed: wall-clock experiment time (infra pauses excluded)

Event-driven: daily financial/org resolution, hourly electricity, event-time
contracts. Executive review at least every 7 simulated days; agent may schedule
earlier review or call world.advance with interrupt conditions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


def utc(y: int, m: int, d: int, hh: int = 0, mm: int = 0) -> datetime:
    return datetime(y, m, d, hh, mm, tzinfo=timezone.utc)


@dataclass
class AttentionLedger:
    hours_per_week: float = 40.0
    used_this_week: float = 0.0
    week_start: datetime = field(default_factory=lambda: utc(2031, 1, 1))

    def reset_if_new_week(self, now: datetime) -> None:
        if (now - self.week_start).days >= 7:
            weeks = (now - self.week_start).days // 7
            self.week_start = self.week_start + timedelta(days=7 * weeks)
            self.used_this_week = 0.0

    def reserve(self, now: datetime, hours: float) -> bool:
        self.reset_if_new_week(now)
        if self.used_this_week + hours <= self.hours_per_week + 1e-9:
            self.used_this_week += hours
            return True
        return False

    @property
    def remaining(self) -> float:
        return max(0.0, self.hours_per_week - self.used_this_week)


@dataclass
class InferenceBudget:
    gen_limit: int = 4_000_000
    input_limit: int = 40_000_000
    tool_limit: int = 40_000
    per_window_tools: int = 32
    per_window_gen: int = 24_000
    gen_used: int = 0
    input_used: int = 0
    tools_used: int = 0

    def consume_window(self, gen_tokens: int, input_tokens: int, tool_calls: int) -> tuple[bool, str]:
        if tool_calls > self.per_window_tools:
            return False, "BUDGET_EXHAUSTED: per-window tool calls exceeded"
        if gen_tokens > self.per_window_gen:
            return False, "BUDGET_EXHAUSTED: per-window generated tokens exceeded"
        if self.gen_used + gen_tokens > self.gen_limit:
            return False, "BUDGET_EXHAUSTED: total generated tokens exhausted"
        if self.input_used + input_tokens > self.input_limit:
            return False, "BUDGET_EXHAUSTED: total input tokens exhausted"
        if self.tools_used + tool_calls > self.tool_limit:
            return False, "BUDGET_EXHAUSTED: total tool calls exhausted"
        self.gen_used += gen_tokens
        self.input_used += input_tokens
        self.tools_used += tool_calls
        return True, "ok"

    @property
    def exhausted(self) -> bool:
        return (self.gen_used >= self.gen_limit or self.input_used >= self.input_limit
                or self.tools_used >= self.tool_limit)


TIER_BUDGETS = {
    "diagnostic": dict(gen_limit=500_000, input_limit=5_000_000, tool_limit=5_000),
    "core_standard": dict(gen_limit=4_000_000, input_limit=40_000_000, tool_limit=40_000),
    "core_extended": dict(gen_limit=12_000_000, input_limit=120_000_000, tool_limit=120_000),
}


@dataclass
class SimClock:
    now: datetime = field(default_factory=lambda: utc(2031, 1, 1))
    horizon_months: int = 60
    attention: AttentionLedger = field(default_factory=AttentionLedger)
    inference: InferenceBudget = field(default_factory=InferenceBudget)
    # execution/wall accounting
    agent_latency_s: float = 0.0
    wall_elapsed_s: float = 0.0
    last_review: datetime = field(default_factory=lambda: utc(2031, 1, 1))
    max_review_gap_days: int = 7

    @property
    def horizon_date(self) -> datetime:
        y = self.now.year + 0  # computed from start below
        return self._start + timedelta(days=int(self.horizon_months * 30.4375))

    _start: datetime = field(default_factory=lambda: utc(2031, 1, 1), repr=False)

    def review_due(self) -> bool:
        return (self.now - self.last_review).days >= self.max_review_gap_days

    def advance(self, to: datetime) -> None:
        if to < self.now:
            raise ValueError("clock cannot go backwards")
        self.now = to
