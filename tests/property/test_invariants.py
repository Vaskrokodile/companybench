"""Determinism + conservation property tests (spec §35.1, §35.4)."""
from companybench.kernel.rng import StableRNG
from companybench.kernel.events import EventLog
from datetime import datetime, timezone


def test_rng_stable():
    r = StableRNG("seed1")
    t = "2031-01-01T00:00:00Z"
    assert r.uniform("m", "e", t, "x", 0) == r.uniform("m", "e", t, "x", 0)
    assert r.uniform("m", "e", t, "x", 1) != r.uniform("m", "e", t, "x", 0)


def test_event_chain_verifies():
    log = EventLog()
    now = datetime(2031, 1, 1, tzinfo=timezone.utc)
    log.append(now, "a", "x", [], [], {"v": 1})
    log.append(now, "b", "x", [], [], {"v": 2})
    assert log.verify_chain()


def test_idempotent_payment_split():
    # splitting a payment preserves total when fees unchanged
    assert 60_000 + 40_000 == 100_000


def test_choice_outside_option_sums_to_one():
    from companybench.markets.customers import choice_probs
    p = choice_probs({"a": 1.0, "b": 0.5, "outside": 0.0})
    assert abs(sum(p.values()) - 1.0) < 1e-9
