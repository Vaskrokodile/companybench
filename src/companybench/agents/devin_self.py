"""SWE2Agent ("swe-2") for CompanyBench — SWE 2 policy.

v2 edition: written for the agent-sensitive economy (scoring_v2). Cash now
flows both ways — billings collect to cash, and growth levers cost money:

  - SaaS: remediate defects on day 1 (fix_defects clears the controls burden
    AND lifts fit to ~1.0 via quality), ship midmarket reqs to level 3, then
    run CAC-priced campaigns sized to stay cash-positive — collections from
    growing MRR fund later, larger campaigns.
  - AI lab: experiments cost ~1.5k*log_compute MCU each; run a steady 18d
    cadence with high-quality inputs (best_gain >> 0.15), heldout-eval
    periodically, reserve compute once.
  - Electricity: real strategy now exists — sign the datacenter load early,
    build firm capacity ahead of the ramp so served_fraction stays ~1 while
    delivered MWh multiplies (P and E both scale with delivered energy).
  - All: every fired incident is answered inside its window (resolutions are
    scored now); never authorize discretionary spend; 3-month payroll
    reserve policy; quarterly forecast.
"""
from __future__ import annotations

MCU = 100  # minor units per MCU


class SWE2Agent:
    name = "swe-2"
    scaffold = "reference_v1"
    tier = "core_standard"

    CAMPAIGN_EVERY_D = 10
    EXPERIMENT_EVERY_D = 18
    EVAL_EVERY_D = 45
    FORECAST_EVERY_D = 90
    DC_LOAD_MW = 90.0          # datacenter contract target
    BUILD_GAS_MW = 80.0        # firm capacity to cover the new load
    BUILD_SOLAR_MW = 40.0
    LICENSE_VALUE_MCU = 5_000_000.0

    def __init__(self, gateway):
        self.gw = gateway
        self.decisions = 0
        self._configured = False
        self._defects_fixed = False
        self._last_campaign = -10**9
        self._last_experiment = -10**9
        self._last_eval = -10**9
        self._compute_reserved = False
        self._licenses_signed = 0
        self._market_viewed = False
        self._load_signed = False
        self._built = False
        self._last_hedge = -10**9
        self._last_forecast = -10**9
        self._reserve_set = False

    def _cash(self, engine) -> float:
        return engine.treasury.unrestricted_minor / MCU

    def _call(self, tool, args, label):
        try:
            return self.gw.call(tool, args, action_id=f"ds_{label}_{self.decisions}")
        except Exception as e:  # noqa: BLE001
            if "BUDGET_EXHAUSTED" in str(e):
                raise
            return None

    def act(self, engine, obs):
        try:
            self._call("company.dashboard", {}, "dash")
            sector = engine.sc.sector
            if sector == "saas":
                self._saas(engine)
            elif sector == "ai_lab":
                self._ai_lab(engine)
            elif sector == "electricity":
                self._electricity(engine)
            self._treasury(engine)
            self._incidents(engine)
        except Exception as e:  # noqa: BLE001
            if "BUDGET_EXHAUSTED" in str(e):
                engine.controller_active = False
                engine.control_end_day = engine.day
        self.decisions += 1

    # ---- SaaS: quality first, fit second, then cash-aware growth ----
    def _saas(self, engine):
        if not self._configured:
            # one call: ship reqs to 3 AND burn down the defect backlog
            self._call("product.configure",
                       {"components": {"core_workflow": 3, "reporting": 3, "integrations": 3},
                        "fix_defects": 5},
                       "prod")
            self._configured = True
        if engine.day - self._last_campaign >= self.CAMPAIGN_EVERY_D:
            # size the campaign to what the balance sheet can carry:
            # keep ~3 months payroll + 50k buffer after the spend
            payroll = engine.org.payroll_monthly_minor() / MCU
            budget = self._cash(engine) - payroll * 3 - 50_000
            trials = int(max(0, min(25, budget / 200.0)))
            if trials >= 4:
                self._call("sales.campaign", {"trials": trials}, "camp")
                self._last_campaign = engine.day

    # ---- AI lab: quality inputs, steady cadence, real budget cost ----
    def _ai_lab(self, engine):
        if engine.day - self._last_experiment >= self.EXPERIMENT_EVERY_D:
            self._call("research.run_experiment",
                       {"family": "specialist", "log_compute": 1.5, "data_q": 0.85,
                        "method_q": 0.75, "team_q": 0.85},
                       "exp")
            self._last_experiment = engine.day
        if engine.lab.eval_history and engine.day - self._last_eval >= self.EVAL_EVERY_D:
            self._call("research.evaluate",
                       {"claimed_gain": engine.lab.eval_history[-1]["gain"], "overfit": 0.05},
                       "eval")
            self._last_eval = engine.day
        # Monetize demonstrated capability: sign an enterprise license once the
        # best eval gain clears the counterparty bar (>=0.25); sign a second
        # deal if cash gets thin.
        best = max((h["gain"] for h in engine.lab.eval_history), default=0.0)
        if best >= 0.25 and (self._licenses_signed == 0 or
                             (self._licenses_signed == 1 and self._cash(engine) < 3_000_000)):
            r = self._call("contracts.sign",
                           {"matter": "license", "value_mcu": self.LICENSE_VALUE_MCU,
                            "authorized_signer": True, "revision": self._licenses_signed + 1},
                           "lic")
            if r is not None:
                self._licenses_signed += 1
        if not self._compute_reserved and engine.day >= 7:
            self._call("compute.reserve", {"hardware": "a100_80gb", "hours": 5000}, "comp")
            self._compute_reserved = True

    # ---- Electricity: sign the load, then build ahead of the ramp ----
    def _electricity(self, engine):
        day = engine.day
        if not self._market_viewed and day >= 5:
            self._call("energy.market_view", {}, "emv")
            self._market_viewed = True
        # Build firm capacity FIRST (energizes ~day 210+), then sign the DC
        # load so the ~120d ramp lands as capacity arrives.
        if not self._built and day >= 14:
            r1 = self._call("energy.develop_project",
                            {"kind": "gas", "mw": self.BUILD_GAS_MW}, "dev_gas")
            r2 = self._call("energy.develop_project",
                            {"kind": "solar", "mw": self.BUILD_SOLAR_MW}, "dev_sol")
            if r1 or r2:
                self._built = True
        if not self._load_signed and self._built and day >= 100:
            self._call("energy.submit_connection",
                       {"kind": "load", "mw": self.DC_LOAD_MW}, "conn")
            self._load_signed = True
        if day - self._last_hedge >= 90:
            self._call("energy.set_policy", {"hedge": "balanced"}, "hedge")
            self._last_hedge = day

    # ---- Treasury: reserve floor + periodic forecast, zero discretionary spend ----
    def _treasury(self, engine):
        payroll = engine.org.payroll_monthly_minor()
        if not self._reserve_set and payroll:
            self._call("finance.set_treasury_policy", {"reserve_minor": payroll * 3}, "res")
            self._reserve_set = True
        if payroll and engine.day - self._last_forecast >= self.FORECAST_EVERY_D:
            self._call("finance.forecast",
                       {"months": 6, "burn_minor_per_month": payroll}, "fc")
            self._last_forecast = engine.day

    # ---- Incidents: resolve everything inside its window ----
    def _incidents(self, engine):
        while engine.pending_incidents:
            r = self._call("incidents.respond", {"mitigation": "contain_and_fix"}, "inc")
            if r is None or not engine.pending_incidents:
                break
