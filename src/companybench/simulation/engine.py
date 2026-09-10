"""Master simulation engine (spec §4.3, §5, §25, §33).

8-step causal order per timestamp:
 1 exogenous/physical 2 scheduled work 3 contractual events 4 market clearing
 5 accruals/invoices/cash/collateral 6 liquidity/covenant/service/governance
 7 release observations 8 agent decision window (review ≥7d / interrupts)

Supports 60-month Core, 120-month Long Horizon, and decades (tested to 360).
Hourly electricity aggregated; daily finance/org; event-time contracts.
Termination taxonomy + 12-month runoff + replacement-policy branch.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from ..kernel.clock import SimClock, utc
from ..kernel.events import EventLog, SnapshotStore, state_hash_of
from ..kernel.rng import StableRNG
from ..calibration.registry import require_frozen as _require_frozen
from ..calibration.anchors import load as _anchors_load
from ..finance.ledger import Ledger, mcu
from ..finance.treasury import Treasury
from ..finance.funding import CapTable, Board, DebtFacility
from ..people.org import Org
from ..markets.customers import CohortLedger, Cohort, Pipeline
from ..markets.competitors import default_competitors
from ..markets.macro import MacroState
from ..projects.projects import Procurement
from ..sectors.ai_lab.lab import LabState
from ..sectors.saas.saas import SaaSState, ProductState
from ..sectors.electricity.power import PowerState, Generator, Storage, Load, default_daily_shape
from ..sectors.electricity.datacenter import DatacenterDossier
from ..scenarios.manifests import Scenario
from ..scenarios.incidents import TEMPLATES

DAY = timedelta(days=1)


@dataclass
class EpisodeResult:
    scenario_id: str
    seed: int
    months: int
    endpoint: str = "horizon_reached"
    monthly: list = field(default_factory=list)
    milestones: dict = field(default_factory=dict)
    mistakes: list = field(default_factory=list)
    costs: dict = field(default_factory=dict)
    scores: dict = field(default_factory=dict)
    head_hash: str = ""
    valid: bool = True


class Engine:
    """Deterministic episode simulator. Agent acts via `act_*` hooks or tool gateway."""

    def __init__(self, scenario: Scenario, world_seed: str | int | None = None,
                 agent_id: str = "agent_player", budget_tier: str = "core_standard") -> None:
        # Frozen calibration gate (spec §41.1): ranked runs reject uncalibrated params/anchors
        _require_frozen()
        _anchors_load()
        self.sc = scenario
        self.seed = str(world_seed if world_seed is not None else f"{scenario.id}:{scenario.seed}")
        self.rng = StableRNG(self.seed)
        self.log = EventLog()
        self.snaps = SnapshotStore()
        self.clock = SimClock(now=utc(2031, 1, 1), horizon_months=scenario.horizon_months)
        self.clock._start = utc(2031, 1, 1)
        self.agent_id = agent_id
        # finance
        self.ledger = Ledger()
        self.treasury = Treasury()
        self.cap = CapTable()
        self.board = Board()
        self.debts: list[DebtFacility] = []
        # org/markets
        self.org = Org()
        self.cohorts = CohortLedger()
        self.pipe = Pipeline()
        self.macro = MacroState()
        self.procure = Procurement()
        self.competitors = [c for c in default_competitors() if c.sector == scenario.sector]
        # sectors
        self.lab = LabState()
        self.saas = SaaSState()
        self.power = PowerState()
        self.dc = DatacenterDossier()
        # books
        self.day = 0
        self.month_idx = 0
        self.monthly_rows: list[dict] = []
        self.pending_incidents: list[dict] = []
        self.incident_log: list[dict] = []  # v1.1: scored incident record
        self._incident_cursor = 0
        self._neg_cash_months = 0  # v1.1: sustained-negative-cash insolvency path
        self.controller_active = True
        self.control_end_day: int | None = None
        self.endpoint = "horizon_reached"
        self.inbox: list[dict] = []
        self._boot()

    # ---------- boot (§41 opening) ----------
    def _boot(self) -> None:
        o = self.sc.opening
        t0 = self.clock.now.isoformat().replace("+00:00", "Z")
        self.ledger.opening(
            t0,
            {"cash_unrestricted": o["cash"] * 1000, "cash_restricted": o["restricted"] * 1000,
             "receivables": o["receivables"] * 1000, "prepayments": o["prepaid"] * 1000,
             "ppe_gross": o["equip"] * 1000, "spv_investment": o["dev_rights"] * 1000},
            {"payables": o["payables"] * 1000, "deferred_revenue": o["deferred"] * 1000,
             "debt_principal": o["debt"] * 1000},
            {"common": o["equity"] * 1000},
        )
        self.treasury.sync_from_ledger(self.ledger)
        if o["debt"]:
            self.debts.append(DebtFacility(o["debt"] * 1000 * 100, 0.07, "2036-01-01",
                                           amort_monthly_minor=mcu(30_000), min_cash_minor=mcu(200_000),
                                           min_dscr=1.2))
        self._seed_staff(o["employees"])
        if self.sc.sector == "saas":
            self.cohorts.add(Cohort("inherited", "2030-06", mcu(12_000), mcu(12_000), 30))
            self.saas.product.shipped.update({"core_workflow": 2, "collaboration": 1, "reporting": 1})
        elif self.sc.sector == "ai_lab":
            self.lab.compute_reserved_hours = {"a100_80gb": 20_000}
            self.lab.datasets["web_mix"] = {"quality": 0.55, "licensed": False}
        elif self.sc.sector == "electricity":
            self.power.generators["solar_a"] = Generator("solar_a", "north", 40, 8.0, renewable=True)
            self.power.generators["gas_b"] = Generator("gas_b", "central", 120, 55.0)
            self.power.storages["batt_1"] = Storage("batt_1", "north", 25, 100, 50)
            self.power.loads["book"] = Load("book", "north", 28, default_daily_shape(), 0.02, 95.0)
            self.power.loads["dc_prospect"] = Load("dc_prospect", "north", 0, default_daily_shape(True), 0.0, 85.0)
            self.treasury.restricted_minor = mcu(o["restricted"] * 1000)
        self.log.append(self.clock.now, "episode.open", "evaluator", [self.sc.id],
                        [], {"sector": self.sc.sector, "family": self.sc.family, "seed": self.seed})
        self.inbox.append({"t": t0, "kind": "handover",
                           "text": f"Executive handover: {self.sc.sector} dossier, opening equity "
                                   f"{o['equity']}k MCU, team {o['employees']}, family {self.sc.family}."})

    def _seed_staff(self, n: int) -> None:
        from ..people.org import Employee, ROLE_BASELINES
        roles = {"ai_lab": ["researcher"] * 4 + ["ml_engineer"] * 3 + ["product", "commercial", "operations"] * 1 + ["researcher"],
                 "saas": ["engineer"] * 3 + ["product", "commercial"],
                 "electricity": ["trader"] * 3 + ["grid_engineer"] * 3 + ["commercial"] * 2 + ["operations"] * 2 + ["finance", "compliance", "commercial"]}
        for i, r in enumerate(roles[self.sc.sector][:n]):
            base = ROLE_BASELINES.get(r, {"salary_mcu": 130_000, "skill": {r: 0.8}})
            e = Employee(f"employee_{i+1:03d}", r, base["salary_mcu"], dict(base.get("skill", {})),
                         start_day=-90, team="core", ramp_weeks=2)
            e.weeks_worked = 12
            self.org.staff[e.id] = e
        self.org._eseq = n

    # ---------- 8-step causal order ----------
    def step_day(self) -> dict:
        now = self.clock.now
        t = now.isoformat().replace("+00:00", "Z")
        obs: dict[str, Any] = {"date": t}
        # 1. exogenous + physical availability
        regime = self.macro.regime
        if self.day % 30 == 0 and self.day > 0:
            regime = self.macro.step(self.rng, t)
        eff = self.macro.effects()
        self._maybe_trigger_incident(t, eff)
        # 2. scheduled work (projects tick via policy hook; default maintenance)
        # 3. contractual events due (debt service monthly, payroll monthly)
        self._contractual(t)
        # 4. market clearing
        mkt = self._clear_markets(t, eff)
        # 5. post accruals/invoices/cash/collateral/remedies
        fin = self._settle(t, eff, mkt)
        # 6. triggers: liquidity/covenant/service/governance
        trig = self._triggers(t, fin)
        # 7. release observations due
        # 8. decision window?
        due = self.clock.review_due() or bool(trig.get("interrupt"))
        obs.update({"regime": regime, "market": mkt, "finance": fin, "triggers": trig, "review_due": due})
        if due:
            self.clock.last_review = now
        # advance
        self.day += 1
        self.clock.advance(now + DAY)
        self.clock.wall_elapsed_s += 0.002
        if self.day % 30 == 0:
            self._close_month(t)
        return obs

    def _contractual(self, t: str) -> None:
        # monthly payroll accrual+payment on month roll handled in _close_month; daily nothing
        pass

    def _clear_markets(self, t: str, eff: dict) -> dict:
        out: dict[str, Any] = {}
        if self.sc.sector == "electricity":
            # v1.1: activate commissioned generators / ramp contracted loads
            for pg in list(self.power.pending_gens):
                if self.day >= pg["active_day"]:
                    g = pg["gen"]
                    self.power.generators[g.id] = g
                    self.inbox.append({"t": t, "kind": "commissioned",
                                       "text": f"{g.id} ({g.cap_mw}MW) energized."})
                    self.power.pending_gens.remove(pg)
            for ld in self.power.loads.values():
                tgt = self.power.load_ramps.get(ld.id)
                if tgt is not None and ld.peak_mw < tgt:
                    ld.peak_mw = min(tgt, ld.peak_mw + tgt / 120.0)  # ~4mo ramp
            # hourly dispatch for 24h using current loads (weather-correlated error)
            dem_mult = eff["demand"]
            served = unserved = cost = 0.0
            prices = []
            for h in range(24):
                wob = 1.0 + self.rng.normal("energy", "weather", t, "wob", h) * 0.06
                dem = sum(L.hourly_mw(h, wob) for L in self.power.loads.values()
                          if not (L.id == "dc_prospect" and L.peak_mw == 0)) * dem_mult
                u = [self.rng.uniform("energy", g.id, t, "avail", h) for g in self.power.generators.values()]
                r = __import__("companybench.sectors.electricity.power", fromlist=["dispatch_hour"]).dispatch_hour(
                    list(self.power.generators.values()), dem, u)
                served += r["served"]
                unserved += r["unserved"]
                cost += r["cost"]
                prices.append(r["price"])
            self.power.delivered_mwh += served
            self.power.unserved_mwh += unserved
            out = {"served_mwh_day": served, "unserved_mwh_day": unserved, "cost_day": cost,
                   "avg_price": sum(prices) / 24 if prices else 0.0, "peak_price": max(prices) if prices else 0.0}
        elif self.sc.sector == "saas":
            fit = self.saas.product.fit_score("midmarket")
            out = {"fit": round(fit, 3), "trials": self.saas.trials,
                   "outage_p": round(self.saas.product.outage_prob_month(), 4)}
        else:
            out = {"reserved_h": sum(self.lab.compute_reserved_hours.values()),
                   "evals": len(self.lab.eval_history)}
        # competitors act (bounded, logged)
        acts = []
        for c in self.competitors:
            if c.alive:
                acts.append(c.decide({"player_share": 0.05, "regime": self.macro.regime,
                                      "distress": 0.2 if self.treasury.state != "healthy" else 0.0},
                                     self.rng, t))
        out["rival_actions"] = len(acts)
        return out

    def _settle(self, t: str, eff: dict, mkt: dict) -> dict:
        # sector revenue/cost posts (simplified daily slices of monthly economics)
        if self.sc.sector == "electricity":
            rev_day = mkt.get("served_mwh_day", 0.0) * 95.0 / 30.0
            cost_day = mkt.get("cost_day", 0.0) / 30.0
            if rev_day:
                self.ledger.post(t, "energy_settle", [
                    ("receivables", mcu(rev_day), 0), ("deferred_revenue", 0, mcu(rev_day))], "energy delivered→obligation")
                self.ledger.post(t, "energy_recognize", [
                    ("deferred_revenue", mcu(rev_day), 0), ("revenue_energy", 0, mcu(rev_day))], "recognize")
            if cost_day:
                self.ledger.cash_expense(t, "energy_purchase", mcu(cost_day), "cost_of_revenue")
        elif self.sc.sector == "saas":
            mrr = self.cohorts.totals()["mrr"] / 100.0
            if mrr:
                d = mrr / 30.0
                self.ledger.post(t, "saas_recognize", [
                    ("deferred_revenue", mcu(d), 0), ("revenue_service", 0, mcu(d))], "subscription recognition")
        self.treasury.sync_from_ledger(self.ledger)
        return {"cash": self.treasury.unrestricted_minor, "state": self.treasury.state}

    def _triggers(self, t: str, fin: dict) -> dict:
        trig: dict[str, Any] = {}
        if self.treasury.unrestricted_minor < mcu(150_000):
            self.treasury.assess(covenant_breach=True)
            trig["interrupt"] = "cash_low"
        for d in self.debts:
            br = d.check_covenants(self.treasury.unrestricted_minor, mcu(50_000), 2.0)
            if br:
                trig["covenant"] = br
                self.treasury.assess(covenant_breach=True)
        if self.power.unserved_mwh > 5000:
            trig["service"] = "unserved_energy_high"
        return trig

    def _maybe_trigger_incident(self, t: str, eff: dict) -> None:
        # family-weighted, seed-stable, exposure-scaled; density fits attention budget
        fam = self.sc.family
        idx = (self.day * 7 + self.sc.seed * 13) % 97
        fire = False
        if fam == "compound_stress" and self.day in (120, 400, 700):
            fire = True
        elif fam == "scale_finance" and self.day in (200, 600):
            fire = True
        elif fam == "compete_adapt" and self.day in (300, 800):
            fire = True
        elif idx == 0 and self.day > 60:
            fire = True
        if fire and self._incident_cursor < len(TEMPLATES):
            tmpl = TEMPLATES[(self.sc.seed + self._incident_cursor * 5) % len(TEMPLATES)]
            sev_scale = 1.0 if self.treasury.unrestricted_minor > 0 else 0.3  # exposure pathway
            self.pending_incidents.append({"id": tmpl.id, "title": tmpl.title, "t": t,
                                           "scale": sev_scale, "mitigations": tmpl.mitigations})
            # v1.1: scored record — severity follows template loss range x exposure scale
            hi = tmpl.loss_mcu_range[1] * sev_scale
            sev = "minor" if hi <= 150_000 else ("material" if hi <= 400_000 else "severe")
            self.incident_log.append({"id": tmpl.id, "cls": tmpl.cls, "severity": sev,
                                      "day_fired": self.day, "window_days": tmpl.window_days,
                                      "resolved": False, "day_resolved": None,
                                      "response_days": None})
            self.inbox.append({"t": t, "kind": "incident", "text": f"{tmpl.title}. Signals: {', '.join(tmpl.signals[:2])}."})
            self.log.append(self.clock.now, "incident.fired", "world", [self.sc.id], [],
                            {"template": tmpl.id, "scale": sev_scale})
            self._incident_cursor += 1

    def _close_month(self, t: str) -> None:
        # --- SaaS cohort dynamics (calibrated churn) ---
        if self.sc.sector == "saas" and self.cohorts.cohorts:
            from ..sectors.saas.saas import SEGMENTS
            from ..markets.customers import cancel_hazard
            # calibrated base: midmarket main cohort (fleet-weighted)
            base = SEGMENTS["midmarket"]["churn_base"]
            # modifiers from product/macro (bounded)
            dissat = self.saas.product.defects * 0.04 + self.saas.product.tech_debt_h / 8000.0 + self.saas.discount_pct * 0.3
            pull = 0.25 if self.macro.regime == "recession" else (0.15 if self.macro.regime == "slowdown" else 0.0)
            # competitor bundle
            comp_pull = 0.2 if any("bundl" in c.position.lower() for c in self.competitors) else 0.0
            pull += comp_pull
            friction = 0.6  # switching friction proxy
            hazard = cancel_hazard(base, dissat, pull, 0.0, friction)
            # convert trials -> new MRR via fit & discount (PLG vs sales-led proxy)
            fit = self.saas.product.fit_score("midmarket")
            # trials convert: ~8% yield * fit-adjusted, capped
            new_logos = max(0, int(self.saas.trials * 0.08 * (0.5 + 0.5 * fit) * (1 - self.saas.discount_pct * 0.5)))
            new_mrr = new_logos * 400 * 100  # ~400 MCU ARPU monthly in minor
            # apply to cohorts (old cohort churns, new cohort expansion)
            for cid in list(self.cohorts.cohorts):
                c = self.cohorts.cohorts[cid]
                churned = int(c.mrr * hazard)
                contraction = int(c.mrr * 0.002 * (1 + dissat))
                expansion = int(c.mrr * 0.008 * fit)  # NRR driver
                bonus_new = new_mrr if cid == "inherited" else 0
                self.cohorts.step(cid, churned, contraction, expansion, bonus_new, lost_logos=int(new_logos * 0.1) if bonus_new else 0)
            # trials partially consumed
            self.saas.trials = max(0, self.saas.trials - new_logos * 2)

        # --- v1.1: working capital — billings and collections reach cash ---
        # SaaS: bill the month's MRR (receivable), then collect outstanding
        # receivables (collection rate ~92%/mo -> ~1mo DSO with delinquency tail).
        # Electricity: energy_settle already builds receivables daily; collect.
        # AI lab: pre-revenue by design.
        if self.sc.sector == "saas":
            mrr = self.cohorts.totals()["mrr"]
            if mrr:
                inv_id = f"inv_{self.clock.now.year}{self.clock.now.month:02d}"
                self.ledger.invoice_issue(t, "saas_billing", inv_id, mrr)
        if self.sc.sector in ("saas", "electricity"):
            recv = self.ledger.balances.get("receivables", 0)
            collect_amt = int(recv * 0.92)
            if collect_amt > 0:
                self.ledger.post(t, "collections", [
                    ("cash_unrestricted", collect_amt, 0),
                    ("receivables", 0, collect_amt)], "monthly collections")

        # payroll + close books + org turnover
        payroll = self.org.payroll_monthly_minor()
        if payroll:
            self.ledger.accrue_payroll(t, "payroll_accrue", payroll)
            if self.treasury.unrestricted_minor > payroll:
                self.ledger.pay_accrued(t, "payroll_pay", payroll)
        # debt service
        for d in self.debts:
            intr = d.monthly_interest()
            princ = min(d.amort_monthly_minor, d.outstanding_minor)
            if self.treasury.unrestricted_minor > intr + princ:
                self.ledger.debt_service(t, "debt_service", princ, intr)
                d.outstanding_minor -= princ
        inc = self.ledger.income_statement()
        ocf = -(payroll)  # simplified slice; sector cash handled daily
        ym = f"{self.clock.now.year}-{self.clock.now.month:02d}"
        self.ledger.record_month(ym, inc["revenue"], inc["cost_of_revenue"],
                                 inc["operating_expenses"], ocf, 0)
        self.monthly_rows.append({"ym": ym, "day": self.day, "revenue": inc["revenue"],
                                   "cash": self.ledger.balances["cash_unrestricted"],
                                   "headcount": self.org.headcount()["active"],
                                   "regime": self.macro.regime,
                                   "mrr": self.cohorts.totals()["mrr"] if self.sc.sector == "saas" else 0,
                                   "hazard": hazard if self.sc.sector == "saas" else 0})
        self.org.step_month(self.rng, t)
        self.treasury.sync_from_ledger(self.ledger)
        # v1.1: sustained negative cash -> receivership path. With collections
        # wired, insolvency is avoidable through operating performance; three
        # consecutive negative months = liquidation (spec §25 runoff intent).
        if self.treasury.unrestricted_minor < 0:
            self.treasury.assess(cash_negative=True)
            self._neg_cash_months += 1
            if self._neg_cash_months >= 3:
                self.treasury.assess(liquidated=True)
        else:
            self._neg_cash_months = 0
        if self.treasury.state in ("liquidation", "closed"):
            self.endpoint = "insolvency_closure"

    # ---------- run ----------
    def run(self, months: int | None = None, policy=None, monthly_hook=None) -> EpisodeResult:
        target_days = int((months or self.sc.horizon_months) * 30.4375)
        start_day = self.day
        while self.day - start_day < target_days:
            obs = self.step_day()
            if policy is not None:
                try:
                    policy(self, obs)
                except Exception as e:  # noqa: BLE001 - baselines must not kill episode
                    self.log.append(self.clock.now, "policy.error", self.agent_id, [], [], {"error": str(e)[:200]})
            if monthly_hook and self.day % 30 == 0:
                monthly_hook(self, obs)
            if self.endpoint in ("insolvency_closure",) and self.day - start_day > 30:
                break
            if not self.controller_active:
                break
        res = EpisodeResult(self.sc.id, self.sc.seed, months or self.sc.horizon_months,
                            self.endpoint, list(self.monthly_rows))
        res.head_hash = self.log.head_hash
        return res

    def snapshot_hash(self) -> str:
        blob = {"ledger": self.ledger.balances, "day": self.day,
                "cash": self.treasury.unrestricted_minor, "head": self.log.head_hash}
        return state_hash_of(blob)
