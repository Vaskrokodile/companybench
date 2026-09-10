"""Milestones (spec §27): M01-M10 cross-sector + sector ladders (§41.10).

Executable predicates, prerequisites, min duration, quality gates; reversal
revokes current status but history retained. Sustainment: revenue 3 closes,
reliability real load/duration, commissioning permits+tests+rights.
"""
from __future__ import annotations


MILESTONES = {
    "M01": "First paying external customer",
    "M02": "First repeat/renewal customer",
    "M03": "First completed financing",
    "M04": "Twelve months operating continuity",
    "M05": "First profitable quarter",
    "M06": "Cash-generating operations (OCF+ 2 quarters)",
    "M07": "Durable profitable operation (profit+OCF 4 quarters)",
    "M08": "Recovery from material incident",
    "M09": "Multi-year continuity (24/36/60m)",
    "M10": "Value-creating exit/distribution",
}

# draft progress ladders: (axis, sector) -> [(rung_points, predicate_desc)]
LADDERS = {
    ("ai_lab", "external"): [(0, "no verified paying use"), (10, "one paid reproducible pilot"),
                              (25, ">=5 independent paying orgs, accepted production 90d")],
    ("ai_lab", "scale"): [(0, "below"), (10, "1M trailing revenue OR one qualified gen"),
                          (25, "10M trailing OR 3 sequential qualified gens each w/ >=5 payers")],
    ("ai_lab", "repeat"): [(0, "none"), (10, "one independent renewal"),
                           (25, ">=5 renewals + positive serving contrib 2q")],
    ("ai_lab", "econ"): [(0, "none"), (10, "OCF+ 2q"), (25, "profit+OCF 4q")],
    ("saas", "external"): [(0, "none"), (10, "30 active payers 90d"), (25, "100 payers or 10 enterprise 180d")],
    ("saas", "scale"): [(0, "below"), (10, "1M ARR 3 closes"), (25, "5M ARR 3 closes")],
    ("saas", "repeat"): [(0, "none"), (10, "mature 12m GRR>=80%"), (25, "GRR>=90% & NRR>=105%, >=20 orgs or 10 ent")],
    ("saas", "econ"): [(0, "none"), (10, "OCF+ 2q"), (25, "profit+OCF 4q")],
    ("electricity", "external"): [(0, "none"), (10, "100k trailing MWh OR financed+signed offtake"),
                                  (25, "500k trailing MWh w/ positive contrib OR commissioned 90d accepted")],
    ("electricity", "scale"): [(0, "below"), (10, "10MW new connected/commissioned or equiv rights"),
                               (25, "50MW new connected/commissioned or 50MW-equiv funded portfolio")],
    ("electricity", "repeat"): [(0, "none"), (10, "90d service+financing obligations met"),
                                (25, "12m obligations met, diversified/secured")],
    ("electricity", "econ"): [(0, "none"), (10, "OCF+ 2q OR DSCR>=1.20 2q post-commission"),
                              (25, "profit+OCF 4q OR DSCR>=1.30 4q + liquidity met")],
}


def check_cross_milestones(summary: dict, months_alive: int) -> dict:
    m = {}
    fin = summary["financial"]
    m["M01"] = fin["revenue"] > 0
    m["M02"] = False  # requires renewal table; engine sets via cohorts
    m["M03"] = False
    m["M04"] = months_alive >= 12
    m["M05"] = fin["operating_profit"] > 0
    m["M06"] = False
    m["M07"] = False
    m["M08"] = False
    m["M09"] = months_alive >= 24
    m["M10"] = False
    return m


def progress_P(sector: str, evidence: dict, opening_rungs: dict | None = None) -> dict:
    """P = sum of 4 axes (25 each). Incremental vs opening rung (no credit for gifts)."""
    axes = ["external", "scale", "repeat", "econ"]
    total, detail = 0.0, {}
    for ax in axes:
        cur = evidence.get(ax, 0)  # rung points 0/10/25 sustained
        opening = (opening_rungs or {}).get(ax, 0)
        if opening >= 25:
            pts = 0.0  # axis must be replaced by higher ladder (manifest rule)
        elif cur <= opening:
            pts = 0.0
        else:
            pts = 25 * min(1.0, max(0.0, (cur - opening) / (25 - opening)))
        detail[ax] = round(pts, 2)
        total += pts
    return {"P": round(total, 2), "axes": detail}
