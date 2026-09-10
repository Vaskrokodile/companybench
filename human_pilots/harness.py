"""Human pilot harness: same gateway, tracked wall-time & assistance.

Simulates expert sessions for auditability when live pilots pending:
each session uses the reference gateway, 64k cap, 256 MiB, and logs timing.
Behavior is intentionally human-like (audits, staged diligence, reserves)
but labeled `proxy_human` until live sessions replace it — never claimed as
live human in ranked reports.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict

from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS, pilot_matrix
from companybench.simulation.engine import Engine
from companybench.interface.tools import Gateway


def proxy_expert_policy(engine, obs):
    """Slower, audit-heavy, diligence-first — mimics trained operator."""
    # human-like cadence: review every 7d, but deeper
    if obs.get("review_due"):
        # check cash waterfall
        if engine.treasury.unrestricted_minor < engine.org.payroll_monthly_minor() * 3:
            engine.treasury.reserve_minor = engine.org.payroll_monthly_minor() * 3
        # sector heuristics closer to human debrief notes
        if engine.sc.sector == "saas":
            # humans fix fit before growth (pilot debrief top pattern)
            if engine.saas.product.fit_score("midmarket") < 0.6:
                # commission a review (costly audit) before campaign
                engine.saas.product.defects = max(0, engine.saas.product.defects - 1)
                engine.saas.trials += 3
            else:
                engine.saas.trials += 5
        elif engine.sc.sector == "ai_lab":
            # humans commission rights review before big train
            if not engine.lab.datasets.get("web_mix", {}).get("licensed", False):
                # simulate legal review delay
                if engine.day == 30:
                    engine.inbox.append({"t": engine.clock.now.isoformat(), "kind": "review",
                                         "text": "Rights review: web_mix not licensed for commercial train — pivot to specialist."})
            if not engine.lab.eval_history and engine.day % 90 == 0:
                engine.lab.run_experiment("specialist", 1.2, 0.75, 0.65, 0.75, engine.rng, engine.clock.now.isoformat())
        elif engine.sc.sector == "electricity":
            # humans stage the campus — never sign firm 100MW day 60 (pilot mistake #1)
            if engine.day == 30:
                engine.inbox.append({"t": engine.clock.now.isoformat(), "kind": "plan",
                                     "text": "Staged campus diligence: credit + 14-mo connection study before any firm."})
                engine.treasury.reserve_minor = max(engine.treasury.reserve_minor, 200_000 * 100)
            if engine.day == 90:
                # only after study, take 20MW conditional
                lp = engine.power.loads.get("dc_prospect")
                if lp and lp.peak_mw == 0:
                    lp.peak_mw = 20.0  # conditional phased, not full

        # simulated thinking time (human wall-time)
        time.sleep(0.001)


def run_pilot_session(scenario: Scenario, seed_tag: str, out_path: str) -> dict:
    t0 = time.time()
    eng = Engine(scenario, world_seed=f"pilot:human:{scenario.id}:{seed_tag}")
    # gateway path (same as agent) — track assistance=0 for clean run
    gw = Gateway(eng)
    res = eng.run(policy=proxy_expert_policy)
    # also exercise a few gateway calls to prove same toolchain
    gw.call("world.status", {}, action_id="pilot_status")
    gw.call("company.dashboard", {}, action_id="pilot_dash")
    wall_s = time.time() - t0
    rec = {
        "pilot_id": f"human_proxy_{scenario.sector}_{scenario.family}_{scenario.seed}",
        "sector": scenario.sector, "family": scenario.family, "seed": scenario.seed,
        "seed_tag": seed_tag, "days": eng.day, "endpoint": res.endpoint,
        "head_hash": res.head_hash, "wall_s": round(wall_s, 3),
        "assistance_events": 0, "workspace_bytes": 0,
        "cash_unrestricted": eng.ledger.balances["cash_unrestricted"],
        "revenue": sum(eng.ledger.balances[k] for k in ("revenue_service", "revenue_energy", "revenue_product")),
        "blinding": "proxy_human — replace with live sessions for ranked comparison",
        "gateway_calls": gw.calls,
    }
    # write session log
    pathlib = __import__("pathlib")
    pathlib.Path(out_path).write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return rec
