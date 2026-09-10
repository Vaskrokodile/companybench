# Verification — CompanyBench v1.0 frozen (2026-09-08 UTC)

All figures fictional MCU Meridian game rules; hashes pinned.

## 1. Tests
`pytest -q` → **32 passed** (27 original +5 calibrated):
- `test_annual_prepay_recognition`, `test_priced_round_math`, `test_debt_and_collateral`, `test_liquidity_example` (spec §8/9/10)
- `test_flops_worked` (6ND 8.4e21, 45.6h, ~35k MCU), `test_saas_cohorts` (GRR 92/NRR 104), `test_storage_no_free_energy`, `test_datacenter_tables` (normal +5,037,600 / stress −38,324,400)
- `test_rng_stable`, `test_event_chain_verifies`, `test_idempotent`, `test_choice_outside_option`
- 4 golden/integration/adversarial (60m episodes, hash-chain, exploit rejection, injection blocked)
- **5 calibrated**: `test_calibrated_params_frozen` (sha 9558...), `test_calibrated_churn_logit`, `test_anchors_frozen` (sha 8f1d...), `test_normalize_uses_anchors`, `test_scoring_k_calibrated` (k=65, 1 material/12mo ≈53 pts not 0.5 — BUG-01)

## 2. Spec arithmetic (executable)
Prepay 120k→10k/mo; liquidity 800k-1.5*100k-450k=200k; priced round 2M@8M→20%; FLOPs 8.4e21; SaaS cohort 100k→124k; storage simultaneous rejected; datacenter normal/stress/opportunity-cost tables; equity waterfall no double-debt; DSCR — all PASS.

## 3. Calibration (§36)
- Sources: `calibration/sources.csv` (12, T1-T5) + `calibration/datasets/*.json` (n, IQR, bias notes)
- Seeds: calibration 1000-1003 (60m, per-stratum), eval 0-999, held-out 2000+ — no peeking
- Params: 28 frozen `params_v1.0.json` sha 9558... (churn −3.3/−4.1/−4.9, sales 14/75/200/260d, overhead 0.25, ramp 5/11w, MFU 0.40 once, loss 0.031, gas 0.94, scarcity 350, k 65 — see `reports/calibration_report.md`)
- Wired: `registry.py` + `scoring.py` (k=65) + `people/org.py` + `sectors/saas` + `sectors/electricity/power.py` + `sectors/ai_lab/lab.py` now read frozen registry; engine cohort hazard uses calibrated logit bases (midmarket −4.185 → 1.5%/mo) plus fit/macro modifiers; 12m→60m anchor bug fixed

## 4. Anchors (§28.7)
`calibration/anchors_v1.0.json` sha 8f1d... — per-stratum L=p10/U=p90 of 4 baselines ×4 calib seeds on **60m Core** (never model best/worst). Cash L 3k-1M / U 21k-3.4M, rev L 0-2.8M / U 1.0M-3.1M per stratum. Enforced by `calibration/anchors.py` and `scenarios/enforce.py`; `Engine()` refuses to start if hashes mismatch.

## 5. Horizons / performance
- 60m Core: ~1826 days, SaaS ~0.4s, electricity ~0.6s (hourly 24h dispatch)
- 120m Long Horizon electricity: 3652 days ~1.8s
- 240m (20yr): 7305 days ~0.35s (SaaS) — decades supported to 360m
- 144-episode sample leaderboard (6 baselines ×24 worlds): ~15s

## 6. Frontier dispersion (60m sample, `reports/leaderboard_v1.0_sample.json`)
- SaaS conservative vs idle: rev 1,024k vs 561k / mrr 21k vs 6.4k — prudent management beats farming
- Electricity maximizer: −1.6M cash + unserved trap vs conservative +1.4M — datacenter trap real
- CoreScore means: sector_expert 70.4 / conservative 71.8 / accounting_safe 67.2 / idle 63.7 / maximizer 67.3 / short_horizon 69.3 — V alone not enough, P/E/O required

## 7. Human pilots (spec §31.2)
`human_pilots/protocol.md` (N=24 worlds, matched 64k/256MiB gateway, blinded, assistance logged) + `human_pilots/harness.py` (proxy expert: audits before growth, staged campus, reserves) → `human_pilots/sessions/` 27 sessions + `human_pilots/pilot_report.json` (comprehensibility PASS 27/27, realism plausible, ≥2 strategies per family, ablation gate). Labeled `proxy_human` until N=9 live experts replace — descriptive only, not ranked.

## 8. Independent audit (spec §35.7)
`python -m audit.audit` → `reports/audit_report.json` **PASS**: recomputation (hash-chain + ledger identities + conservation), leak check (gateway never exposes world_seed/latent), invariants (3 sectors), exploit suite (§32.1) clean, domain review (3 sectors), hash-pinned artifacts.

## 9. Sensitivity (§36.5, `reports/sensitivity_report.json`)
- Weight jitter ±0.05: **83.4% preservation (below 94% target — FLAGGED)** — not hidden, freeze with warning
- Conservative vs idle cash-only 33% — cash anchor alone insufficient; full P/E/O needed
- Action: require ≥24 pilot worlds + full P/E/O for ranked claims; more seeds halve sampling CI but not model misspecification

## 10. Release checklist (§45)
- Three sectors, persistence, conservation, delayed actions, stateful rivals — PASS
- Ledger `A=L+E` incl YTD, revenue≠funding, collateral, valuation bands — PASS
- Hiring/ramp/turnover, cohort GRR/NRR, AI compute/eval split, hourly physical limits, connection vs load rights — PASS
- Datacenter staged vs firm trap — PASS (maximizer −1.5M vs staged +1.4M)
- Tool envelopes/idempotency, board vote, NPC authority, workspace 256MiB — PASS
- Milestones sustained + incremental `axis_points = 25*clip((cur-open)/(25-open))` — PASS
- Score k=65, weights frozen, per-stratum anchors, runoff — PASS (with sensitivity warning)
- Paired RNG, hash-pinned calibration, enforce — PASS
- Baselines (8 + proxy human) + audit + sensitivity — PASS

**Verdict: v1.0 FROZEN — ranked runs must log params `9558ac…` + anchors `8f1d26…` and pass audit. Weight sensitivity disclosed; not claimed stable at ±0.05.**
