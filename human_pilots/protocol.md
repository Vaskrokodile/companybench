# Human Pilot Protocol — CompanyBench v1.0
**Spec §31.2** | frozen 2026-09-08 | ethics: consented anonymized

## 1. Objective
Provide a descriptive, not rank-claiming, human reference that validates
comprehensibility, realism, and strategy validity — not to claim human vs model
superiority without matched workload.

## 2. Recruitment
- SaaS: founders + finance leads (seed/Series A operator experience, 3+ yr).
- AI lab: research/product/infrastructure leads (shipped production model or API).
- Electricity: energy commercial + project-finance specialists (retail supply or developer).
- N=9 (3 per sector), paid, blinded to model scores, conflict-disclosed.
- Informed consent: fictional MCU economy; no real legal/financial liability;
  data retained as anonymized trajectories + timing.

## 3. Matching constraints (anti-cherry-pick)
- Same rulebook (`rules/meridian_v1/`), same tool gateway (`interface/tools.py`),
  same initial dossiers and inbox, same 256 MiB workspace, same 64k input cap.
- Tutorial: 45-min walkthrough + 2 practice 12-month worlds (not in eval).
- Assigned-sector Core harness: reference scaffold, no external models/planners.
  Assistance events (hint, bugfix, extra time) logged and published; assisted
  trajectories labeled separately per §37.
- Time budget matched to Core Standard inference window: max 8 wall-hours per
  60-month episode, with breaks logged. Team-of-specialists over days is a
  *different track* (reported as such, not compared to single-model Core).

## 4. Instrumentation
- Gateway logs every tool call, wall time, attention hours, workspace writes.
- Blind review: sector experts review trajectories without seeing model labels.
- Missing forecast / extra context assistance recorded as process labels.

## 5. Success criteria (not ranking)
- Comprehensibility: ≥7/9 humans complete 60m without manual operator repair.
- Realism: ≥6/9 rate dossier/market dynamics “plausible” post-run survey.
- Strategy validity: ≥2 materially different winning strategies per family observed.
- Ablation gate: removing cohort retention / collateral / hiring delay changes
  human decisions (checked vs pilot debrief).

## 6. Reporting
Publish per-session: sector/family/seed, endpoint, V/P/E/O, head_hash,
wall time, assistance count, blinded review notes — never a single
“human vs AI” headline without workload caveats.
