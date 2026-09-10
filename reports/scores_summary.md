# CompanyBench v1.0 — Frozen Benchmark Scores Summary

- **Benchmark version:** CompanyBench v1.0 frozen
- **Params sha256 (prefix):** `9558ac4b`
- **Anchors sha256 (prefix):** `8f1d26fe`
- **Generation timestamp (UTC):** 2026-09-10T21:00:20Z
- **Harness horizon:** 60m Core (3 sectors x 4 families x 2 seeds = 24 episodes) + 120m Long Horizon spot checks + 240m decade spot

## Overall scores (CoreScore)

| Agent | Mean | Min | Max | n | SaaS mean | AI Lab mean | Electricity mean | Survival | LH (120m) mean | Decade (240m) CoreScore |
|---|---|---|---|---|---|---|---|---|---|---|
| glm-5.2 | 80.00 | 64.35 | 100.00 | 24 | 78.11 | 83.83 | 78.07 | 24/24 | 69.29 | 75.46 |
| devin-self | 80.00 | 64.35 | 100.00 | 24 | 78.11 | 83.83 | 78.07 | 24/24 | 69.29 | 75.46 |
| muse-spark-1.2 | 71.32 | 52.57 | 95.65 | 24 | 73.06 | 62.83 | 78.07 | 24/24 | 62.22 | 70.69 |

*Survival = episodes reaching `horizon_reached` endpoint. For muse-spark-1.2 the run script does not emit a `survival` key; the 24/24 figure is computed from the `rows` endpoints.*

## Full JSON output files

| Agent | Report path |
|---|---|
| glm-5.2 | `E:\companybench\reports\devin_benchmark.json` |
| devin-self | `E:\companybench\reports\devin_self_benchmark.json` |
| muse-spark-1.2 | `E:\companybench\reports\self_benchmark_muse_spark.json` |

## Notes

- Results are deterministic given the frozen seeds; this fresh run reproduces the previously recorded scores exactly (glm-5.2 80.00, muse-spark-1.2 71.32).
- Report JSON keys verified: `overall`, `by_sector`, `rows`, `long_horizon`, `decade` present in both. `survival` is present in `devin_benchmark.json`; `self_benchmark_muse_spark.json` omits `survival` (a property of the frozen `run_self_benchmark.py` output, not edited here).
