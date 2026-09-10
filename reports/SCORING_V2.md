# CompanyBench v1.1 — Agent-Sensitive Scoring

**Problem found (v1.0 proxy):** scores were world-determined, not agent-determined.
`devin`, `glm-5.2` posted *literally identical* per-episode CoreScores (80.00) because:

- Cash was outflow-only — `invoice_issue`/`collect` existed in the ledger but the
  engine never called them. E = opening − payroll − costs, pure world RNG.
- P saturated on action *counts* (trials pool, experiment count), not outcomes.
- O ignored the real incident log; `incidents.respond` was unscored.
- Insolvency was unreachable (no path set `liquidation`) → V=100 for all.
- Electricity had zero agent levers (mechanical dispatch, fixed loads).

## v1.1 changes

**Engine (`simulation/engine.py`, `interface/tools.py`, `sectors/electricity/power.py`)**
- Working capital: SaaS bills MRR monthly to receivables; both sectors collect
  92%/mo of receivables to `cash_unrestricted` (double-entry preserved).
- Real insolvency: 3 consecutive negative-cash months → liquidation → episode ends.
- Growth costs cash: `sales.campaign` 200 MCU/trial (sales_expense),
  `research.run_experiment` 1500·log_compute MCU (rd_expense).
- `product.configure` accepts `fix_defects` (4k MCU/defect) — a real controls lever.
- Electricity is now playable: `energy.develop_project` takes capex and energizes a
  real generator after a lead time (solar 300d/35k MW, wind 270d/40k, gas 210d/45k,
  battery 120d/40k); `energy.submit_connection` kind=load ramps `dc_prospect`
  demand over ~120 days. Sign load → build capacity → serve it (or eat unserved).
- `contracts.sign` {matter:"license"} for ai_lab: enterprise license prepays up to
  5M MCU cash, gated on best eval gain ≥ 0.25 — research becomes monetizable.
- Every fired incident is recorded in `eng.incident_log` (class, severity,
  window); `incidents.respond` marks it resolved with response latency.

**Scorer (`evaluation/scoring_v2.py`)** — same frozen weights 0.25V+0.25P+0.30E+0.20O:
- V: unchanged formula; now reachable-failure (insolvency).
- P: outcomes — saas `70·min(1,mrr/300k)+30·fit`; ai_lab `60·min(1,best_gain/0.9)+40·min(1,evals/12)`;
  elec `55·served_frac + 45·min(1,delivered/2e6)`.
- E: `0.5·norm(cash) + 0.5·norm(revenue)` vs frozen per-stratum anchors
  (ai_lab cash-only — degenerate revenue anchor).
- O: real `incident_log` with resolution-quality burden weights
  (prompt 0.4× / late 1.0× / never 2.0×; unresolved severe caps 25, terminal → 0)
  plus end-state signals (treasury distress, unserved>8k severe/>50k terminal,
  saas defects>4).

## Comparative results (60m Core, 24 episodes each)

| Agent | Core | Survival | saas | ai_lab | electricity | LH 120m |
|---|---|---|---|---|---|---|
| **swe-2** | **91.24** | 24/24 | 91.8 | 91.4 | 90.5 | 93.5 |
| glm-5.2 | 82.91 | 22/24 | 83.1 | 76.6 | 89.1 | 79.3 |
| muse-spark-1.2 | 67.80 | 24/24 | 70.5 | 57.2 | 75.7 | 73.0 |
| revenue_maximizer | 67.50 | 24/24 | 71.1 | 47.2 | 84.2 | — |
| sector_expert | 64.82 | 24/24 | 66.4 | 58.9 | 69.2 | — |
| conservative_growth | 60.10 | 24/24 | 64.0 | 47.2 | 69.2 | — |
| idle_cash | 54.24 | 24/24 | 46.4 | 47.2 | 69.2 | — |
| accounting_safe | 54.24 | 24/24 | 46.4 | 47.2 | 69.2 | — |
| short_horizon_optimizer | 52.50 | 24/24 | 41.1 | 47.2 | 69.2 | — |

Ordering now tracks operational competence: growth with cash discipline >
passive survival > destructive play. Examples: revenue_maximizer's dc trap
(182k unserved) now costs it a terminal customer obligation; GLM's ai_lab
dies insolvent on compound_stress s0 and at 120m (no monetization lever
used); swe-2's license signing keeps the lab solvent through 240m.

Frozen artifacts untouched: params `9558ac4b…`, anchors `8f1d26fe…`.
`pytest`: 32/32 pass. Full rows: `reports/comparative_benchmark_v2.json`.
Runner: `run_comparative_benchmark.py`.
