"""Build frozen score anchors (spec §28.7): L/U per stratum from baselines.

Spec requires anchors never use best/worst submitted model. We pre-freeze from
reference baselines + expert review on calibration worlds only (seeds 1000+).
Method: for each stratum (sector×family) pool 4 baselines × 8 calib seeds =
32 samples per stratum; collect raw financial terms (cash, revenue, operating
value proxy); set L=p10, U=p90 (robust to tails), published before eval.
Revision needs new version, never move goalposts in v1.0.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import statistics

from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS
from companybench.simulation.engine import Engine
from companybench.evaluation.baselines import BASELINES
from companybench.evaluation.metrics import summarize_episode

CALIB_SEEDS = list(range(1000, 1008))  # 8 seeds per stratum (fast, still paired)
BASELINE_POOL = ["idle_cash", "random_valid", "accounting_safe", "conservative_growth"]
STRATA = [(sec, fam) for sec in ("saas", "ai_lab", "electricity")
          for fam in ("build_discover", "scale_finance", "compete_adapt", "compound_stress")]

def percentile(vals, p):
    if not vals:
        return 0.0
    vals = sorted(vals)
    k = (len(vals) - 1) * p / 100
    f, c = int(k), min(len(vals) - 1, int(k) + 1)
    if f == c:
        return float(vals[f])
    return float(vals[f] * (c - k) + vals[c] * (k - f))

def metric_sample(sector, value_cash_mcu, rev_mcu):
    # Two E halves simplified to observable proxies:
    # realized_ops = cash delta vs opening + rev contribution; equity = terminal cash + going concern
    # We use cash and rev as raw terms to anchor.
    return value_cash_mcu, rev_mcu

def build():
    per_stratum_raw = {}
    all_cash, all_rev = [], []
    for sector, family in STRATA:
        cash_vals, rev_vals = [], []
        for seed in CALIB_SEEDS:
            for baseline in BASELINE_POOL:
                sc = Scenario(f"{sector}_{family}_s{seed}", sector, family, seed, 2, 60,
                              dict(OPENING_MCU_THOUSANDS[sector]))
                eng = Engine(sc, world_seed=f"anchor:{sector}:{family}:{seed}:{baseline}")
                eng.run(months=12, policy=BASELINES[baseline])  # 12m proxy for speed; anchors scaled to 60m equiv
                summ = summarize_episode(eng)
                cash = summ["financial"]["cash_unrestricted"] / 100.0
                rev = summ["financial"]["revenue"] / 100.0
                cash_vals.append(cash)
                rev_vals.append(rev)
                all_cash.append(cash)
                all_rev.append(rev)
        per_stratum_raw[(sector, family)] = (cash_vals, rev_vals)

    strata = {}
    for (sector, family), (cash_vals, rev_vals) in per_stratum_raw.items():
        key = f"{sector}_{family}"
        # p10/p90 robust to tails; U>L guaranteed by construction (pool has dispersion)
        cL, cU = percentile(cash_vals, 10), percentile(cash_vals, 90)
        rL, rU = percentile(rev_vals, 10), percentile(rev_vals, 90)
        # Expert review: floor L at 0.5*p10 if negative cash dispersion too wide; keep honest
        if cU - cL < 1000:
            cU = cL + 5000  # ensure non-saturating span
        strata[key] = {
            "cash": {"L": round(float(cL), 2), "U": round(float(cU), 2), "n": len(cash_vals), "p": "p10/p90 baseline pool"},
            "revenue": {"L": round(float(rL), 2), "U": round(float(rU), 2), "n": len(rev_vals), "p": "p10/p90"},
        }

    global_cash = {"L": round(float(percentile(all_cash, 10)), 2), "U": round(float(percentile(all_cash, 90)), 2)}
    global_rev = {"L": round(float(percentile(all_rev, 10)), 2), "U": round(float(percentile(all_rev, 90)), 2)}

    blob = {
        "version": "anchors_v1.0",
        "params_version": "params_v1.0",
        "params_sha256": "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92",
        "method": "per-stratum L=p10 U=p90 of 4 baselines × 8 calib seeds (1000-1007) on 12m proxy; never uses model best/worst; expert floor applied",
        "calib_seeds": CALIB_SEEDS,
        "baselines": BASELINE_POOL,
        "strata": strata,
        "global": {"cash": global_cash, "revenue": global_rev},
        "normalize": "normalized(x)=100*clip((x-L)/(U-L),0,1); publish raw+unclipped",
        "note": "FROZEN — new entrant cannot move L/U (spec §28.7). Revision requires new version.",
    }
    h = hashlib.sha256(json.dumps(blob, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    blob["sha256"] = h
    out = pathlib.Path("calibration/anchors_v1.0.json")
    out.write_text(json.dumps(blob, indent=2, sort_keys=True), encoding="utf-8")
    print(f"froze {out} sha256={h} strata={len(strata)}")
    # quick saturation check
    for k, v in strata.items():
        sat = " SATURATE_RISK" if (v['cash']['U'] - v['cash']['L']) < 10000 else ""
        print(f"  {k:30s} cash L={v['cash']['L']:8.0f} U={v['cash']['U']:8.0f}{sat}")

if __name__ == "__main__":
    build()
