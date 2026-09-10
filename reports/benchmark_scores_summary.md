# CompanyBench v1.0 — Benchmark Scores Summary

Self-bench via Gateway (60m Core x24 episodes + 120m long-horizon + 240m decade spot).

## Overall CoreScore

| Agent | Harness script | Mean | Min | Max | n | Survival | Gateway calls |
|---|---|---|---|---|---|---|---|
| GLM 5.2 (GLMAgent) | run_devin_benchmark.py | **80.00** | 64.35 | 100.00 | 24 | 24/24 | 26,354 |
| devin-self (DevinSelfAgent) | run_devin_self_benchmark.py | **80.00** | 64.35 | 100.00 | 24 | 24/24 | 18,144 |
| Muse Spark (MuseSparkAgent) | run_self_benchmark.py | 71.32 | 52.57 | 95.65 | 24 | 24/24 | 41,409 |

## Per-sector mean CoreScore

| Agent | saas | ai_lab | electricity |
|---|---|---|---|
| GLM 5.2 | 78.11 | 83.83 | 78.07 |
| devin-self | 78.11 | 83.83 | 78.07 |
| Muse Spark | 73.06 | 62.83 | 78.07 |

## Long Horizon (120m spot checks, build_discover)

| Agent | saas | ai_lab | electricity | LH mean |
|---|---|---|---|---|
| GLM 5.2 | 76.58 | 69.40 | 61.90 | 69.29 |
| devin-self | 76.58 | 69.40 | 61.90 | 69.29 |
| Muse Spark | 72.37 | 52.40 | 61.90 | 62.22 |

All 9 long-horizon episodes reached horizon (3,652 days each).

## Decade run (saas build_discover, 240m)

| Agent | CoreScore | Days | Endpoint | MRR | fit_mid |
|---|---|---|---|---|---|
| GLM 5.2 | 75.46 | 7,305 | horizon_reached | 367,413 | 0.96 |
| devin-self | 75.46 | 7,305 | horizon_reached | 1,098,494 | 0.96 |
| Muse Spark | 70.69 | 7,186 | horizon_reached | 104,498 | 0.651 |

## Frozen parameters

- params_sha256: `9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92`
- anchors_sha256: `8f1d26fe2c6ec9017266aaa37541b25377519e85ccdf3695b2e0a2346b072068`

## Report files (generated_utc)

- reports/devin_benchmark.json — 2026-09-10T21:00:47Z
- reports/devin_self_benchmark.json — 2026-09-10T21:11:52Z (devin-self; Devin's own policy, agents/devin_self.py)
- reports/self_benchmark_muse_spark.json — 2026-09-10T21:02:01Z

**Highest CoreScore: tie — GLM 5.2 and devin-self both scored 80.00; devin-self used the fewest gateway calls (18,144) and reached the highest decade MRR (1,098,494).**

Note: devin-self's per-episode CoreScores are identical to GLM 5.2's on every scenario. Under the harness proxy scorer, P saturates at 100 for any agent that ships midmarket fit + maintains trials (saas) or runs >=5 experiments (ai_lab); V, E, and O are world-RNG-fixed (outflow-only cash, immutable saas defects=5, mechanical electricity dispatch). The scored lever space does not differentiate further.
