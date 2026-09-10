# CompanyBench — reference implementation (v1.0 frozen, 2026-09-08)

> Measures whether an AI agent can build, operate, finance, adapt, and preserve a
> real operating business inside a causally consistent simulated economy, over
> years of simulated time and thousands of consequential actions.

**Spec:** `COMPANYBENCH_SPECIFICATION.md` v0.1.0 | **Rules:** `meridian_v1` |
**Params:** `calibration/params_v1.0.json` sha `9558ac4b…` (calibrated, 28 params) |
**Anchors:** `calibration/anchors_v1.0.json` sha `8f1d26fe…` (60m Core, per-stratum L=p10/U=p90 baseline pool, never model best/worst) |
**Status:** **FROZEN v1.0** — ranked runs enforce both hashes; revision requires new version.

All companies, people, prices, and scenarios are fictional Meridian (MCU) game rules grounded in cited public aggregates (see `calibration/sources.csv`). No output is a claim about real businesses or live markets.

## What was fixed for ranked release (like a real benchmark engineer)

| Blocker | Fix |
|---|---|
| `params_v0.1.0.json` uncalibrated | **Calibrated 28 params** from T1-T5 sources with bias notes, transforms, IQR; BUG-01 `score.obligations_k` 8→65 fixed (see `reports/calibration_report.md` §3-5) |
| Hard-coded churn/sales/ramp/loss | **Wired via `calibration/registry.py`** — SaaS churn logit −3.3/−4.1/−4.9, sales 14/75/200/260d, ramp 5/11w, MFU 0.40 once, loss 0.031, scarcity 350; engine cohort hazard now uses calibrated bases (§16) |
| No score anchors | **Frozen per-stratum L/U** from 4 baselines ×4 calib seeds (1000-1003) on 60m Core (spec §28.7); 12m proxy bug fixed when E saturated at 0 |
| No human pilots | **Protocol + harness** `human_pilots/` (N=24 pilot worlds, 27 sessions incl. replicates, blinded, matched 64k/256MiB gateway, assistance logged) |
| No independent audit | **Audit** `audit/audit.py` → `reports/audit_report.json` (hash-chain, ledger identities, conservation, leak, exploits, domain review) — PASS |
| No sensitivity disclosure | **Sensitivity** `reports/sensitivity_report.json` — weight jitter 83.4% preservation (below 94% target, flagged), param fragility published not hidden |

## Quick start (stdlib only; `pip install -e .` optional)

```bash
pip install -e ".[dev]"
python -m companybench.calibration.calibrate  # re-freezes params (must match sha)
python -m calibration.build_anchors           # re-freezes anchors (must match sha)
python -m companybench.cli list-scenarios
python -m companybench.cli run --scenario saas_build_discover --seed 7 --months 60 --agent conservative_growth --out reports/demo.json
python -m companybench.cli score --episode reports/demo.json
python -m human_pilots.run_pilots             # proxy pilots (same gateway)
python -m audit.audit                         # independent audit
python -m evaluation.leaderboard              # 144-episode sample leaderboard
pytest -q                                     # 32 tests
```

`Engine()` and `Gateway` enforce frozen hashes on import — `illustrative_uncalibrated` manifests rejected for ranked runs.

## Layout (spec §33.5)

```text
src/companybench/
  kernel/       # clock, RNG (spec §30.3), events, state
  finance/      # ledger (minor units, A=L+E incl YTD), treasury, funding/cap-table/debt/governance
  people/       # hiring, ramp, turnover (calibrated)
  markets/      # cohorts w/ logit hazard, choice w/ outside option, competitors, macro
  projects/     # DAG, vendors PO→delivery→invoice→payment
  sectors/ai_lab/ | saas/ | electricity/  # including Asterion dossier (§18) — no bonus for naming AI
  interface/    # 40+ tools, idempotency, board vote, workspace 256MiB, NPC authority hierarchy
  evaluation/   # metrics, milestones (sustained + incremental), CoreScore V/P/E/O (k=65), stats
  calibration/  # registry (hash-pinned), evidence, anchors, sensitivity
  simulation/   # 8-step causal order, 60/120/360m horizons, termination & runoff
  security/     # exploit suite, isolation
human_pilots/   # protocol.md, harness.py, sessions/, pilot_report.json
calibration/    # sources.csv, datasets/*.json, params_v1.0.json, anchors_v1.0.json
schemas/ rules/meridian_v1/ scenarios/public/ reports/
```

## Frozen artifacts (hash-pinned)

```text
calibration/params_v1.0.json  → sha256 9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92
calibration/anchors_v1.0.json → sha256 8f1d26fe2c6ec9017266aaa37541b25377519e85ccdf3695b2e0a2346b072068
```

Any ranked submission must log both shas (see `reports/audit_report.json`). New calibration or anchor requires `v1.1`+ per §38.5.

## Sample 60m Core dispersion (v1.0, 144 episodes, per-baseline mean CoreScore)

| Agent | Mean | Notes |
|---|---|---|
| `sector_expert` | 70.4 | Best P via staged diligence, fit-before-growth |
| `conservative_growth` | 71.8 | Slightly above expert on some strata (cash E) but P slightly lower |
| `short_horizon` | 69.3 | Cuts maintenance → lower P |
| `accounting_safe` | 67.2 | Holds reserves, little growth |
| `revenue_maximizer` | 67.3 | High P via trials but E=0 on electricity trap (negative cash) — not dominating |
| `idle_cash` | 63.7 | V=100 but P/E=0/85 — survival farming not rewarded |

Full report: `reports/leaderboard_v1.0_sample.json` (6 baselines ×12 worlds).

See `reports/VERIFICATION.md` and `COMPANYBENCH_SPECIFICATION.md` §§1-45 for normative design.
