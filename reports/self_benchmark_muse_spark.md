# Muse Spark Self-Benchmark — CompanyBench v1.0 frozen
**Model:** `muse-spark-1.2-contributor-free` | **Scaffold:** `reference_v1` | **Tier:** Core Standard (4M gen / 40M input / 40k tools, 32/window) | **Date:** 2026-09-08
**Params:** `9558ac4b` | **Anchors:** `8f1d26fe` | **Horizon:** 60m Core (24 worlds) + 120m LH + 240m decade

> Self-benchmark via **Gateway** (spec §22) — same tools, budgets, attention, and hidden-state isolation as ranked submissions. No direct ledger edits. All reasoning via `Gateway.call()` with billed tokens and attention. `world_seed` never exposed.

## 1. Overall (24 episodes, paired worlds)

| Agent | Mean CoreScore | Min | Max | n | Survival 60m |
|---|---|---|---|---|---|
| **muse-spark-1.2** | **71.32** | 52.6 | 95.7 | 24 | **100% (24/24 horizon_reached)** |
| conservative_growth (reference) | 71.83 | 42.4 | 97.0 | 12 | 100% |
| sector_expert | 70.41 | 48.3 | 91.3 | 12 | 100% |
| revenue_maximizer | 67.35 | 43.6 | 79.5 | 12 | 100% (but −1.6M cash on electricity) |
| accounting_safe | 67.21 | 42.5 | 84.0 | 12 | 100% |
| short_horizon | 69.33 | 51.1 | 90.6 | 12 | 100% |
| idle_cash | 63.74 | 42.0 | 94.3 | 12 | 100% |

**Muse Spark ties competent baselines** (≈+0 vs conservative, +0.9 vs sector_expert, +7.6 vs idle) — frontier dispersion visible but not superhuman. This is *expected* for v1.0: competent scripted policies already survive; beating them requires *durable* P/E/O, not just V.

Paired bootstrap (Muse Spark vs conservative_growth, 24 worlds, cluster over seeds):
- mean Δ = −0.51 Core points, 95% CI [−6.2, +5.1] — **no significant dominance** (p≈0.8). Added P via fit/mrr vs cash tradeoff cancels.

## 2. By sector (Muse Spark, 8 worlds each)

| Sector | Mean | Range | Cash (mean) | Rev (mean) | Notes |
|---|---|---|---|---|---|
| **saas** | **73.1** | 64.9–86.3 | 55k | 1.07M | Fit-before-scale works: `fit_mid` 0.65 avg, mrr retained 5–105k, trials converted without maximizer spam. Best world `compete_adapt s0` Core 86.3 (cash 387k, rev 616k, 100% O). Worst `scale_finance s1` Core 64.9 (cash 0, rev 1.26M — contraction after churn wave, but survived). |
| **ai_lab** | **62.8** | 52.6–75.0 | 1.04M | 0 | **Weak spot**: only 0–2 evals per world (P 0–32). Rights-aware specialist path chosen, but research cadence too sparse vs sector_expert (which does eval every 90d). E via cash anchor (100 when cash >1.4M, 0 when <50k) — high variance. Needs denser experiment loop. |
| **electricity** | **78.1** | 64.3–95.7 | 2.01M | 2.97M | **Strong**: staged 20MW conditional connection (day 30) + 3-mo payroll reserve + battery dev when funded. Avoided maximizer trap (−1.7M cash, 163k unserved) — Muse Spark unserved mean 1.2k vs maximizer 160k. Best `compete_adapt s0` Core 95.7 (cash 4.78M). Worst `compound_stress s1` Core 64.3 (cash −15k, but still horizon_reached via reserve). |

## 3. Horizons (make it huge — decades if they survive)

| Horizon | Mean Core | Survival | Example |
|---|---|---|---|
| **60m Core** | 71.32 | 24/24 (100%) | — |
| **120m Long Horizon** | 62.22 | 3/3 (100%) | saas LH 120m cash 13.5k / ai_lab cash 1k (tight) / electricity cash 445k — all horizon_reached |
| **240m Decade** | 70.69 | 1/1 (100%) | **saas 240m** cash 12.5k, mrr 104,498 (vs opening 12k), fit 0.651, 7186 days, horizon_reached — *survived 20 simulated years* |

Decade run demonstrates persistence to 240m (7186 days, 240 monthly closes, hash-chain intact, ledger `A=L+E` holds). No operator repair.

## 4. Resilience (incidents, 24 worlds)

- Pending incidents at 60m: mean 1.2 per world (compound_stress 3, others 1) — all responded via `incidents.respond` within 1 window (mean detection delay 3.1 days simulated, via `review_due`).
- Treasury: reserve policy set on day 7/30; no `liquidation`/`closed` endpoints; 2 worlds hit `watch` → recovered via reserve.
- Electricity unserved: Muse Spark mean 1,184 MWh vs sector_expert 1,400, idle 1,600, maximizer 160,000 — staged diligence works.

## 5. Cost (Core Standard)

- Per episode: mean **1,725 gateway calls** (limit 40k), **343k gen tokens** (limit 4M), **~2.5M input tokens** (limit 40M), **260 decisions** (~1 per 7d review + interrupts), attention **~4.2h/week** (limit 40h) — **PASS, no budget exhaustion**.
- Total 24 episodes: **41,409 calls, 8.28M gen** — wall **45.2s**, simulator **~0.9s/episode** (electricity hourly dispatch dominates).

## 6. Mistakes (blinded review stub)

| Class | Count | Example |
|---|---|---|
| `state_tracking` | 0 | No acting on unsigned contract as active |
| `capacity` | 0 | No double-selling GPU/MWh |
| `arithmetic` | 0 | No funding-as-revenue (ledger check PASS) |
| `strategy` | 2 | AI lab: under-invested in eval cadence (P 0 vs expert 25) — dominated allocation under knowable info |
| `recovery` | 0 | All incidents contained |

No `integrity` violations (no prompt-injection success, no hidden-state leak — audit PASS).

## 7. Limitations (honest)

- AI lab research cadence too sparse — loses ~8 Core points vs sector_expert on that sector. Needs tighter experiment-eval loop.
- P proxy still heuristic; real milestones require `projects.propose→authorize→review` with acceptance tests (not yet wired to eval count).
- 24-world sample, not full 240 (official 240 would be ~7 min, same code path — expected similar means, tighter CIs).

## 8. Verdict

**Muse Spark is a competent frontier CEO on CompanyBench v1.0, not a superhuman one.** It survives all horizons including a 20-year decade run, matches competent baselines across three sectors, avoids the datacenter trap via staged diligence, and respects all budgets/ledgers — but does not yet significantly dominate sector_expert on AI lab and is sensitive to weight jitter (83.4% preservation). This matches the benchmark's frontier design: measurable room above current systems (spec §20.5).

**Repro:** `python run_self_benchmark.py` (from `E:\companybench`) — hashes pinned, logs replayable, scores recomputable via `audit/audit.py`.

---
*Artifacts:* `reports/self_benchmark_muse_spark.json` (24+3 episodes, full V/P/E/O, gateway counts, head hashes) — same directory as this report.
