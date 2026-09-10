"""Scoring checks (spec §28): V/P/E/O, DSCR, waterfall, obligations mapping."""
from companybench.evaluation.scoring import (viability, equity_value_added, normalize,
                                              obligations_score, terminal_value, core_score)
from companybench.finance.funding import DebtFacility, exit_waterfall
from companybench.evaluation.milestones import progress_P


def test_viability():
    assert viability(1825, 1825) == 100.0
    assert viability(913, 1825) == 50.0 or abs(viability(913, 1825) - 50.0) < 0.2


def test_equity_value_adjusts_support():
    # distributions 1M at day 365, terminal 2M, initial 1.5M, new 0.5M, support 0.3M
    eva = equity_value_added([(365, 1_000_000)], 2_000_000, 1_500_000, [(100, 500_000)],
                             [(200, 300_000)], 730, r=0.10)
    assert eva < (1_000_000 + 2_000_000 - 1_500_000)  # discount + contributions reduce


def test_dscr_definition():
    d = DebtFacility(1_000_000_00, 0.08, "2036-01-01", amort_monthly_minor=50_000_00)
    cafds = 100_000_00
    assert abs(d.dscr(cafds) - cafds / (50_000_00 + d.monthly_interest())) < 1e-9


def test_exit_waterfall_no_double_debt():
    w = exit_waterfall(10_000_000, 2_000_000, 500_000, [], 9_000_000)
    assert w["creditors"] == 2_000_000 and w["fees"] == 500_000
    assert w["common"] == 10_000_000 - 2_000_000 - 500_000


def test_obligations_mapping():
    o = obligations_score([{"category": "customer", "severity": "material", "resolved": True}],
                          {"customer": 12, "workforce": 12, "financing": 12, "controls": 12})
    assert 0 < o["O"] <= 100
    bad = obligations_score([{"category": "customer", "severity": "terminal", "resolved": False}],
                            {"customer": 12, "workforce": 12, "financing": 12, "controls": 12})
    assert bad["categories"]["customer"] == 0.0


def test_progress_incremental():
    p = progress_P("saas", {"external": 10, "scale": 10, "repeat": 0, "econ": 0}, {"external": 0})
    assert p["P"] > 0
    gift = progress_P("saas", {"external": 10}, {"external": 10})
    assert gift["axes"]["external"] == 0.0  # no credit for inherited rung


def test_core_weights():
    assert core_score(100, 100, 100, 100) == 100.0
    assert abs(core_score(80, 60, 40, 20) - (0.25*80 + 0.25*60 + 0.30*40 + 0.20*20)) < 1e-9


def test_normalize_anchors_fixed():
    assert normalize(5, 0, 10) == 50.0
    assert normalize(-5, 0, 10) == 0.0
    assert normalize(50, 0, 10) == 100.0
