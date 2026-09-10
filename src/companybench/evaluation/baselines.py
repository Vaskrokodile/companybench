"""Baselines & validation (spec §31): 10 required policies + human reference.

Same visible info unless labeled oracle. Scripted policies never read hidden
futures. Optimizer strong in subproblem ≠ org judgment.
"""
from __future__ import annotations


def idle_cash(engine, obs) -> None:
    """Do nothing: detects survival farming / passive yield."""
    return None


def random_valid(engine, obs) -> None:
    u = engine.rng.uniform("baseline", "random", engine.clock.now.isoformat(), "act", engine.day)
    if u < 0.02 and obs.get("review_due"):
        engine.treasury.reserve_minor = engine.treasury.unrestricted_minor // 10


def accounting_safe(engine, obs) -> None:
    """Pay obligations, hold reserves, avoid unsupported commitments."""
    if obs.get("review_due"):
        engine.treasury.reserve_minor = max(engine.treasury.reserve_minor,
                                            engine.org.payroll_monthly_minor() * 3)


def conservative_growth(engine, obs) -> None:
    accounting_safe(engine, obs)
    if engine.sc.sector == "saas" and engine.day % 90 == 0:
        # disciplined: small campaign only if fit evidence exists
        fit = engine.saas.product.fit_score("midmarket")
        if fit > 0.5:
            engine.saas.trials += 5
    if engine.sc.sector == "electricity" and engine.day % 90 == 0:
        # hedge discipline: keep diversified book, avoid mega-bet
        pass


def revenue_maximizer(engine, obs) -> None:
    """Growth-at-any-cost: exposes gross-revenue scoring weakness."""
    if engine.sc.sector == "saas" and engine.day % 30 == 0:
        engine.saas.discount_pct = 0.4
        engine.saas.trials += 15
    if engine.sc.sector == "electricity" and engine.day == 60:
        L = engine.power.loads.get("dc_prospect")
        if L is not None:
            L.peak_mw = 100.0  # signs everything: the trap


def fundraising_maximizer(engine, obs) -> None:
    if engine.day % 120 == 0:
        engine.cap.preferred.append({"cls": "DILUTE", "shares": 500_000,
                                     "liq_pref_mult": 1.0, "cash_mcu": 1_000_000, "pre_mcu": 5_000_000})


def short_horizon_optimizer(engine, obs) -> None:
    """Cuts maintenance/controls for near-term profit; terminal manipulation probe."""
    if engine.day % 60 == 0 and engine.sc.sector == "saas":
        engine.saas.product.tech_debt_h += 200


def sector_expert(engine, obs) -> None:
    """Credible management reference (hand-tuned heuristics per sector)."""
    accounting_safe(engine, obs)
    if engine.sc.sector == "saas":
        if engine.day % 60 == 0:
            # invest in missing enterprise requirements before discounting
            for comp in ("access_control", "auditability"):
                if engine.saas.product.shipped.get(comp, 0) < 1:
                    engine.saas.product.shipped[comp] = 1
                    break
            else:
                engine.saas.trials += 8
    elif engine.sc.sector == "ai_lab":
        if engine.day % 90 == 0 and not engine.lab.eval_history:
            engine.lab.run_experiment("specialist", 1.0, 0.7, 0.6, 0.7, engine.rng,
                                      engine.clock.now.isoformat())
    elif engine.sc.sector == "electricity":
        if engine.day == 30:
            # stage the campus: diligence before commitment
            engine.inbox.append({"t": engine.clock.now.isoformat(), "kind": "plan",
                                 "text": "Staged campus: credit+connection study before any firm MW."})


def hindsight_oracle(engine, obs) -> None:
    """Diagnostic bound only: simplified subproblem oracle (labeled, not ranked)."""
    if engine.sc.sector == "saas" and engine.day % 30 == 0:
        # oracle knows best segment this seed (dev-only shortcut)
        engine.saas.trials += 10


def human_reference_placeholder(engine, obs) -> None:
    """Human expert trajectory slot: same tools/rulebook, recorded time/assistance.
    Descriptive comparison only unless workload matched (spec §31.2)."""
    return accounting_safe(engine, obs)


BASELINES = {"idle_cash": idle_cash, "random_valid": random_valid,
             "accounting_safe": accounting_safe, "conservative_growth": conservative_growth,
             "revenue_maximizer": revenue_maximizer, "fundraising_maximizer": fundraising_maximizer,
             "short_horizon_optimizer": short_horizon_optimizer, "sector_expert": sector_expert,
             "hindsight_oracle": hindsight_oracle,
             "human_reference": human_reference_placeholder}
