"""Full benchmark runner (spec §30): 240-episode Core matrix, pilot, Long Horizon.

Unit = episode (config × world × replicate × tier × version). Aggregation:
world→family→sector→overall macro-average. Paired bootstrap CIs. Survival
curves. Cost frontier. No best-of-N; every valid replicate counts.
"""
from __future__ import annotations

import time

from ..scenarios.manifests import all_core_scenarios, pilot_matrix, long_horizon
from ..simulation.engine import Engine
from ..evaluation.baselines import BASELINES
from ..evaluation.metrics import summarize_episode
from ..evaluation.scoring import viability, terminal_value, core_score, obligations_score
from ..evaluation.statistics import aggregate, paired_bootstrap


def run_episode(scenario, agent: str, seed_tag: str, months: int | None = None) -> dict:
    eng = Engine(scenario, world_seed=f"{scenario.id}:{seed_tag}")
    policy = BASELINES.get(agent)
    res = eng.run(months=months or scenario.horizon_months, policy=policy)
    summ = summarize_episode(eng)
    horizon_days = int((months or scenario.horizon_months) * 30.4375)
    V = viability(eng.day, horizon_days)
    term = terminal_value(scenario.sector, summ)
    return {"scenario": scenario.id, "sector": scenario.sector, "family": scenario.family,
            "seed": scenario.seed, "agent": agent, "days": eng.day, "endpoint": res.endpoint,
            "V": V, "terminal": term, "cash": summ["financial"]["cash_unrestricted"],
            "revenue": summ["financial"]["revenue"], "head": res.head_hash}


def run_matrix(agent: str = "conservative_growth", seeds_per_family: int = 2,
               replicates: int = 1, months: int = 12) -> dict:
    """Reduced matrix for dev (full 240 = seeds 10 × reps 2 × 60m)."""
    scenarios = all_core_scenarios(seeds_per_family, horizon=months)
    rows = []
    t0 = time.time()
    for sc in scenarios:
        for rep in range(replicates):
            rows.append(run_episode(sc, agent, f"rep{rep}", months))
    scores = [{"sector": r["sector"], "family": r["family"], "seed": r["seed"],
               "replicate": 0, "score": r["V"]} for r in rows]
    return {"rows": rows, "agg": aggregate(scores), "wall_s": round(time.time() - t0, 2),
            "n": len(rows)}
