"""Financial golden cases (spec §35.2): prepay/recognition, equity, debt, collateral."""
from companybench.finance.ledger import Ledger, mcu


def test_annual_prepay_recognition():
    L = Ledger()
    L.annual_prepay("2031-01-01T00:00:00Z", "e1", mcu(120_000))
    assert L.balances["cash_unrestricted"] == mcu(120_000)
    assert L.balances["deferred_revenue"] == mcu(120_000)
    for _ in range(12):
        L.recognize_revenue("2031-01-31T00:00:00Z", "e2", mcu(10_000))
    assert L.balances["deferred_revenue"] == 0
    assert L.balances["revenue_service"] == mcu(120_000)
    assert L.check_identities() == []


def test_priced_round_math():
    # §10.2: 2M at 8M pre => 20% new, existing 80%
    from companybench.finance.funding import CapTable
    c = CapTable()
    r = c.priced_round(8_000_000, 2_000_000)
    assert abs(r["new_fraction"] - 0.2) < 1e-9
    assert abs(r["post_money_mcu"] - 10_000_000) < 1e-9


def test_debt_and_collateral():
    L = Ledger()
    L.opening("2031-01-01T00:00:00Z", {"cash_unrestricted": 1000}, {}, {"common": 1000})
    L.debt_draw("2031-02-01T00:00:00Z", "e", mcu(500))
    L.restrict_cash("2031-02-02T00:00:00Z", "e", mcu(100))
    assert L.balances["cash_restricted"] == mcu(100)
    L.debt_service("2031-03-01T00:00:00Z", "e", mcu(50), mcu(5))
    assert L.check_identities() == []


def test_liquidity_example():
    # §9.3: 800k cash, 100k burn, 450k installment @45d => ~200k usable
    from companybench.finance.treasury import Treasury
    t = Treasury(unrestricted_minor=mcu(800_000), restricted_minor=mcu(300_000))
    assert t.usable_cash_after(mcu(100_000), 1.5, mcu(450_000)) == mcu(200_000)
    assert t.trailing_runway([mcu(-100_000)] * 3) == 8.0
