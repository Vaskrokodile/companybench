"""Golden regression: replay same seed => same hash + economics."""
from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS
from companybench.simulation.engine import Engine
from companybench.evaluation.baselines import BASELINES


def test_replay_deterministic():
    kw = dict(sector="saas", family="build_discover", seed=3, difficulty=2,
              horizon_months=6, opening=dict(OPENING_MCU_THOUSANDS["saas"]))
    a = Engine(Scenario("g", **kw), world_seed="gold:1")
    a.run(months=6, policy=BASELINES["conservative_growth"])
    b = Engine(Scenario("g", **kw), world_seed="gold:1")
    b.run(months=6, policy=BASELINES["conservative_growth"])
    assert a.log.head_hash == b.log.head_hash
    assert a.ledger.balances == b.ledger.balances
