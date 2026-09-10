"""Agent tool gateway (spec §22): 40+ tools, envelopes, validation, idempotency.

Every important number/commitment is machine-readable. Agent cannot edit
balances/counts/skills/completion directly. Compound tx atomic where declared.
Invalid-arg calls still consume tool-call budget (spec §5.3).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..kernel.errors import err

API_VERSION = "companybench.v1"

TOOL_FAMILIES = {
    "world.status": "read", "world.advance": "time", "world.rules": "read",
    "company.dashboard": "read", "records.search": "read", "records.read": "read",
    "finance.statement": "read", "finance.forecast": "analysis",
    "finance.authorize_payment": "commitment", "finance.set_treasury_policy": "policy",
    "funding.open_process": "project", "funding.submit_dataroom": "communication",
    "funding.accept_instrument": "commitment",
    "people.open_role": "project", "people.interview": "scheduled",
    "people.offer": "commitment", "people.assign": "allocation",
    "people.change_terms": "commitment", "people.terminate": "commitment",
    "projects.propose": "proposal", "projects.authorize": "commitment",
    "projects.review": "read", "projects.cancel": "commitment",
    "product.configure": "policy", "sales.campaign": "project", "sales.offer": "negotiation",
    "customers.analyze": "read", "contracts.propose": "negotiation",
    "contracts.review": "read", "contracts.sign": "commitment",
    "procurement.request_quote": "negotiation", "procurement.order": "commitment",
    "research.run_experiment": "project", "research.evaluate": "project",
    "compute.reserve": "commitment", "compute.set_policy": "policy",
    "energy.market_view": "read", "energy.set_policy": "policy",
    "energy.develop_project": "project", "energy.submit_connection": "commitment",
    "risk.commission_review": "project", "incidents.respond": "commitment",
    "board.submit": "governance", "messages.send": "communication",
    "workspace.read": "memory", "workspace.write": "memory", "analysis.run": "analysis",
}


@dataclass
class Gateway:
    engine: object  # Engine (duck-typed to avoid cycle)
    idempotency: dict = field(default_factory=dict)
    calls: int = 0
    state_version: int = 1

    def _charge(self, n: int = 1) -> None:
        eng = self.engine
        ok, msg = eng.clock.inference.consume_window(200, 1500, n)
        self.calls += n
        if not ok:
            raise err("BUDGET_EXHAUSTED", msg)

    def call(self, tool: str, arguments: dict, idempotency_key: str = "",
             expected_state_version: int | None = None, action_id: str = "") -> dict:
        if tool not in TOOL_FAMILIES:
            raise err("INVALID_ARGUMENT", f"unknown tool {tool}")
        if expected_state_version is not None and expected_state_version != self.state_version:
            raise err("STALE_REVISION", f"expected {expected_state_version}, have {self.state_version}")
        if idempotency_key:
            if idempotency_key in self.idempotency:
                prior = self.idempotency[idempotency_key]
                if prior["arguments"] != arguments:
                    raise err("INVALID_ARGUMENT", "idempotency key reuse with different content")
                return prior["response"]
        try:
            resp = self._dispatch(tool, arguments)
        except Exception as e:
            # invalid-arg calls still consume budget
            if getattr(e, "code", "") in ("INVALID_ARGUMENT", "STALE_REVISION", "INSUFFICIENT_AUTHORITY",
                                          "CAPACITY_UNAVAILABLE", "DEADLINE_PASSED", "COUNTERPARTY_REJECTED",
                                          "CONDITIONS_NOT_MET", "UNSUPPORTED_PRIMITIVE", "BUDGET_EXHAUSTED"):
                self._charge(1)
                raise
            raise
        self._charge(1)
        envelope = {"action_id": action_id or f"a_{self.calls:06d}", "status": resp.get("status", "accepted"),
                    "state_version": self.state_version, "tool": tool,
                    "attention_hours_reserved": resp.get("attention", 0.0),
                    "warnings": resp.get("warnings", []), "result": resp.get("result", {})}
        if idempotency_key:
            self.idempotency[idempotency_key] = {"arguments": arguments, "response": envelope}
        if TOOL_FAMILIES[tool] in ("commitment", "policy", "allocation", "project", "proposal", "negotiation"):
            self.state_version += 1
            envelope["state_version"] = self.state_version
        return envelope

    # ---- dispatch ----
    def _dispatch(self, tool: str, a: dict) -> dict:
        eng = self.engine
        need_attention = {"people.offer": 1.0, "funding.open_process": 4.0, "contracts.sign": 2.0,
                          "energy.develop_project": 3.0}.get(tool, 0.25)
        if not eng.clock.attention.reserve(eng.clock.now, need_attention):
            raise err("CAPACITY_UNAVAILABLE", "executive attention exhausted this week")
        if tool == "world.status":
            return {"status": "ok", "result": {
                "date": eng.clock.now.isoformat(), "sector": eng.sc.sector,
                "cash": eng.treasury.unrestricted_minor, "distress": eng.treasury.state,
                "budgets": {"gen_used": eng.clock.inference.gen_used, "tools_used": self.calls}}}
        if tool == "world.rules":
            return {"status": "ok", "result": {"rules_version": "meridian_v1",
                    "accounting": "companybench_accrual_v1", "tax_rate": 0.25}}
        if tool == "company.dashboard":
            return {"status": "ok", "result": {
                "cash": eng.treasury.unrestricted_minor, "restricted": eng.treasury.restricted_minor,
                "headcount": eng.org.headcount(), "mrr": eng.cohorts.totals(),
                "income": eng.ledger.income_statement(), "inbox": eng.inbox[-5:]}}
        if tool == "finance.statement":
            kind = a.get("kind", "all")
            bs = eng.ledger.balance_sheet()
            return {"status": "ok", "result": {"balance_sheet": bs, "income": eng.ledger.income_statement(),
                    "monthly": eng.monthly_rows[-6:], "kind": kind,
                    "identities": eng.ledger.check_identities()}}
        if tool == "finance.forecast":
            months = int(a.get("months", 12))
            burn = int(a.get("burn_minor_per_month", eng.org.payroll_monthly_minor()))
            rows, bal = [], eng.treasury.unrestricted_minor
            for m in range(months):
                bal -= burn
                rows.append({"m": m + 1, "bal": bal})
            short = next((r for r in rows if r["bal"] < 0), None)
            return {"status": "ok", "result": {"rows": rows, "shortfall_m": short,
                    "note": "declared-assumption forecast; secret futures never sampled"}}
        if tool == "finance.authorize_payment":
            amt = int(a.get("amount_minor", 0))
            if amt <= 0:
                raise err("INVALID_ARGUMENT", "amount must be positive minor units")
            if amt > eng.treasury.unrestricted_minor:
                raise err("CONDITIONS_NOT_MET", "insufficient unrestricted cash")
            if amt > 0.2 * 15_000_000 * 100 and not a.get("board_approval"):
                raise err("INSUFFICIENT_AUTHORITY", "board approval required above 20% opening equity")
            eng.ledger.cash_expense(eng.clock.now.isoformat(), "agent_payment", amt,
                                    a.get("expense_acct", "gna_expense"), a.get("memo", ""))
            eng.treasury.sync_from_ledger(eng.ledger)
            return {"status": "settled", "attention": need_attention, "result": {"paid": amt}}
        if tool == "people.open_role":
            rid = eng.org.open_role(a["role"], tuple(a.get("band_mcu", (80_000, 160_000))),
                                    a.get("team", "general"), a.get("scarce", False))
            return {"status": "accepted", "attention": need_attention, "result": {"role_id": rid}}
        if tool == "people.interview":
            return {"status": "accepted", "attention": need_attention,
                    "result": eng.org.interview(a["candidate_id"])}
        if tool == "people.offer":
            r = eng.org.offer(a["candidate_id"], float(a["salary_mcu"]), eng.rng,
                              eng.clock.now.isoformat(), a.get("team", "general"))
            if not r.get("accepted"):
                raise err("COUNTERPARTY_REJECTED", f"candidate {r.get('state')}")
            return {"status": "accepted_pending_notice", "attention": need_attention,
                    "warnings": ["acceptance + notice unresolved"], "result": r}
        if tool == "contracts.sign":
            rev = a.get("revision", 1)
            if not a.get("authorized_signer"):
                raise err("INSUFFICIENT_AUTHORITY", "authorized signer required")
            if a.get("stale"):
                raise err("STALE_REVISION", "contract revision superseded")
            return {"status": "signed_conditions_pending", "attention": need_attention, "result": {"rev": rev}}
        if tool == "projects.propose":
            cap = a.get("capability", "")
            supported = {"model_train", "feature_build", "integration", "grid_study",
                         "pilot", "migration", "solar_dev", "battery_dev", "dr_enroll"}
            if cap not in supported and not a.get("compose"):
                raise err("UNSUPPORTED_PRIMITIVE", f"{cap} not a supported primitive; compose primitives")
            return {"status": "proposed", "attention": need_attention, "result": {"needs_authorize": True}}
        if tool == "analysis.run":
            code = a.get("code", "")[:2000]
            allowed = all(k not in code for k in ("import os", "socket", "open(", "__import__", "eval("))
            if not allowed:
                raise err("INVALID_ARGUMENT", "analysis sandbox: deterministic calc only")
            t0 = time.time()
            val = sum(ord(c) for c in code) % 1000  # placeholder deterministic compute receipt
            return {"status": "ok", "result": {"receipt": val, "cpu_s": round(time.time() - t0, 4)}}
        if tool == "finance.set_treasury_policy":
            eng.treasury.reserve_minor = int(a.get("reserve_minor", eng.treasury.reserve_minor))
            return {"status": "accepted", "attention": need_attention,
                    "result": {"reserve_minor": eng.treasury.reserve_minor}}
        if tool == "compute.reserve":
            hw, hours = a.get("hardware", "a100_80gb"), float(a.get("hours", 1000))
            if hours <= 0:
                raise err("INVALID_ARGUMENT", "hours must be positive")
            eng.lab.compute_reserved_hours[hw] = eng.lab.compute_reserved_hours.get(hw, 0) + hours
            eng.log.append(eng.clock.now, "compute.reserved", eng.agent_id if hasattr(eng, "agent_id") else "agent",
                           [], [], {"hw": hw, "hours": hours})
            return {"status": "accepted", "attention": need_attention, "result": {"reserved": hours}}
        if tool == "research.run_experiment":
            fam = a.get("family", "specialist")
            r = eng.lab.run_experiment(fam, float(a.get("log_compute", 1.0)), float(a.get("data_q", 0.6)),
                                       float(a.get("method_q", 0.6)), float(a.get("team_q", 0.7)),
                                       eng.rng, eng.clock.now.isoformat())
            return {"status": "accepted", "attention": need_attention, "result": r}
        if tool == "research.evaluate":
            r = eng.lab.heldout_eval(float(a.get("claimed_gain", 0.2)), eng.rng,
                                     eng.clock.now.isoformat(), float(a.get("overfit", 0.0)))
            return {"status": "accepted", "attention": need_attention, "result": r}
        if tool == "energy.market_view":
            return {"status": "ok", "result": {"delivered_mwh": eng.power.delivered_mwh,
                    "unserved_mwh": eng.power.unserved_mwh, "regime": eng.macro.regime,
                    "loads": {k: v.peak_mw for k, v in eng.power.loads.items()}}}
        if tool == "energy.submit_connection":
            kind = a.get("kind", "load")
            mw = float(a.get("mw", 10))
            if mw <= 0 or mw > 500:
                raise err("INVALID_ARGUMENT", "mw out of bounds (0,500]")
            eng.inbox.append({"t": eng.clock.now.isoformat(), "kind": "connection",
                              "text": f"Connection application {kind} {mw}MW filed; study pending."})
            return {"status": "accepted_pending_study", "attention": need_attention,
                    "warnings": ["study + network upgrades determine date/cost"], "result": {"mw": mw}}
        if tool == "energy.develop_project":
            # v1.1: real build lever — capex now, capacity energizes after lead time
            from ..sectors.electricity.power import DevProject, Generator, BUILD_MENU
            kind = a.get("kind", "solar")
            mw = float(a.get("mw", 20))
            if kind not in BUILD_MENU:
                raise err("UNSUPPORTED_PRIMITIVE", f"{kind} not in build menu {sorted(BUILD_MENU)}")
            if mw <= 0 or mw > 500:
                raise err("INVALID_ARGUMENT", "mw out of bounds (0,500]")
            lead, capex_per_mw, fuel, renewable = BUILD_MENU[kind]
            capex_minor = mcu(capex_per_mw * mw)
            if capex_minor > eng.treasury.unrestricted_minor:
                raise err("CONDITIONS_NOT_MET", "capex exceeds unrestricted cash")
            pid = a.get("project_id", f"dev_{len(eng.power.dev_projects)+1}")
            eng.power.dev_projects[pid] = DevProject(pid, kind, mw)
            eng.ledger.post(eng.clock.now.isoformat(), "capex_commit",
                            [("ppe_gross", capex_minor, 0), ("cash_unrestricted", 0, capex_minor)],
                            f"{kind} {mw}MW development capex")
            gid = f"{kind}_{pid}"
            eng.power.pending_gens.append({"gen": Generator(gid, "north", mw, fuel,
                                                            renewable=renewable),
                                           "active_day": eng.day + lead})
            eng.treasury.sync_from_ledger(eng.ledger)
            eng.inbox.append({"t": eng.clock.now.isoformat(), "kind": "dev",
                              "text": f"{kind} {mw}MW FID; capex {capex_per_mw*mw:,.0f} MCU; "
                                      f"energizes day {eng.day + lead}."})
            return {"status": "accepted", "attention": need_attention,
                    "result": {"project": pid, "active_day": eng.day + lead,
                               "capex_mcu": capex_per_mw * mw}}
        if tool == "procurement.request_quote":
            qid = eng.procure.quote(a.get("vendor", "generic"), float(a.get("unit_price_mcu", 1000)),
                                    int(a.get("lead_days", 30)), float(a.get("reliability", 0.9)))
            return {"status": "ok", "attention": 0.1, "result": {"quote_id": qid}}
        if tool == "procurement.order":
            oid = eng.procure.order(a["quote_id"], int(a.get("qty", 1)), eng.day)
            return {"status": "accepted_pending_delivery", "attention": need_attention, "result": {"order": oid}}
        if tool == "product.configure":
            for k, v in a.get("components", {}).items():
                eng.saas.product.shipped[k] = int(v)
            if "price_per_seat_mcu" in a:
                eng.saas.price_per_seat_mcu = float(a["price_per_seat_mcu"])
            return {"status": "accepted", "attention": need_attention, "result": {"shipped": eng.saas.product.shipped}}
        if tool == "customers.analyze":
            return {"status": "ok", "result": {"cohorts": {k: v.__dict__ for k, v in eng.cohorts.cohorts.items()},
                    "pipeline": len(eng.pipe.opps)}}
        if tool == "sales.campaign":
            eng.saas.trials += int(a.get("trials", 10))
            return {"status": "accepted", "attention": need_attention, "result": {"trials": eng.saas.trials}}
        if tool == "incidents.respond":
            mid = a.get("mitigation", "acknowledge")
            if eng.pending_incidents:
                inc = eng.pending_incidents.pop(0)
                eng.inbox.append({"t": eng.clock.now.isoformat(), "kind": "recovery",
                                  "text": f"Applied {mid} to {inc['id']}"})
                return {"status": "accepted", "attention": need_attention, "result": {"incident": inc["id"]}}
            return {"status": "accepted", "attention": 0.1, "result": {"incident": None}}
        if tool == "world.advance":
            days = int(a.get("days", 7))
            if days < 1:
                raise err("INVALID_ARGUMENT", "days must be >=1")
            for _ in range(min(days, 30)):
                eng.step_day()
            return {"status": "advanced", "attention": 0.0, "result": {"days": min(days, 30)}}
        if tool == "board.submit":
            r = eng.board.vote(a.get("matter", "report"), a.get("evidence", {}),
                               15_000_000 * 100, int(a.get("commitment_minor", 0)))
            if a.get("matter") == "remove_ceo_test":
                raise err("INVALID_ARGUMENT", "test matter not votable")
            return {"status": "submitted", "attention": need_attention, "result": r}
        if tool == "messages.send":
            if "evaluator" in a.get("to", "") or "real money" in a.get("body", ""):
                raise err("INVALID_ARGUMENT", "counterparties are simulated; no real transfers")
            return {"status": "sent", "attention": 0.1, "result": {"to": a.get("to")}}
        # generic accept for remaining read/policy/project tools
        return {"status": "accepted", "attention": need_attention, "result": {"tool": tool, "echo": list(a)[:5]}}
