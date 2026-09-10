"""Projects, vendors/procurement, risk/insurance (spec §13).

Dependency graphs with acceptance tests; tech debt w/ location+mechanism;
vendors with quotes/stock/lead-time/reliability; PO→delivery→invoice→payment
separation; risk controls tied to hazard pathways; insurance with exclusions.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    skill: str
    estimate_h: float
    remaining_h: float
    preds: list = field(default_factory=list)
    done: bool = False
    acceptance: str = ""


@dataclass
class Project:
    id: str
    kind: str  # research|product|infra|sales_impl|regulatory|org_change|energy_dev
    objective: str
    tasks: dict = field(default_factory=dict)
    budget_minor: int = 0
    spent_minor: int = 0
    status: str = "proposed"  # proposed→authorized→active→blocked→done|cancelled
    artifacts: list = field(default_factory=list)
    debt_entries: list = field(default_factory=list)
    maintenance_h_per_month: float = 0.0

    def add_task(self, t: Task) -> None:
        self.tasks[t.id] = t

    def ready(self, tid: str) -> bool:
        return all(self.tasks[p].done for p in self.tasks[tid].preds)

    def apply_work(self, hours_by_skill: dict[str, float]) -> float:
        """Returns accepted effective hours; dependency-constrained (no speedup by unrelated staff)."""
        accepted = 0.0
        for t in self.tasks.values():
            if t.done or not self.ready(t.id):
                continue
            avail = hours_by_skill.get(t.skill, 0.0)
            if avail <= 0:
                continue
            w = min(t.remaining_h, avail)
            t.remaining_h -= w
            hours_by_skill[t.skill] = avail - w
            accepted += w
            if t.remaining_h <= 1e-9:
                t.done = True
        return accepted

    @property
    def complete(self) -> bool:
        return bool(self.tasks) and all(t.done for t in self.tasks.values())

    def add_debt(self, where: str, mechanism: str, future_cost_h: float) -> None:
        self.debt_entries.append({"where": where, "mechanism": mechanism, "future_h": future_cost_h})


@dataclass
class VendorOffer:
    id: str
    vendor: str
    unit_price_minor: int
    lead_days: int
    reliability: float
    min_qty: int = 1
    cancellable: bool = True
    cancel_fee_minor: int = 0


class Procurement:
    def __init__(self) -> None:
        self.offers: dict[str, VendorOffer] = {}
        self.orders: dict[str, dict] = {}
        self._seq = 0

    def quote(self, vendor: str, unit_price_mcu: float, lead_days: int, reliability: float,
              min_qty: int = 1, cancel_fee_mcu: float = 0.0) -> str:
        self._seq += 1
        oid = f"quote_{self._seq:03d}"
        self.offers[oid] = VendorOffer(oid, vendor, int(unit_price_mcu * 100), lead_days,
                                       reliability, min_qty, True, int(cancel_fee_mcu * 100))
        return oid

    def order(self, quote_id: str, qty: int, order_day: int) -> str:
        q = self.offers[quote_id]
        if qty < q.min_qty:
            raise ValueError("below minimum")
        oid = f"po_{len(self.orders)+1:03d}"
        self.orders[oid] = {"quote": quote_id, "qty": qty, "ordered_day": order_day,
                            "due_day": order_day + q.lead_days, "delivered": False,
                            "amount_minor": q.unit_price_minor * qty}
        return oid


@dataclass
class RiskControl:
    id: str
    hazard: str
    reduction: float  # multiplies hazard rate
    cost_minor: int
    implemented: bool = False


@dataclass
class Insurance:
    id: str
    premium_minor_per_month: int
    deductible_minor: int
    limit_minor: int
    exclusions: list = field(default_factory=list)
    active: bool = True

    def claim(self, loss_minor: int, cause: str) -> int:
        if not self.active or cause in self.exclusions:
            return 0
        return max(0, min(self.limit_minor, loss_minor - self.deductible_minor))
