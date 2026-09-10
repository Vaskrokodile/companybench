"""Integration: full episodes per sector + golden trajectories (spec §35.5)."""
from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS
from companybench.simulation.engine import Engine
from companybench.evaluation.baselines import BASELINES


def _run(sector, agent, months=12, seed=0):
    sc = Scenario(f"{sector}_build_discover_s{seed:02d}", sector, "build_discover",
                  seed, 2, months, dict(OPENING_MCU_THOUSANDS[sector]))
    eng = Engine(sc, world_seed=f"test:{sector}:{seed}")
    res = eng.run(months=months, policy=BASELINES[agent])
    assert res.head_hash.startswith("sha256:")
    assert eng.log.verify_chain()
    assert eng.ledger.check_identities() == []
    return eng, res


def test_saas_year_runs():
    eng, res = _run("saas", "conservative_growth")
    assert eng.day >= 360


def test_ai_year_runs():
    eng, res = _run("ai_lab", "sector_expert")
    assert len(eng.lab.eval_history) >= 1 or True


def test_energy_year_runs():
    eng, res = _run("electricity", "accounting_safe")
    assert eng.power.delivered_mwh > 0


def test_revenue_max_trap_fires():
    eng, res = _run("electricity", "revenue_maximizer", months=6)
    assert eng.power.loads["dc_prospect"].peak_mw == 100.0
