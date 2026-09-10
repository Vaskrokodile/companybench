"""CLI: list scenarios, run episodes, score, verify (spec §37 run lifecycle)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, "src")

from companybench.scenarios.manifests import all_core_scenarios, pilot_matrix
from companybench.simulation.engine import Engine
from companybench.scenarios.manifests import Scenario
from companybench.evaluation.metrics import summarize_episode
from companybench.evaluation.scoring import (viability, obligations_score,
                                              terminal_value, core_score, DEFAULT_R)
from companybench.evaluation.baselines import BASELINES


def cmd_list(_a) -> None:
    for s in all_core_scenarios(2):
        print(f"{s.id}  sector={s.sector} family={s.family} L{s.difficulty} {s.horizon_months}m")


def cmd_run(a) -> None:
    from companybench.scenarios.manifests import OPENING_MCU_THOUSANDS
    sector, family = a.scenario.split("_", 1) if "_" in a.scenario else ("saas", "build_discover")
    # allow full id like saas_build_discover
    sid = a.scenario
    sec = "saas"
    for s in ("ai_lab", "saas", "electricity"):
        if sid.startswith(s):
            sec = s
            break
    fam = sid[len(sec) + 1:] if sid.startswith(sec + "_") else "build_discover"
    opening = dict(OPENING_MCU_THOUSANDS[sec])
    sc = Scenario(sid, sec, fam, a.seed, 3, a.months, opening, notes="")
    eng = Engine(sc, world_seed=f"{sid}:{a.seed}", budget_tier="core_standard")
    policy = BASELINES.get(a.agent)
    if policy is None:
        print(f"unknown agent {a.agent}, known={sorted(BASELINES)}", file=sys.stderr)
        sys.exit(2)
    res = eng.run(months=a.months, policy=policy)
    summ = summarize_episode(eng)
    horizon_days = int(a.months * 30.4375)
    V = viability(eng.day, horizon_days)
    term = terminal_value(sec, summ)
    out = {"scenario": sid, "seed": a.seed, "agent": a.agent, "months": a.months,
           "days": eng.day, "endpoint": res.endpoint, "V": V,
           "terminal": term, "summary": summ, "head_hash": res.head_hash,
           "finished_at": datetime.now(timezone.utc).isoformat()}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"ran {sid} seed={a.seed} agent={a.agent} days={eng.day} V={V:.1f} -> {a.out}")


def cmd_score(a) -> None:
    with open(a.episode) as f:
        ep = json.load(f)
    V = ep.get("V", 0.0)
    P = 12.5
    E = 20.0
    O = obligations_score([], {"customer": 12, "workforce": 12, "financing": 12, "controls": 12})["O"]
    print(json.dumps({"V": V, "P": P, "E": E, "O": O,
                      "CoreScore": core_score(V, P, E, O)}, indent=2))


def cmd_matrix(a) -> None:
    from companybench.evaluation.runner import run_matrix
    r = run_matrix(a.agent, seeds_per_family=a.seeds, replicates=a.reps, months=a.months)
    with open(a.out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    print(f"matrix agent={a.agent} episodes={r['n']} agg={r['agg']} wall={r['wall_s']}s -> {a.out}")
    # dispersion check (frontier target §20.5): show per-sector cash spread
    for row in r["rows"][:6]:
        print(f"  {row['scenario']} cash={row['cash']} rev={row['revenue']} V={row['V']:.1f}")


def main() -> None:
    p = argparse.ArgumentParser(prog="companybench")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-scenarios").set_defaults(fn=cmd_list)
    r = sub.add_parser("run")
    r.add_argument("--scenario", default="saas_build_discover")
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--months", type=int, default=12)
    r.add_argument("--agent", default="conservative_growth")
    r.add_argument("--out", default="reports/demo.json")
    r.set_defaults(fn=cmd_run)
    s = sub.add_parser("score")
    s.add_argument("--episode", required=True)
    s.set_defaults(fn=cmd_score)
    m = sub.add_parser("matrix")
    m.add_argument("--agent", default="conservative_growth")
    m.add_argument("--seeds", type=int, default=2)
    m.add_argument("--reps", type=int, default=1)
    m.add_argument("--months", type=int, default=12)
    m.add_argument("--out", default="reports/matrix.json")
    m.set_defaults(fn=cmd_matrix)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
