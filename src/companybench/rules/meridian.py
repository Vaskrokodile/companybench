"""Meridian rules: jurisdiction + accounting policy + calendar (spec §2.3, §8, §41.8)."""
from __future__ import annotations

RULES_VERSION = "meridian_v1"
ACCOUNTING_POLICY = "companybench_accrual_v1"
CURRENCY = "MCU"
MINOR_PER_MCU = 100
TAX_RATE = 0.25

CALENDAR_HOLIDAYS = ["2031-01-01", "2031-05-01", "2031-12-25", "2031-12-26"]

DEFAULT_TIMING = {
    "payroll": "monthly_last_business_day_accrued_daily",
    "employee_notice_days": 30,
    "supplier_terms": "net_30_from_accepted_delivery",
    "tax": "25pct_positive_profit_after_carryforward_quarterly",
    "loss_carryforward": "unlimited_same_entity_no_refund",
    "unsecured_cure_days": 5,
    "wholesale_collateral": "intraday_or_next_day_per_instrument",
    "board_reserved_commitment_pct": 0.20,
}

OPENING_EQUITY = {"ai_lab": 8_700_000, "saas": 1_500_000, "electricity": 15_000_000}

ACCOUNTING_NOTES = (
    "Training/research expensed unless separately specified asset class. "
    "Energy construction in CIP, depreciated post-commissioning. Impairment on "
    "engine evidence. Principal/agent by contract structure. Interest paid = "
    "operating (reference policy). FCF = OCF - gross cash capex, asset sales separate."
)
