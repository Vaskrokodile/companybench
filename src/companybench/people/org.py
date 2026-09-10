"""Employees & organization (spec §11) — calibrated.

Overhead, ramp, competing-offer, and turnover now sourced from
calibration/params_v1.0.json (frozen). Hard-coded fallbacks only for import
isolation; engine path uses registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field

try:
    from ..calibration.registry import get as _get
    OVERHEAD_RATE = float(_get("labor.overhead_rate"))
    RAMP_GENERAL_W = int(_get("labor.ramp_general_weeks"))
    RAMP_SCARCE_W = int(_get("labor.ramp_scarce_weeks"))
    COMPETING_GENERAL = float(_get("labor.competing_offer_general"))
    COMPETING_SCARCE = float(_get("labor.competing_offer_scarce"))
    TURNOVER_ANNUAL = float(_get("labor.voluntary_turnover_annual"))
except Exception:
    OVERHEAD_RATE = 0.25
    RAMP_GENERAL_W = 5
    RAMP_SCARCE_W = 11
    COMPETING_GENERAL = 0.20
    COMPETING_SCARCE = 0.35
    TURNOVER_ANNUAL = 0.13

ROLE_BASELINES = {
    "researcher": {"salary_mcu": 180_000, "skill": {"research": 1.0}},
    "ml_engineer": {"salary_mcu": 170_000, "skill": {"systems": 1.0}},
    "engineer": {"salary_mcu": 140_000, "skill": {"engineering": 1.0}},
    "product": {"salary_mcu": 150_000, "skill": {"product": 1.0}},
    "commercial": {"salary_mcu": 130_000, "skill": {"sales": 1.0}},
    "operations": {"salary_mcu": 110_000, "skill": {"ops": 1.0}},
    "trader": {"salary_mcu": 160_000, "skill": {"trading": 1.0}},
    "grid_engineer": {"salary_mcu": 150_000, "skill": {"grid": 1.0}},
    "finance": {"salary_mcu": 140_000, "skill": {"finance": 1.0}},
    "compliance": {"salary_mcu": 120_000, "skill": {"compliance": 1.0}},
}


@dataclass
class Employee:
    id: str
    role: str
    salary_mcu: float
    skills: dict = field(default_factory=dict)
    start_day: int = 0
    notice_days: int = 30
    team: str = "general"
    manager: str | None = None
    ramp_weeks: int = 8
    workload: float = 0.8  # 1.0 = full
    morale: float = 0.7
    retention_risk: float = 0.05
    active: bool = True
    equity_grant: int = 0
    weeks_worked: float = 0.0
    burnout: float = 0.0

    def ramp_factor(self, today_day: int) -> float:
        w = max(0.0, (today_day - self.start_day) / 7.0)
        if self.ramp_weeks <= 0:
            return 1.0
        return min(1.0, 0.35 + 0.65 * (w / self.ramp_weeks))

    def cash_cost_monthly_minor(self) -> int:
        base = self.salary_mcu / 12.0
        return int(round((base * (1 + OVERHEAD_RATE)) * 100))

    def effective_hours(self, today_day: int, scheduled: float = 160.0,
                        availability: float = 1.0, skill_match: float = 1.0,
                        coordination: float = 1.0) -> float:
        skill_match = min(max(skill_match, 0.0), 1.25)  # bounded upside
        return scheduled * self.ramp_factor(today_day) * availability * skill_match * coordination


@dataclass
class Candidate:
    id: str
    role: str
    salary_ask_mcu: float
    true_quality: float  # hidden 0..1
    resume_signal: float  # noisy visible
    notice_weeks: int = 4
    competing_offer_prob: float = 0.25
    state: str = "sourced"  # sourced→screened→interviewed→offered→accepted/declined/lost


class Org:
    def __init__(self) -> None:
        self.staff: dict[str, Employee] = {}
        self.candidates: dict[str, Candidate] = {}
        self.roles_open: dict[str, dict] = {}
        self._eseq = 0
        self._cseq = 0
        self.mgmt_span_warn = 8

    # ---- hiring pipeline ----
    def open_role(self, role: str, band_mcu: tuple[float, float], team: str = "general",
                  scarce: bool = False) -> str:
        rid = f"role_{role}_{len(self.roles_open)+1}"
        self.roles_open[rid] = {"role": role, "band": band_mcu, "team": team,
                                "scarce": scarce, "applicants": []}
        return rid

    def source(self, role_id: str, rng, sim_day: int, sim_time_s: str, n: int = 3) -> list[str]:
        spec = self.roles_open[role_id]
        ids = []
        for i in range(n):
            self._cseq += 1
            cid = f"candidate_{self._cseq:03d}"
            q = rng.uniform("people", cid, sim_time_s, "quality", i)
            noise = rng.normal("people", cid, sim_time_s, "resume_noise", i) * 0.12
            ask = (spec["band"][0] + spec["band"][1]) / 2 * (0.9 + 0.2 * q)
            scarce = spec["scarce"]
            # calibrated lead-time proxy via notice weeks; engine-level MF
            notice = rng.randint(6, 20, "people", cid, sim_time_s, "notice", i) if scarce else rng.randint(2, 8, "people", cid, sim_time_s, "notice", i)
            # calibrated competing-offer rates
            comp = COMPETING_SCARCE if scarce else COMPETING_GENERAL
            c = Candidate(cid, spec["role"], ask, q, min(1, max(0, q + noise)), notice, comp)
            self.candidates[cid] = c
            spec["applicants"].append(cid)
            ids.append(cid)
        return ids

    def interview(self, cid: str) -> dict:
        c = self.candidates[cid]
        c.state = "interviewed"
        return {"candidate": cid, "resume_signal": round(c.resume_signal, 2),
                "ask_mcu": round(c.salary_ask_mcu), "notice_weeks": c.notice_weeks}

    def offer(self, cid: str, salary_mcu: float, rng, sim_time_s: str, team: str = "general") -> dict:
        c = self.candidates[cid]
        c.state = "offered"
        accept_p = 0.75 if salary_mcu >= c.salary_ask_mcu * 0.97 else 0.35
        accepted = rng.bernoulli(accept_p, "people", cid, sim_time_s, "accept", 0)
        lost = (not accepted) or rng.bernoulli(c.competing_offer_prob, "people", cid, sim_time_s, "compete", 1)
        if accepted and not lost:
            c.state = "accepted"
            self._eseq += 1
            eid = f"employee_{self._eseq:03d}"
            base = ROLE_BASELINES.get(c.role, {"salary_mcu": salary_mcu, "skill": {c.role: 0.8}})
            ramp = RAMP_SCARCE_W if c.notice_weeks > 6 else RAMP_GENERAL_W
            e = Employee(eid, c.role, salary_mcu, dict(base.get("skill", {})), 0,
                         notice_days=30, team=team, ramp_weeks=ramp)
            e.skills["general"] = c.true_quality
            # calibrated base turnover drives retention_risk
            e.retention_risk = TURNOVER_ANNUAL / 3.0  # spread via burnout/workload in step_month
            self.staff[eid] = e
            return {"accepted": True, "employee_id": eid, "start_delay_weeks": c.notice_weeks}
        c.state = "lost" if lost else "declined"
        return {"accepted": False, "state": c.state}

    # ---- capacity / management ----
    def team_capacity(self, today_day: int, team: str | None = None, skill: str | None = None) -> float:
        tot = 0.0
        for e in self.staff.values():
            if not e.active:
                continue
            if team and e.team != team:
                continue
            sm = e.skills.get(skill, 0.7) if skill else 0.85
            tot += e.effective_hours(today_day, skill_match=sm + 0.15)
        managers = sum(1 for e in self.staff.values() if e.active and ("lead" in e.role or e.manager is None))
        span = len([e for e in self.staff.values() if e.active]) / max(1, max(1, managers))
        coord = 1.0 if span <= self.mgmt_span_warn else max(0.6, 1.0 - 0.03 * (span - self.mgmt_span_warn))
        return tot * coord

    def payroll_monthly_minor(self) -> int:
        return sum(e.cash_cost_monthly_minor() for e in self.staff.values() if e.active)

    def headcount(self) -> dict:
        act = [e for e in self.staff.values() if e.active]
        return {"active": len(act), "fte": round(sum(e.workload for e in act), 2)}

    def step_month(self, rng, sim_time_s: str, workload_avg: float = 0.85) -> dict:
        """Turnover, burnout with lag, morale drift — calibrated turnover base."""
        left, burned = [], 0
        for e in list(self.staff.values()):
            if not e.active:
                continue
            e.weeks_worked += 4.3
            e.burnout = 0.9 * e.burnout + 0.1 * max(0.0, e.workload - 0.9) * 2.0
            if e.burnout > 0.5:
                burned += 1
            # monthly hazard derived from annual: p_month = 1-(1-annual)^(1/12)
            p_month_base = 1 - (1 - TURNOVER_ANNUAL) ** (1 / 12)
            p_leave = p_month_base * (1 + e.burnout) * (0.7 + 0.6 * workload_avg) * (e.retention_risk / (TURNOVER_ANNUAL / 3) if TURNOVER_ANNUAL else 1)
            if rng.bernoulli(min(0.2, p_leave), "people", e.id, sim_time_s, "attrition", 0):
                e.active = False
                left.append(e.id)
        return {"left": left, "burned_out": burned}
