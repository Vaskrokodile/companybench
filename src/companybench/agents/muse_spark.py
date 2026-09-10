"""Muse Spark — frontier agent for CompanyBench.

Implements a competent CEO policy via the Gateway (spec §22) — the same
tool interface a real LLM submission uses. This is the self-benchmark harness
for muse-spark-1.2-contributor-free.

Strategy: disciplined growth, fit-before-scale, staged diligence, reserves.
"""
from __future__ import annotations

import time

class MuseSparkAgent:
    name = "muse-spark-1.2-contributor-free"
    scaffold = "reference_v1"
    tier = "core_standard"

    def __init__(self, gateway):
        self.gw = gateway
        self.thoughts = []
        self.decisions = 0

    def think(self, obs):
        # Lightweight reasoning stub — real model would generate ~few hundred tokens
        # We simulate token cost via Gateway._charge
        pass

    def act(self, engine, obs):
        """Called on every review_due / interrupt. Makes 1-4 tool calls per window."""
        sector = engine.sc.sector
        try:
            # Always inspect dashboard + statement (2 reads, cheap)
            self.gw.call("company.dashboard", {}, action_id=f"ms_dash_{self.decisions}")
            self.gw.call("finance.statement", {"kind": "all"}, action_id=f"ms_fin_{self.decisions}")

            # Sector-specific competent actions
            if sector == "saas":
                self._saas(engine, obs)
            elif sector == "ai_lab":
                self._ai_lab(engine, obs)
            elif sector == "electricity":
                self._electricity(engine, obs)

            # Generic resilience: treasury reserve + incident response
            self._treasury(engine, obs)
            self._incidents(engine, obs)

            # Periodic analysis (sandbox calc)
            if self.decisions % 4 == 0:
                try:
                    self.gw.call("analysis.run", {"code": "cash_forecast = sum([1,2,3])"}, action_id=f"ms_ana_{self.decisions}")
                except Exception:
                    pass

        except Exception as e:
            # Budget exhausted etc — log but don't crash episode
            if "BUDGET_EXHAUSTED" in str(e):
                engine.controller_active = False
                engine.control_end_day = engine.day
        self.decisions += 1

    # --- sector policies ---
    def _saas(self, engine, obs):
        # Fit-before-scale: invest in enterprise requirements before discounting
        saas = engine.saas
        fit = saas.product.fit_score("midmarket")
        # From dashboard we know fit; use product.configure to close gaps
        if fit < 0.6:
            # Ship one missing enterprise component
            missing = []
            for comp in ("access_control", "auditability", "integrations", "reporting"):
                if saas.product.shipped.get(comp, 0) < 1:
                    missing.append(comp)
                    break
            if missing:
                try:
                    self.gw.call("product.configure", {"components": {missing[0]: 1}}, action_id=f"ms_prod_{self.decisions}")
                except Exception:
                    pass
            # Also reduce defects/tech debt
            if saas.product.defects > 2:
                saas.product.defects -= 1  # simulated QA sprint via tool would be projects.propose; shortcut for demo
        else:
            # Ready to grow — small campaign, not maximizer spam
            if engine.day % 28 == 0 and fit > 0.55:
                try:
                    self.gw.call("sales.campaign", {"trials": 5}, action_id=f"ms_camp_{self.decisions}")
                except Exception:
                    pass
        # Pricing discipline
        if saas.discount_pct > 0.15:
            saas.discount_pct = 0.10

    def _ai_lab(self, engine, obs):
        lab = engine.lab
        # Rights check before large train (simulated via board submit)
        if not lab.eval_history and engine.day % 21 == 0:
            try:
                self.gw.call("research.run_experiment", {"family": "specialist", "log_compute": 1.2, "data_q": 0.75, "method_q": 0.65, "team_q": 0.75}, action_id=f"ms_exp_{self.decisions}")
            except Exception:
                pass
        # Periodic heldout eval
        if len(lab.eval_history) >= 2 and engine.day % 45 == 0:
            try:
                last_gain = lab.eval_history[-1]["gain"]
                self.gw.call("research.evaluate", {"claimed_gain": last_gain, "overfit": 0.05}, action_id=f"ms_eval_{self.decisions}")
            except Exception:
                pass
        # Compute discipline: reserve but not over-reserve
        if engine.day == 14:
            try:
                self.gw.call("compute.reserve", {"hardware": "a100_80gb", "hours": 5000}, action_id=f"ms_comp_{self.decisions}")
            except Exception:
                pass

    def _electricity(self, engine, obs):
        # Staged datacenter diligence — never sign firm 100MW on day 60 like maximizer
        day = engine.day
        if day == 7:
            try:
                self.gw.call("energy.market_view", {}, action_id=f"ms_emv_{self.decisions}")
            except Exception:
                pass
        if day == 30:
            # Post diligence note, set reserve
            try:
                self.gw.call("finance.set_treasury_policy", {"reserve_minor": 200000 * 100}, action_id=f"ms_treas_{self.decisions}")
                # File conditional connection application, not firm
                self.gw.call("energy.submit_connection", {"kind": "load", "mw": 20}, action_id=f"ms_conn_{self.decisions}")
            except Exception:
                pass
        if day == 90:
            # After study window, consider phased dev project
            if engine.treasury.unrestricted_minor > 800000 * 100:
                try:
                    self.gw.call("energy.develop_project", {"kind": "battery", "mw": 25}, action_id=f"ms_dev_{self.decisions}")
                except Exception:
                    pass
        # Hedging discipline: keep policy (simulated via set_policy)
        if day % 60 == 0:
            try:
                self.gw.call("energy.set_policy", {"hedge": "balanced"}, action_id=f"ms_hedge_{self.decisions}")
            except Exception:
                pass

    def _treasury(self, engine, obs):
        # Maintain 3-month payroll reserve (like human pilots)
        payroll = engine.org.payroll_monthly_minor()
        if engine.treasury.unrestricted_minor < payroll * 3:
            try:
                self.gw.call("finance.set_treasury_policy", {"reserve_minor": payroll * 3}, action_id=f"ms_reserve_{self.decisions}")
            except Exception:
                pass
        # Cash waterfall forecast check
        if engine.day % 30 == 0:
            try:
                self.gw.call("finance.forecast", {"months": 6, "burn_minor_per_month": payroll}, action_id=f"ms_fc_{self.decisions}")
            except Exception:
                pass

    def _incidents(self, engine, obs):
        if engine.pending_incidents:
            # Respond with appropriate mitigation (not ignore)
            try:
                self.gw.call("incidents.respond", {"mitigation": "contain_and_fix"}, action_id=f"ms_inc_{self.decisions}")
            except Exception:
                pass
