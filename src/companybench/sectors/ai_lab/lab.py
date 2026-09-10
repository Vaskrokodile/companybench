"""AI laboratory sector (spec §15): Aster Research — calibrated."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

try:
    from ...calibration.registry import get as _get
    _MFU = float(_get("ai.mfu_default"))
    _SAT = float(_get("ai.saturation"))
    _SCALE = float(_get("ai.scale_eff_256"))
except Exception:
    _MFU, _SAT, _SCALE = 0.40, 2.5, 0.88


def training_flops_estimate(params: int, tokens: int) -> float:
    return 6.0 * params * tokens


def elapsed_training_s(flops: float, sustained_flops_per_s: float) -> float:
    return flops / sustained_flops_per_s if sustained_flops_per_s > 0 else float("inf")


def worked_example() -> dict:
    flops = training_flops_estimate(7_000_000_000, 200_000_000_000)
    per_acc = 2.0e14
    elapsed = elapsed_training_s(flops, 256 * per_acc)
    return {"flops": flops, "elapsed_s": elapsed, "elapsed_h": elapsed / 3600.0,
            "rental_mcu": 256 * (elapsed / 3600.0) * 3.0}


@dataclass
class HardwareType:
    id: str
    peak_tflops: float
    mem_gb: float
    mfu: float
    scale_eff: float
    price_mcu_per_hour: float
    lead_days: int = 14
    fail_per_1k_h: float = 0.5
    power_kw: float = 1.0

    def sustained_flops(self) -> float:
        return self.peak_tflops * 1e12 * self.mfu * self.scale_eff


DEFAULT_HARDWARE = {
    "a100_80gb": HardwareType("a100_80gb", 312, 80, _MFU, _SCALE, 3.0),
    "h100_80gb": HardwareType("h100_80gb", 989, 80, _MFU, _SCALE, 5.5),
    "b200": HardwareType("b200", 2250, 192, _MFU - 0.02, _SCALE - 0.03, 9.0, lead_days=60),
}


@dataclass
class ResearchSurface:
    w_compute: float = 0.35
    w_data: float = 0.30
    w_method: float = 0.20
    w_team: float = 0.15
    bottleneck: str = "data"
    innovation_prob: float = 0.04
    innovation_boost: float = 0.08
    saturation: float = _SAT

    def outcome(self, log_compute: float, data_q: float, method_q: float, team_q: float, rng_u: float) -> float:
        x = (self.w_compute * log_compute + self.w_data * data_q
             + self.w_method * method_q + self.w_team * team_q)
        y = self.saturation * (1 - math.exp(-x / self.saturation))
        if self.bottleneck == "data":
            y = min(y, 0.4 + 0.9 * data_q)
        elif self.bottleneck == "compute":
            y = min(y, 0.3 + 0.9 * min(1.0, log_compute / 3.0))
        if rng_u < self.innovation_prob:
            y = min(self.saturation, y + self.innovation_boost)
        return y


EVAL_DIMS = ["domain", "reasoning", "factuality", "tool_use", "robustness",
             "safety", "latency", "memory", "cost"]


@dataclass
class ModelAsset:
    id: str
    family: str
    params: int
    tokens: int
    data_rights_ok: bool = False
    eval_vector: dict = field(default_factory=dict)
    serving_profile: dict = field(default_factory=dict)
    released: bool = False
    limitations: list = field(default_factory=list)


@dataclass
class Dataset:
    id: str
    volume_tokens: int
    quality: float
    permitted_uses: list = field(default_factory=list)
    price_mcu: float = 0.0
    lead_days: int = 30
    contamination_risk: float = 0.05


def serving_contribution(billed_in_units: float, in_price: float, billed_out_units: float,
                         out_price: float, credits: float, refunds: float,
                         compute: float, network: float, storage: float, support: float) -> dict:
    net_rev = billed_in_units * in_price + billed_out_units * out_price - credits - refunds
    contrib = net_rev - compute - network - storage - support
    return {"net_api_revenue": net_rev, "serving_contribution": contrib}


@dataclass
class LabState:
    models: dict = field(default_factory=dict)
    datasets: dict = field(default_factory=dict)
    surfaces: dict = field(default_factory=dict)
    compute_reserved_hours: dict = field(default_factory=dict)
    compute_used_hours: dict = field(default_factory=dict)
    eval_history: list = field(default_factory=list)
    pilots: list = field(default_factory=list)
    serving: dict = field(default_factory=lambda: {"in_units": 0.0, "out_units": 0.0, "contrib_mcu": 0.0})

    def ensure_surface(self, family: str, rng, seed_s: str) -> ResearchSurface:
        if family not in self.surfaces:
            u = rng.uniform("ai_research", family, seed_s, "surface", 0)
            bott = "data" if u < 0.4 else ("compute" if u < 0.7 else "method")
            self.surfaces[family] = ResearchSurface(bottleneck=bott)
        return self.surfaces[family]

    def run_experiment(self, family: str, log_compute: float, data_q: float, method_q: float,
                       team_q: float, rng, sim_time_s: str) -> dict:
        surf = self.ensure_surface(family, rng, sim_time_s)
        u = rng.uniform("ai_research", family, sim_time_s, "outcome", len(self.eval_history))
        gain = surf.outcome(log_compute, data_q, method_q, team_q, u)
        self.eval_history.append({"family": family, "gain": gain, "t": sim_time_s})
        return {"capability_gain": gain, "bottleneck": surf.bottleneck,
                "knowledge": True, "n": len(self.eval_history)}

    def heldout_eval(self, claimed_gain: float, rng, sim_time_s: str, overfit: float = 0.0) -> dict:
        u = rng.uniform("ai_research", "heldout", sim_time_s, "heldout", 0)
        true_gain = max(0.0, claimed_gain - overfit * (0.5 + u))
        passed = true_gain > 0.15
        return {"true_gain": round(true_gain, 4), "passed": passed,
                "ci": [round(max(0, true_gain - 0.05), 4), round(true_gain + 0.05, 4)]}
