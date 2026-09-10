"""Electricity sector (spec §17): Northline — calibrated.

Loss rate, scarcity proxy, and gas availability from params_v1.0.
Reduced 3-zone model limits disclosed per §36.6.
"""
from __future__ import annotations

from dataclasses import dataclass, field

try:
    from ...calibration.registry import get as _get
    LOSS_RATE = float(_get("energy.loss_rate"))
    SCARCITY_PRICE = float(_get("energy.scarcity_price_mcu"))
    GAS_AVAIL = float(_get("energy.generator_avail_gas"))
except Exception:
    LOSS_RATE = 0.031
    SCARCITY_PRICE = 350.0
    GAS_AVAIL = 0.94

ZONES = ["north", "central", "south"]
HOURS_PER_YEAR = 8760
TRANSFER = {("north", "central"): 400.0, ("central", "south"): 500.0, ("north", "south"): 150.0}


@dataclass
class Generator:
    id: str
    zone: str
    cap_mw: float
    fuel_mcu_per_mwh: float
    startup_mcu: float = 5_000.0
    min_mw: float = 0.0
    ramp_mw_per_h: float = 1e9
    avail: float = 0.95
    renewable: bool = False
    out_mw: float = 0.0


@dataclass
class Storage:
    id: str
    zone: str
    power_mw: float
    energy_mwh: float
    soc_mwh: float = 0.0
    ch_eff: float = 0.92
    dis_eff: float = 0.92
    degraded_pct: float = 0.0

    def usable_cap(self) -> float:
        return self.energy_mwh * (1 - self.degraded_pct / 100.0)

    def step(self, ch_mw: float, dis_mw: float, dt_h: float = 1.0) -> dict:
        if ch_mw > 0 and dis_mw > 0:
            raise ValueError("simultaneous charge/discharge disallowed")
        ch_mw = min(max(ch_mw, 0.0), self.power_mw)
        dis_mw = min(max(dis_mw, 0.0), self.power_mw)
        cap = self.usable_cap()
        ch_e = ch_mw * dt_h * self.ch_eff
        dis_e = dis_mw * dt_h / self.dis_eff
        if self.soc_mwh + ch_e - dis_e < -1e-9 or self.soc_mwh + ch_e - dis_e > cap + 1e-9:
            ch_e = min(ch_e, cap - self.soc_mwh)
            dis_e = min(dis_e, self.soc_mwh)
        self.soc_mwh = min(cap, max(0.0, self.soc_mwh + ch_e - dis_e))
        return {"soc": self.soc_mwh, "charged": ch_e, "discharged": dis_e}


@dataclass
class Load:
    id: str
    zone: str
    peak_mw: float
    shape: list = field(default_factory=list)
    growth_pct: float = 0.0
    price_mcu_per_mwh: float = 95.0
    flexible_pct: float = 0.0

    def hourly_mw(self, h: int, weather_mult: float = 1.0) -> float:
        f = self.shape[h % 24] if self.shape else 0.7
        # losses applied on delivery side (reduced-model proxy)
        return self.peak_mw * f * weather_mult * (1 + LOSS_RATE)


def default_daily_shape(peaky: bool = False) -> list[float]:
    base = [0.55, 0.5, 0.48, 0.47, 0.5, 0.58, 0.7, 0.8, 0.85, 0.88, 0.9, 0.92,
            0.93, 0.92, 0.9, 0.88, 0.9, 0.95, 1.0, 0.97, 0.9, 0.8, 0.7, 0.6]
    if peaky:
        base[18] = 1.15
    return base


def dispatch_hour(gens: list[Generator], demand_mw: float, rng_u: list[float] | None = None) -> dict:
    avail_gens = []
    for i, g in enumerate(gens):
        u = rng_u[i] if rng_u else 0.99
        # calibrated gas availability overrides default where fuel matches
        eff_avail = GAS_AVAIL if ("gas" in g.id.lower() or g.fuel_mcu_per_mwh > 40) and not g.renewable else g.avail
        a = g.cap_mw if u < eff_avail else 0.0
        if g.renewable:
            a *= 0.4 + 0.6 * (rng_u[i] if rng_u else 0.5)
        avail_gens.append((g.fuel_mcu_per_mwh, a, g))
    avail_gens.sort(key=lambda x: x[0])
    served, cost, used = 0.0, 0.0, []
    rem = demand_mw
    for price, a, g in avail_gens:
        take = min(a, rem)
        served += take
        cost += take * price
        rem -= take
        used.append((g.id, take))
        if rem <= 1e-9:
            break
    unserved = max(0.0, demand_mw - served)
    clearing = max([p for p, a, g in avail_gens if a > 0], default=0.0)
    if unserved > 0:
        clearing = max(clearing, SCARCITY_PRICE)
    return {"served": served, "unserved": unserved, "cost": cost, "price": clearing, "mix": used}


def credit_call(min_support: float, current_exposure: float, stressed_future: float,
                unsecured_limit: float, posted: float) -> dict:
    req = max(min_support, max(0.0, current_exposure) + stressed_future - unsecured_limit)
    call = max(0.0, req - posted)
    return {"required": req, "call": call}


@dataclass
class PPA:
    id: str
    zone: str
    shape: str
    volume_mwh_year: float
    price_mcu_per_mwh: float
    term_years: int
    escalator: float = 0.0
    balancing: str = "supplier"
    credit_support_mcu: float = 0.0

    def annual_revenue(self, delivered_mwh: float, spot_avg: float = 0.0) -> float:
        if self.shape == "cfd_financial":
            return (self.price_mcu_per_mwh - spot_avg) * min(delivered_mwh, self.volume_mwh_year)
        return self.price_mcu_per_mwh * min(delivered_mwh, self.volume_mwh_year)


DEV_GATES = ["site", "resource_study", "environmental", "permit", "interconnection",
             "offtake", "financing", "procurement", "construction", "commissioning", "operation"]


@dataclass
class DevProject:
    id: str
    kind: str
    mw: float
    gate: str = "site"
    spent_mcu: float = 0.0
    capex_mcu: float = 0.0
    connection_approved: bool = False
    permitted: bool = False
    financed: bool = False
    months_at_gate: int = 0

    def advance(self, ok: bool) -> str:
        if ok:
            i = DEV_GATES.index(self.gate)
            self.gate = DEV_GATES[min(len(DEV_GATES) - 1, i + 1)]
            self.months_at_gate = 0
        else:
            self.months_at_gate += 1
        return self.gate


PROJECT_MENU = {
    "operating_solar_buy": {"months": (3, 9), "bottleneck": "diligence/financing/condition/contracted revenue"},
    "new_solar": {"months": (18, 48), "bottleneck": "interconnection/permitting/equipment/financing"},
    "battery": {"months": (12, 36), "bottleneck": "connection/safety/revenue durability"},
    "efficiency_dr": {"months": (3, 12), "bottleneck": "enrollment/controls/measurement"},
    "dispatchable": {"months": (36, 84), "bottleneck": "permits/fuel+network/construction+financing"},
    "nuclear": {"months": (120, 240), "bottleneck": "beyond Core in ordinary scenarios"},
}


@dataclass
class PowerState:
    generators: dict = field(default_factory=dict)
    storages: dict = field(default_factory=dict)
    loads: dict = field(default_factory=dict)
    ppas: dict = field(default_factory=dict)
    dev_projects: dict = field(default_factory=dict)
    delivered_mwh: float = 0.0
    unserved_mwh: float = 0.0
    collateral_posted_mcu: float = 0.0
    # v1.1: real build/load levers — generators energize after a lead time,
    # contracted loads ramp toward their signed peak.
    pending_gens: list = field(default_factory=list)   # [{gen: Generator, active_day: int}]
    load_ramps: dict = field(default_factory=dict)      # {load_id: target_peak_mw}


# v1.1: build menu — kind -> (lead_days, capex_mcu_per_mw, fuel_mcu_per_mwh, renewable)
BUILD_MENU = {
    "solar": (300, 35_000.0, 0.0, True),
    "wind": (270, 40_000.0, 0.0, True),
    "gas": (210, 45_000.0, 55.0, False),
    "battery": (120, 40_000.0, 0.0, False),  # modeled as 4h-duration gas-free peaker
}
