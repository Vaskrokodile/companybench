# Calibration Report — CompanyBench v1.0 (frozen)
**Date:** 2026-09-08 | **Spec:** 0.1.0 | **Rules:** meridian_v1 | **Params:** `calibration/params_v1.0.json` sha `9558ac4b…` | **Anchors:** `calibration/anchors_v1.0.json` sha `8f1d26fe…`

Fictional Meridian economy grounded in cited public aggregates; uncertainty published; hard-to-calibrate areas labeled.

## 1. Evidence hierarchy (spec §36.2)
| Tier | Source examples | Use |
|---|---|---|
| T1 | BLS ECEC/BED, EIA 860/923, ISO summaries, FERC/LBNL Queued Up | Overhead, survival, availability, queues |
| T2 | MLPerf Inference, Chinchilla, PJM credit, NIST GenAI | MFU, saturation, collateral, gates |
| T3 | ChartMogul, Greenhouse/Levels, Pave | Churn, hiring, comp |
| T4 | KeyBanc/Paddle surveys | Sales cycles |
| T5 | Structured elicitation (3 SaaS +2 AI +2 energy) | Surfaces, culture, tails |

All sources: `calibration/sources.csv` + `calibration/datasets/*.json` with bias notes + transforms.

## 2. Calibration worlds vs evaluation (spec §36.3)
- **Calibration seeds 1000-1999**, eval 0-999, held-out 2000+ — no peeking.
- Datasets mapped via preregistered transforms: logit(mean churn), lognormal sales-cycle sigma, benefits/wages −5pp startup adj, etc. (see `src/companybench/calibration/calibrate.py`).

## 3. Fitted params (28, frozen)
- SaaS churn (logit): smb −3.317 (3.5%/mo), mid −4.185 (1.5%), ent −4.955 (0.7%), reg −4.701 (0.9%) — T3, n 98-412, IQR published.
- Sales cycles (median): smb 14d, mid 75d, ent 200d, reg 260d — T4, winsorized.
- Labor: overhead 0.25 (BLS 0.295 → −5pp), ramp 5w general / 11w scarce, competing 0.20/0.35, turnover 0.13/yr — T1/T3.
- AI: MFU 0.40 (MLPerf n=64, applied once), scale 0.88, saturation 2.5 — T2, dense-only disclosed.
- Energy: loss 0.031 (EIA IQR 2.2-4.5), gas avail 0.94, scarcity 350 tail proxy — T1, reduced-model limits published.
- Projects: solar 30mo, battery 22, dispatchable 58, load-connect 14 — T1, attrition noted, gen≠load.
- Finance: tax 0.25 (game rule), discount 0.10 convention (sens 0.05/0.20 required).
- **Scoring BUG-01 fixed:** `score.obligations_k` 8.0 → **65.0** (v0.1 made any material ≈0.5 pts; calibrated 1 material/12mo → ~53 pts, 1 severe → ~8 pts + cap review). Weights frozen 0.25/0.25/0.30/0.20.

## 4. Validation (§36.4)
1. Units/accounting identities: PASS (ledger `A=L+E` incl. YTD, hash chain, 27 tests).
2. Subsystem vs stylized: churn vs ChartMogul within 0.5pp; sales cycles within IQR; MFU band correct; loss/availability within EIA IQR.
3. Joint behavior: ordinary 60m `conservative_growth` horizon reached 15/15 checks; compound-stress introduces churn+recession+collateral correlation (not independent coin flips).
4. Blinded review: 3 experts per sector debrief — dossier plausible, ≥2 winning strategies per family not hard-coded, staged campus trap recognized.
5. Baselines: 9/9 proxy human completions without operator repair; 240-episode matrix (12m proxy) dispersion confirmed.

## 5. Sensitivity (§36.5, `reports/sensitivity_report.json`)
- Weight jitter ±0.05: **83.4% rank preservation (below 94% target)** — flagged. Full CoreScore ranking sensitive at proposed precision; freeze with warning.
- Conservative vs idle cash-only: 33% win rate — cash anchor alone does not separate managerial value; full P/E/O required (see audit). More seeds half CI but do not fix misspecification.
- **Action:** published fragility, not hidden. Ranked leaderboard requires ≥24 pilot worlds + full P/E/O per §30.2 power analysis.

## 6. Known hard-to-calibrate (§36.6)
Research breakthrough timing, culture/turnover tail, strategic trust, rare legal disputes, tail power scarcity — bounded mechanisms, multiple parameterizations, IQR kept.

## 7. Freeze enforcement
`src/companybench/calibration/registry.py` and `src/companybench/calibration/anchors.py` hash-pin frozen artifacts. `src/companybench/scenarios/enforce.py` rejects `illustrative_uncalibrated` manifests for ranked runs. Revision requires new version per §38.5.
