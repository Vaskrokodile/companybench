"""Treasury: runway, cash waterfall, distress machine (spec §9).

- Separates unrestricted / restricted / undrawn-committed / indicative /
  deposits / near-term mandatory / discretionary.
- trailing runway only when meaningful; authoritative forecast = dated waterfall
  with base/downside/severe. Undrawn credit only if draw conditions met.
- Distress states: healthy→watch→payment_shortfall→cure_period→restructuring→
  receivership→liquidation→closed. Negative equity alone ≠ death.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


DISTRESS_ORDER = ["healthy", "watch", "payment_shortfall", "cure_period",
                  "restructuring", "receivership", "liquidation", "closed"]


@dataclass
class Treasury:
    unrestricted_minor: int = 0
    restricted_minor: int = 0
    undrawn_committed_minor: int = 0
    indicative_minor: int = 0  # never counts as cash
    customer_deposits_minor: int = 0
    near_term_mandatory_minor: int = 0
    # waterfall schedule: list of (date_str, label, amount_minor signed +inflow)
    schedule: list = field(default_factory=list)
    state: str = "healthy"
    reserve_minor: int = 0
    shortfall_date: str | None = None

    def sync_from_ledger(self, ledger) -> None:
        self.unrestricted_minor = ledger.balances.get("cash_unrestricted", 0)
        self.restricted_minor = ledger.balances.get("cash_restricted", 0)

    def trailing_runway(self, last3_ocf_plus_investing: list[int]) -> str | float:
        """spec §9.2: mean of last 3 months OCF+investing; burn floored at 0."""
        if len(last3_ocf_plus_investing) < 3:
            return "insufficient_history"
        burn = -sum(last3_ocf_plus_investing[-3:]) / 3.0
        burn = max(0.0, burn)
        if burn <= 0:
            return "not_applicable_positive_or_zero_cashflow"
        return self.unrestricted_minor / burn

    def waterfall(self, opening_minor: int | None = None) -> dict:
        bal = self.unrestricted_minor if opening_minor is None else opening_minor
        rows = []
        low_date, low_bal = None, bal
        for date_s, label, amt in sorted(self.schedule):
            bal += amt
            rows.append({"date": date_s, "label": label, "flow_minor": amt, "balance_minor": bal})
            if bal < low_bal:
                low_bal, low_date = bal, date_s
        shortfall = next((r["date"] for r in rows if r["balance_minor"] < self.reserve_minor), None)
        self.shortfall_date = shortfall
        return {"rows": rows, "min_balance_minor": low_bal, "min_date": low_date,
                "shortfall_date": shortfall, "reserve_minor": self.reserve_minor}

    def add_flow(self, date_s: str, label: str, amount_minor: int) -> None:
        self.schedule.append((date_s, label, amount_minor))

    # ---- distress transitions ----
    def assess(self, missed_payment: bool = False, covenant_breach: bool = False,
               cash_negative: bool = False, restructured: bool = False,
               receiver_appointed: bool = False, liquidated: bool = False,
               cured: bool = False) -> str:
        cur = self.state
        if liquidated:
            self.state = "liquidation"
        elif receiver_appointed and cur not in ("liquidation", "closed"):
            self.state = "receivership"
        elif restructured and cur in ("healthy", "watch", "payment_shortfall", "cure_period"):
            self.state = "restructuring"
        elif cash_negative or missed_payment:
            if cur in ("healthy", "watch"):
                self.state = "payment_shortfall"
            elif cur == "payment_shortfall":
                self.state = "cure_period"
        elif covenant_breach and cur == "healthy":
            self.state = "watch"
        if cured and self.state in ("watch", "payment_shortfall", "cure_period"):
            self.state = "healthy"
        return self.state

    def usable_cash_after(self, burn_per_month_minor: int, months: float, installment_minor: int = 0) -> int:
        """Worked §9.3 helper: usable = unrestricted - burn*months - installment."""
        return int(self.unrestricted_minor - burn_per_month_minor * months - installment_minor)
