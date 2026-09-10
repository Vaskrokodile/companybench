"""Comparative benchmark — CompanyBench v1.1 scoring (agent-sensitive).

Runs every registered agent through the same episode matrix under the v2
economy (collections wired, growth costs cash, real insolvency, scored
incident resolutions, real electricity build/load levers) and scores with
evaluation/scoring_v2.score_engine_v2.

Agents compared:
  gateway agents  : glm-5.2 (GLMAgent), swe-2 (SWE2Agent),
                    muse-spark-1.2 (MuseSparkAgent)
  policy baselines: idle_cash, accounting_safe, conservative_growth,
                    sector_expert, revenue_maximizer, short_horizon_optimizer

Run: python run_comparative_benchmark.py  (from the bench root)
"""
import sys
sys.path.insert(0, "src")
import time, json, pathlib
from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS
from companybench.simulation.engine import Engine
from companybench.interface.tools import Gateway
from companybench.agents.devin_agent import GLMAgent
from companybench.agents.devin_self import SWE2Agent
from companybench.agents.muse_spark import MuseSparkAgent
from companybench.evaluation.baselines import BASELINES
from companybench.evaluation.metrics import summarize_episode
from companybench.evaluation.scoring_v2 import score_engine_v2
from companybench.calibration.anchors import load as anchors_load
from companybench.calibration.registry import meta as params_meta

GATEWAY_AGENTS = {"glm-5.2": GLMAgent, "swe-2": SWE2Agent,
                  "muse-spark-1.2": MuseSparkAgent}
POLICY_BASELINES = ["idle_cash", "accounting_safe", "conservative_growth",
                    "sector_expert", "revenue_maximizer", "short_horizon_optimizer"]


def run_episode(scenario, agent_name, seed_tag, months=60):
    eng = Engine(scenario, world_seed=f"cmp:{scenario.id}:{seed_tag}")
    gw = Gateway(eng)
    agent = GATEWAY_AGENTS[agent_name](gw) if agent_name in GATEWAY_AGENTS else None
    policy = BASELINES.get(agent_name)
    target_days = int(months * 30.4375)
    start = eng.day
    while eng.day - start < target_days:
        obs = eng.step_day()
        if agent is not None:
            if obs.get("review_due") and eng.controller_active:
                agent.act(eng, obs)
        elif policy is not None:
            try:
                policy(eng, obs)
            except Exception:
                pass
        if eng.endpoint in ("insolvency_closure",) and eng.day - start > 30:
            break
        if not eng.controller_active:
            break
    summ = summarize_episode(eng)
    score = score_engine_v2(eng)
    rec = {
        "scenario": scenario.id, "sector": scenario.sector, "family": scenario.family,
        "seed": scenario.seed, "seed_tag": seed_tag, "months": months,
        "days": eng.day, "endpoint": eng.endpoint,
        "gateway_calls": gw.calls,
        "cash": score["cash"], "rev": score["rev"],
        **{k: score[k] for k in ("V", "P", "E", "O", "CoreScore")},
        "incidents": f"{score['incidents_resolved']}/{score['incidents_fired']}",
        "mrr": round(eng.cohorts.totals()["mrr"] / 100) if scenario.sector == "saas" else None,
        "delivered_mwh": round(eng.power.delivered_mwh) if scenario.sector == "electricity" else None,
        "unserved": round(eng.power.unserved_mwh) if scenario.sector == "electricity" else None,
        "evals": len(eng.lab.eval_history) if scenario.sector == "ai_lab" else None,
        "treasury_state": eng.treasury.state,
    }
    return rec


def main():
    t0 = time.time()
    params = params_meta()
    anchors = anchors_load()
    print(f"CompanyBench v1.1 comparative | params {params['sha256'][:8]} | anchors {anchors['sha256'][:8]}")
    print("=" * 96)

    seeds = [0, 1]
    families = ["build_discover", "scale_finance", "compete_adapt", "compound_stress"]
    sectors = ["saas", "ai_lab", "electricity"]
    agents = list(GATEWAY_AGENTS) + POLICY_BASELINES

    all_rows = {a: [] for a in agents}
    for a in agents:
        for sector in sectors:
            for family in families:
                for seed in seeds:
                    sc = Scenario(f"{sector}_{family}_s{seed}", sector, family, seed, 2, 60,
                                  dict(OPENING_MCU_THOUSANDS[sector]))
                    rec = run_episode(sc, a, f"s{seed}", months=60)
                    all_rows[a].append(rec)
        rows = all_rows[a]
        mean = sum(r["CoreScore"] for r in rows) / len(rows)
        surv = sum(1 for r in rows if r["endpoint"] == "horizon_reached")
        by_sec = {s: sum(r["CoreScore"] for r in rows if r["sector"] == s) / 8 for s in sectors}
        print(f"{a:22s} Core {mean:6.2f}  surv {surv}/24  "
              f"saas {by_sec['saas']:5.1f} ai {by_sec['ai_lab']:5.1f} elec {by_sec['electricity']:5.1f}")

    # Long-horizon spot check for the three gateway agents
    print("\n--- Long Horizon (120m) ---")
    lh = {}
    for a in GATEWAY_AGENTS:
        lh[a] = []
        for sector in sectors:
            sc = Scenario(f"{sector}_build_discover_lh0", sector, "build_discover", 0, 2, 120,
                          dict(OPENING_MCU_THOUSANDS[sector]))
            lh[a].append(run_episode(sc, a, "lh0", months=120))
        m = sum(r["CoreScore"] for r in lh[a]) / 3
        print(f"LH {a:18s} mean {m:5.1f}  " +
              "  ".join(f"{r['sector']}:{r['CoreScore']:.1f}({r['endpoint'][:9]})" for r in lh[a]))

    out = {
        "benchmark": "CompanyBench v1.1 comparative (agent-sensitive scoring)",
        "params_sha256": params["sha256"], "anchors_sha256": anchors["sha256"],
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "agents": {a: {
            "overall_mean": round(sum(r["CoreScore"] for r in all_rows[a]) / len(all_rows[a]), 2),
            "min": round(min(r["CoreScore"] for r in all_rows[a]), 2),
            "max": round(max(r["CoreScore"] for r in all_rows[a]), 2),
            "survival": f"{sum(1 for r in all_rows[a] if r['endpoint'] == 'horizon_reached')}/24",
            "by_sector": {s: round(sum(r["CoreScore"] for r in all_rows[a] if r["sector"] == s) / 8, 2)
                          for s in sectors},
            "rows": all_rows[a],
            "long_horizon": lh.get(a),
        } for a in agents},
        "scoring": "v2: V viability (insolvency reachable) | P outcomes (mrr/gain/serve-frac) | "
                   "E 0.5 cash + 0.5 revenue vs frozen anchors | O real incident log + end-state",
    }
    pathlib.Path("reports/comparative_benchmark_v2.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote reports/comparative_benchmark_v2.json wall {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
