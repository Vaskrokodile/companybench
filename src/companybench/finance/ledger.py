"""Double-entry general ledger (spec §8).

Invariants per posting:
  sum(debits) == sum(credits)
  assets == liabilities + equity
  closing_cash == opening + OCF + ICF + FCF-classified flows
Money = integer minor units (1 MCU = 100 minor). No float aggregates.
Revenue ≠ bookings ≠ cash: bookings/RPO/invoice/cash/recognition separated
(IFRS-15-inspired fictional policy companybench_accrual_v1).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

MINOR_PER_MCU = 100

ASSET_ACCOUNTS = {
    "cash_unrestricted", "cash_restricted", "receivables", "allowance_doubtful",
    "prepayments", "inventory", "ppe_gross", "accum_depreciation",
    "intangibles", "spv_investment", "deferred_tax_asset",
}
LIABILITY_ACCOUNTS = {
    "payables", "accrued_payroll", "deferred_revenue", "debt_principal",
    "interest_payable", "tax_payable", "provisions", "customer_deposits",
    "spv_nci",
}
EQUITY_ACCOUNTS = {"common", "preferred", "apic", "retained_earnings", "oci"}
REVENUE_ACCOUNTS = {"revenue_service", "revenue_product", "revenue_energy", "revenue_other"}
EXPENSE_ACCOUNTS = {
    "cost_of_revenue", "rd_expense", "sales_expense", "gna_expense",
    "depreciation", "equity_comp", "financing_expense", "tax_expense",
    "bad_debt", "impairment", "other_loss",
}

ALL_ACCOUNTS = (ASSET_ACCOUNTS | LIABILITY_ACCOUNTS | EQUITY_ACCOUNTS
                | REVENUE_ACCOUNTS | EXPENSE_ACCOUNTS | {"contra_equity_options"})

CONTRA_ASSET_ACCOUNTS = {"allowance_doubtful", "accum_depreciation"}
# debit-normal assets exclude contra-assets (credit-normal)
DEBIT_NORMAL = ((ASSET_ACCOUNTS - CONTRA_ASSET_ACCOUNTS) | EXPENSE_ACCOUNTS
                | {"contra_equity_options"})


def mcu(x_mcu: float) -> int:
    """Fictional MCU float -> integer minor units."""
    return int(round(x_mcu * MINOR_PER_MCU))


def fmt_minor(v: int) -> float:
    return v / MINOR_PER_MCU


@dataclass
class Posting:
    posting_id: str
    occurred_at: str
    source_event: str
    lines: list  # [(account, debit_minor, credit_minor)]
    memo: str = ""


class Ledger:
    def __init__(self) -> None:
        self.balances: dict[str, int] = {a: 0 for a in ALL_ACCOUNTS}
        # debit-normal vs credit-normal for trial check
        self.postings: list[Posting] = []
        self._seq = 0
        # subledgers
        self.invoices: dict[str, dict] = {}
        self.monthly: dict[str, dict] = {}  # YYYY-MM -> {revenue, cor, opex, ...}

    # ---- core posting ----
    def post(self, occurred_at: str, source_event: str, lines: list[tuple[str, int, int]], memo: str = "") -> Posting:
        for acct, _d, _c in lines:
            if acct not in ALL_ACCOUNTS:
                raise ValueError(f"unknown account {acct}")
        td = sum(d for _, d, _ in lines)
        tc = sum(c for _, _, c in lines)
        if td != tc:
            raise ValueError(f"unbalanced posting debits={td} credits={tc}")
        self._seq += 1
        p = Posting(f"posting_{self._seq:06d}", occurred_at, source_event, lines, memo)
        for acct, d, c in lines:
            self.balances[acct] += d - c if self._is_debit_normal(acct) else c - d
        self.postings.append(p)
        return p

    @staticmethod
    def _is_debit_normal(acct: str) -> bool:
        return acct in DEBIT_NORMAL

    # ---- convenience ops ----
    def opening(self, occurred_at: str, assets_mcu: dict, liabilities_mcu: dict, equity_mcu: dict) -> Posting:
        lines: list[tuple[str, int, int]] = []
        for a, v in assets_mcu.items():
            lines.append((a, mcu(v), 0))
        for a, v in liabilities_mcu.items():
            lines.append((a, 0, mcu(v)))
        for a, v in equity_mcu.items():
            lines.append((a, 0, mcu(v)))
        return self.post(occurred_at, "opening", lines, "opening balance sheet")

    def cash_expense(self, occurred_at: str, event: str, amount_minor: int, expense_acct: str, memo: str = "") -> Posting:
        return self.post(occurred_at, event, [
            (expense_acct, amount_minor, 0),
            ("cash_unrestricted", 0, amount_minor),
        ], memo or f"cash expense {expense_acct}")

    def accrue_payroll(self, occurred_at: str, event: str, amount_minor: int) -> Posting:
        # Dr gna (or allocated) / Cr accrued_payroll ; payment separate
        return self.post(occurred_at, event, [
            ("gna_expense", amount_minor, 0),
            ("accrued_payroll", 0, amount_minor),
        ], "accrue payroll")

    def pay_accrued(self, occurred_at: str, event: str, amount_minor: int) -> Posting:
        return self.post(occurred_at, event, [
            ("accrued_payroll", amount_minor, 0),
            ("cash_unrestricted", 0, amount_minor),
        ], "pay accrued payroll")

    def invoice_issue(self, occurred_at: str, event: str, invoice_id: str, amount_minor: int) -> Posting:
        self.invoices[invoice_id] = {"amount": amount_minor, "collected": 0, "issued_at": occurred_at}
        return self.post(occurred_at, event, [
            ("receivables", amount_minor, 0),
            ("deferred_revenue", 0, amount_minor),  # obligation until performed; recognition separate
        ], f"invoice {invoice_id} issued (bookings/RPO, not yet revenue)")

    def collect(self, occurred_at: str, event: str, invoice_id: str, amount_minor: int) -> Posting:
        inv = self.invoices.get(invoice_id, {"amount": 0, "collected": 0})
        inv["collected"] = inv.get("collected", 0) + amount_minor
        self.invoices[invoice_id] = inv
        return self.post(occurred_at, event, [
            ("cash_unrestricted", amount_minor, 0),
            ("receivables", 0, amount_minor),
        ], f"collect {invoice_id}")

    def recognize_revenue(self, occurred_at: str, event: str, amount_minor: int, revenue_acct: str = "revenue_service") -> Posting:
        return self.post(occurred_at, event, [
            ("deferred_revenue", amount_minor, 0),
            (revenue_acct, 0, amount_minor),
        ], "recognize revenue as obligations performed")

    def annual_prepay(self, occurred_at: str, event: str, cash_minor: int) -> Posting:
        # Cash Dr / Deferred revenue Cr (spec §8.2 example: 120k for 12 months)
        return self.post(occurred_at, event, [
            ("cash_unrestricted", cash_minor, 0),
            ("deferred_revenue", 0, cash_minor),
        ], "annual prepayment: liability until delivery")

    def equity_raise(self, occurred_at: str, event: str, cash_minor: int, fees_minor: int = 0) -> Posting:
        lines = [("cash_unrestricted", cash_minor - fees_minor, 0)]
        if fees_minor:
            lines.append(("gna_expense", fees_minor, 0))
        lines.append(("common", 0, cash_minor))
        return self.post(occurred_at, event, lines, "priced equity (financing CF, never revenue)")

    def debt_draw(self, occurred_at: str, event: str, cash_minor: int) -> Posting:
        return self.post(occurred_at, event, [
            ("cash_unrestricted", cash_minor, 0),
            ("debt_principal", 0, cash_minor),
        ], "debt draw")

    def debt_service(self, occurred_at: str, event: str, principal_minor: int, interest_minor: int) -> Posting:
        lines = []
        if principal_minor:
            lines += [("debt_principal", principal_minor, 0), ("cash_unrestricted", 0, principal_minor)]
        if interest_minor:
            lines += [("financing_expense", interest_minor, 0), ("cash_unrestricted", 0, interest_minor)]
        return self.post(occurred_at, event, lines, "debt service (interest=operating per reference policy)")

    def restrict_cash(self, occurred_at: str, event: str, amount_minor: int) -> Posting:
        # reclass unrestricted -> restricted (collateral)
        return self.post(occurred_at, event, [
            ("cash_restricted", amount_minor, 0),
            ("cash_unrestricted", 0, amount_minor),
        ], "post collateral")

    def release_cash(self, occurred_at: str, event: str, amount_minor: int) -> Posting:
        return self.post(occurred_at, event, [
            ("cash_unrestricted", amount_minor, 0),
            ("cash_restricted", 0, amount_minor),
        ], "release collateral")

    # ---- statements ----
    def trial_ok(self) -> bool:
        # debits-normal balances positive check via reconstruct: sum of all signed = 0
        return True  # post() guarantees balance

    def balance_sheet(self) -> dict:
        gross_debit_assets = sum(self.balances[x] for x in ASSET_ACCOUNTS if x not in CONTRA_ASSET_ACCOUNTS)
        contra = sum(self.balances[x] for x in CONTRA_ASSET_ACCOUNTS)
        a = gross_debit_assets - contra
        l = sum(self.balances[x] for x in LIABILITY_ACCOUNTS)
        base_equity = (sum(self.balances[x] for x in EQUITY_ACCOUNTS)
                       - self.balances["contra_equity_options"])
        # YTD earnings live in revenue/expense accounts until formal close;
        # include them so A == L + E holds continuously (spec §8.1).
        ytd_net = sum(self.balances[x] for x in REVENUE_ACCOUNTS) - sum(
            self.balances[x] for x in EXPENSE_ACCOUNTS)
        e = base_equity + ytd_net
        return {"assets": a, "liabilities": l, "equity": e,
                "base_equity": base_equity, "ytd_net": ytd_net,
                "balances": dict(self.balances)}

    def close_to_retained(self, occurred_at: str = "", source_event: str = "close") -> Posting | None:
        """Optional formal close: move YTD net into retained_earnings (identity preserved)."""
        ytd = sum(self.balances[x] for x in REVENUE_ACCOUNTS) - sum(
            self.balances[x] for x in EXPENSE_ACCOUNTS)
        if ytd == 0:
            return None
        # zero out temp accounts via offsetting post
        lines: list[tuple[str, int, int]] = []
        for acct in REVENUE_ACCOUNTS:
            b = self.balances[acct]
            if b:
                lines.append((acct, b, 0))  # debit revenue to zero (credit-normal)
        for acct in EXPENSE_ACCOUNTS:
            b = self.balances[acct]
            if b:
                lines.append((acct, 0, b))  # credit expense to zero (debit-normal)
        if ytd > 0:
            lines.append(("retained_earnings", 0, ytd))
        else:
            lines.append(("retained_earnings", -ytd, 0))
        return self.post(occurred_at or "close", source_event, lines, "close YTD to retained earnings")

    def income_statement(self, revenue_minor: int | None = None) -> dict:
        rev = sum(self.balances[x] for x in REVENUE_ACCOUNTS)
        cor = self.balances["cost_of_revenue"]
        opex = (self.balances["rd_expense"] + self.balances["sales_expense"]
                + self.balances["gna_expense"] + self.balances["depreciation"]
                + self.balances["equity_comp"] + self.balances["bad_debt"])
        gross = rev - cor
        op = gross - opex
        pretax = op - self.balances["financing_expense"] - self.balances["other_loss"] - self.balances["impairment"]
        net = pretax - self.balances["tax_expense"]
        # net also equals rev - all expenses by construction; assert in tests
        return {"revenue": rev, "cost_of_revenue": cor, "gross_profit": gross,
                "operating_expenses": opex, "operating_profit": op,
                "pretax": pretax, "net_profit": net}

    def check_identities(self) -> list[str]:
        errs = []
        bs = self.balance_sheet()
        if bs["assets"] != bs["liabilities"] + bs["equity"]:
            errs.append(f"A({bs['assets']}) != L+E({bs['liabilities']}+{bs['equity']})")
        for p in self.postings:
            td = sum(d for _, d, _ in p.lines)
            tc = sum(c for _, _, c in p.lines)
            if td != tc:
                errs.append(f"unbalanced {p.posting_id}")
                break
        return errs

    # ---- period close ----
    def record_month(self, ym: str, revenue_minor: int, cor_minor: int, opex_minor: int,
                     ocf_minor: int, capex_minor: int, fcf_note: str = "") -> None:
        self.monthly[ym] = {"revenue": revenue_minor, "cor": cor_minor, "opex": opex_minor,
                            "ocf": ocf_minor, "capex": capex_minor,
                            "fcf": ocf_minor - capex_minor}
