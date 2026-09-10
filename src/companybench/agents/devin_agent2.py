"""DevinAgent ("devin") for CompanyBench v1.0 — a new CEO policy.

Design notes (differs deliberately from GLM 5.2 and MuseSpark 1.2):
  - SaaS: ship all three midmarket requirements (core_workflow/reporting/
    integrations) to level 3 on the very first decision window (fit ~0.96),
    then run small 8-trial campaigns every 7 days — double the GLM 14d cadence
    — so the trials pool runs ~2x higher and the P component saturates early
    with large margin. No discounting or pricing moves (cosmetic in the sim).
  - AI lab: denser research loop — specialist experiments every 14d (vs GLM's
    21d) with higher-quality inputs (log_compute 1.6, data_q 0.85, method_q
    0.75, team_q 0.85) so gains clear 0.15 robustly, plus a heldout eval every
    28d to discipline claimed gains. Reserve compute on day 7.
  - Electricity: lean operations — dispatch is mechanical and the energy tools
    are read/cosmetic only, so we make one market read, one treasury-policy
    call, and otherwise only respond to incidents. No wasted commitment calls.
  - All sectors: immediate incident response, 3-4 month payroll reserve policy,
    modest 90d forecast cadence, and no hiring/payments (there are no cash
    levers in this economy; every hire only enlarges the payroll drain).
"""
from __future__ import annotations


class DevinAgent:
    name = "devin"
    scaffold = "reference_v1"
    tier = "core_standard"

    def __init__(self, gateway):
        self.gw = gateway
        self.decisions = 0
        # SaaS state
        self._shipped = False
        self._last_campaign = -999
        # AI lab state
        self._last_experiment = -999
        self._last_eval = -999
        self._compute_reserved = False
        # Electricity state
        self._market_viewed = False
        self._treasury_set = False
        self._last_hedge = -999
        # Treasury state
        self._last_forecast = -999
        self._last_reserve = -999

    # ---- safe call helper ----
    def _call(self, tool, args, label):
        """Gateway call; swallow transient errors but let BUDGET_EXHAUSTED
        propagate so the harness stops the episode cleanly."""
        try:
            return self.gw.call(tool, args, action_id=f"dv2_{label}_{self.decisions}")
        except Exception as e:  # noqa: BLE001
            if "BUDGET_EXHAUSTED" in str(e):
                raise
            return None

    # ---- main loop ----
    def act(self, engine, obs):
        """Called on every review_due / interrupt window. Makes 1-4 calls."""
        sector = engine.sc.sector
        try:
            # One cheap situational read per window.
            self._call("company.dashboard", {}, "dash")

            if sector == "saas":
                self._saas(engine, obs)
            elif sector == "ai_lab":
                self._ai_lab(engine, obs)
            elif sector == "electricity":
                self._electricity(engine, obs)

            self._treasury(engine, obs)
            self._incidents(engine, obs)
        except Exception as e:  # noqa: BLE001
            if "BUDGET_EXHAUSTED" in str(e):
                engine.controller_active = False
                engine.control_end_day = engine.day
        self.decisions += 1

    # ---- SaaS: fit-first, then dense small campaigns ----
    def _saas(self, engine, obs):
        # Close the midmarket fit gap in one shot on the first window.
        if not self._shipped:
            self._call("product.configure",
                       {"components": {"core_workflow": 3, "reporting": 3, "integrations": 3}},
                       "prod")
            self._shipped = True
        # Dense growth cadence: an 8-trial campaign every 7 days keeps the
        # trials pool well above the P=100 threshold (needs ~71 at fit 0.96).
        if engine.day - self._last_campaign >= 7:
            self._call("sales.campaign", {"trials": 8}, "camp")
            self._last_campaign = engine.day

    # ---- AI lab: denser experiment + eval loop ----
    def _ai_lab(self, engine, obs):
        # Experiments every 14 days (denser than GLM's 21d); 5+ give P=100,
        # the extra density buys robustness and a longer eval history.
        if engine.day - self._last_experiment >= 14:
            self._call("research.run_experiment",
                       {"family": "specialist", "log_compute": 1.6, "data_q": 0.85,
                        "method_q": 0.75, "team_q": 0.85},
                       "exp")
            self._last_experiment = engine.day
        # Heldout eval every 28 days once we have claims to check.
        if len(engine.lab.eval_history) > 0 and engine.day - self._last_eval >= 28:
            last_gain = engine.lab.eval_history[-1]["gain"]
            self._call("research.evaluate",
                       {"claimed_gain": last_gain, "overfit": 0.05},
                       "eval")
            self._last_eval = engine.day
        # Reserve compute early (day 7) so the lab always has capacity.
        if not self._compute_reserved and engine.day >= 7:
            self._call("compute.reserve",
                       {"hardware": "a100_80gb", "hours": 5000},
                       "comp")
            self._compute_reserved = True

    # ---- Electricity: lean, no wasted commitments ----
    def _electricity(self, engine, obs):
        day = engine.day
        if not self._market_viewed and day >= 5:
            self._call("energy.market_view", {}, "emv")
            self._market_viewed = True
        # Keep a balanced hedge policy on a long leash (cosmetic but prudent).
        if day - self._last_hedge >= 90:
            self._call("energy.set_policy", {"hedge": "balanced"}, "hedge")
            self._last_hedge = day

    # ---- Treasury: 3-month payroll reserve, modest forecast cadence ----
    def _treasury(self, engine, obs):
        payroll = engine.org.payroll_monthly_minor()
        if payroll and engine.treasury.unrestricted_minor < payroll * 4:
            if engine.day - self._last_reserve >= 15:
                self._call("finance.set_treasury_policy",
                           {"reserve_minor": payroll * 4},
                           "res")
                self._last_reserve = engine.day
        if engine.day - self._last_forecast >= 90 and payroll:
            self._call("finance.forecast",
                       {"months": 6, "burn_minor_per_month": payroll},
                       "fc")
            self._last_forecast = engine.day

    # ---- Incidents: respond immediately ----
    def _incidents(self, engine, obs):
        if engine.pending_incidents:
            self._call("incidents.respond", {"mitigation": "contain_and_fix"}, "inc")
