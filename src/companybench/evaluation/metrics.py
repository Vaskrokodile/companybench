"""Metric dictionary (spec §26): identity/control, financial, org, commercial,
reliability, runtime/cost. Ratios specify cohort/period/numerator/denominator.
"""
from __future__ import annotations


def monthly_series(rows: list[dict], key: str) -> list:
    return [r.get(key) for r in rows]


def summarize_episode(engine) -> dict:
    inc = engine.ledger.income_statement()
    bs = engine.ledger.balance_sheet()
    tot = engine.cohorts.totals()
    hc = engine.org.headcount()
    return {
        "identity": {"scenario": engine.sc.id, "sector": engine.sc.sector,
                     "family": engine.sc.family, "seed": engine.seed,
                     "rules": "meridian_v1", "spec": "0.1.0"},
        "financial": {
            "revenue": inc["revenue"], "gross_profit": inc["gross_profit"],
            "operating_profit": inc["operating_profit"], "net_profit": inc["net_profit"],
            "cash_unrestricted": bs["balances"]["cash_unrestricted"],
            "cash_restricted": bs["balances"]["cash_restricted"],
            "liabilities": bs["liabilities"], "equity": bs["equity"],
            "monthly": engine.monthly_rows,
        },
        "org": {"headcount": hc, "payroll_monthly": engine.org.payroll_monthly_minor()},
        "commercial": {"mrr": tot["mrr"], "customers": tot["customers"],
                       "delivered_mwh": getattr(engine.power, "delivered_mwh", 0.0),
                       "unserved_mwh": getattr(engine.power, "unserved_mwh", 0.0),
                       "evals": len(engine.lab.eval_history)},
        "runtime": {"days": engine.day, "events": len(engine.log.events),
                    "gen_used": engine.clock.inference.gen_used,
                    "tools_used": engine.clock.inference.tools_used},
    }
