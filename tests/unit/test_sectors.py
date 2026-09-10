"""Sector math checks: FLOPs, SaaS cohorts, storage, datacenter tables."""
from companybench.sectors.ai_lab.lab import training_flops_estimate, worked_example
from companybench.sectors.saas.saas import cohort_example, acquisition_example
from companybench.sectors.electricity.power import Storage, credit_call
from companybench.sectors.electricity.datacenter import normal_case, stress_case


def test_flops_worked():
    assert training_flops_estimate(7_000_000_000, 200_000_000_000) == 8.4e21
    w = worked_example()
    assert 45.0 < w["elapsed_h"] < 46.5
    assert 34_000 < w["rental_mcu"] < 36_000


def test_saas_cohorts():
    c = cohort_example()
    assert c["end_mrr"] == 124_000
    assert abs(c["grr"] - 0.92) < 1e-9
    assert abs(c["nrr"] - 1.04) < 1e-9
    a = acquisition_example()
    assert a["cac"] == 3_000
    assert abs(a["payback_months"] - 12.5) < 1e-9


def test_storage_no_free_energy():
    s = Storage("b", "north", 100, 400, 200)
    try:
        s.step(10, 10)
        assert False, "simultaneous must fail"
    except ValueError:
        pass
    r = s.step(0, 50)
    assert 0 <= s.soc_mwh <= 400


def test_datacenter_tables():
    n = normal_case()
    assert n["mwh"] == 100 * 0.90 * 8760
    assert abs(n["contribution"] - 5_037_600) < 1.0
    st = stress_case()
    assert abs(st["contribution"] - (-38_324_400)) < 1.0
    cc = credit_call(100, 500, 300, 200, 100)
    assert cc["call"] == 500
