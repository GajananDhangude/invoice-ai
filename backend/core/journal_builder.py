from models.invoice_model import InvoiceExtract
from models.journal_model import JournalEntryInvoice

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EXPENSE_ACCOUNT      = "1310020100"
CGST_INPUT_ACCOUNT   = "1120599007"
SGST_INPUT_ACCOUNT   = "1120599005"
IGST_INPUT_ACCOUNT   = "1120599003"
BANK_ACCOUNT         = "1113411000"

RS_GST_NUMBER        = "33AABCR7106G2ZP"
ACC_PERIOD           = "2026/001"
BRANCH_CODE          = "LXS00"
CHANNEL_CODE         = "CC004"
DEPARTMENT_CODE      = "SRO"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _common(invoice: InvoiceExtract) -> dict:
    """Fields that are the same across every row."""
    return dict(
        acc_period=ACC_PERIOD,
        trans_date=invoice.invoice_date,
        curr_code="INR",
        jrnal_source=None,
        asset_code=None,
        asset_indicator=None,
        asset_item_qty=None,
        due_date=None,                          # date field — None not ""
        product_analysis_code="_NA",
        channel_analysis_code=CHANNEL_CODE,
        sub_channel_analysis_code="_NA",
        underwriting_year_analysis_code="_NA",
        employee_code_analysis_code="_NA",
        department_analysis_code=DEPARTMENT_CODE,
        sequence_code_analysis_code="_NA",
        vendor_code_analysis_code=invoice.vendor_code,
        invoice_date=invoice.invoice_date,
        from_date=None,                         # date field — None not ""
        to_date=None,
        addl_date_4=None,
        addl_date_5=None,
        cheque_neft_number=invoice.vendor_gst,
        invoice_number=invoice.invoice_number,
        additional_remarks=None,
        additional_remarks_2=None,
        credence_description=None,
        reverse_charge=None,
        reverse_charge_pct=None,
        item_details_sr_no=None,
        goods_service=None,
        original_invoice_no=RS_GST_NUMBER,
    )


def _vendor_ref(invoice: InvoiceExtract) -> str:
    return f"{invoice.vendor_code}/{invoice.vendor_name.upper()}"


def _payment_ref(invoice: InvoiceExtract) -> str:
    return "VT" + invoice.invoice_number[-5:]


def _safe_hsn(invoice: InvoiceExtract) -> str | None:
    """Return HSN code safely — handles None."""
    if invoice.hsn_code is None:
        return None
    # Strip decimals if it looks like a number e.g. "998315.0" → "998315"
    if invoice.hsn_code.replace(".", "").isdigit():
        return str(int(float(invoice.hsn_code)))
    return invoice.hsn_code


# ---------------------------------------------------------------------------
# Row builders
# ---------------------------------------------------------------------------

def _row_expense_debit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 1 — Debit expense GL (taxable amount, before GST)."""
    return JournalEntryInvoice(
        **_common(invoice),
        l_id="1;3;6;7",
        account_code=EXPENSE_ACCOUNT,
        description="IT CLOUD INFRA EXPENSES",
        trans_amount=round(invoice.taxable_amount, 2),  # taxable, not net
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="TD02",
        hsn_sac_no=None,
        taxable_on_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_igst_debit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 2 inter-state — Debit IGST input credit."""
    return JournalEntryInvoice(
        **_common(invoice),
        l_id="6;7",
        account_code=IGST_INPUT_ACCOUNT,
        description="GST input cr exps-IGST",
        trans_amount=round(invoice.igst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_on_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=invoice.gst_rate,
        advance_challan_no=EXPENSE_ACCOUNT,
    )


def _row_sgst_debit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 2 intra-state — Debit SGST input credit."""
    return JournalEntryInvoice(
        **_common(invoice),
        l_id="6;7",
        account_code=SGST_INPUT_ACCOUNT,
        description="GST input cr exps-SGST",
        trans_amount=round(invoice.sgst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_on_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=round(invoice.gst_rate / 2, 2) if invoice.gst_rate else None,
        advance_challan_no=EXPENSE_ACCOUNT,
    )


def _row_cgst_debit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 3 intra-state — Debit CGST input credit."""
    return JournalEntryInvoice(
        **_common(invoice),
        l_id="6;7",
        account_code=CGST_INPUT_ACCOUNT,
        description="GST input cr exps-CGST",
        trans_amount=round(invoice.cgst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_on_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=round(invoice.gst_rate / 2, 2) if invoice.gst_rate else None,
        advance_challan_no=EXPENSE_ACCOUNT,
    )


def _row_vendor_credit_net(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 4 — Credit vendor payable net amount (GST02 bucket)."""
    return JournalEntryInvoice(
        **{**_common(invoice), "branch_analysis_code": "GST02"},
        l_id="6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="C",
        jrnal_type="SEXPS",
        reference=_payment_ref(invoice),
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=None,
        taxable_on_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_vendor_credit_gst(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 5 — Credit vendor payable GST amount (GST01 bucket)."""
    total_gst = round(invoice.igst or (invoice.cgst + invoice.sgst), 2)
    return JournalEntryInvoice(
        **{**_common(invoice), "branch_analysis_code": "GST01"},
        l_id="6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=total_gst,
        dr_cr="C",
        jrnal_type="SEXPS",
        reference=_payment_ref(invoice),
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=None,
        taxable_on_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_payment_debit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 6 — Debit vendor account (SPYMT payment entry)."""
    return JournalEntryInvoice(
        **_common(invoice),
        l_id="1;3;6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="D",
        jrnal_type="SPYMT",
        reference=_payment_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="_NA",
        hsn_sac_no=None,
        taxable_on_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_bank_credit(invoice: InvoiceExtract) -> JournalEntryInvoice:
    """Row 7 — Credit bank account (SPYMT payment entry)."""
    common = _common(invoice)
    common['additional_remarks'] = 'NEFT'
    return JournalEntryInvoice(
        **common,
        l_id="6;7",
        account_code=BANK_ACCOUNT,
        description="HDFC EXPENSES CORPORATE",
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="C",
        jrnal_type="SPYMT",
        reference=_payment_ref(invoice),
        branch_analysis_code=BRANCH_CODE,
        tds_applicability_analysis_code="_NA",

        hsn_sac_no=None,
        taxable_on_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


# ---------------------------------------------------------------------------
# Main entry point — returns a list of rows, not a single object
# ---------------------------------------------------------------------------

def build_journal_entries(invoice: InvoiceExtract) -> list[JournalEntryInvoice]:
    rows = []

    # SEXPS — expense booking
    rows.append(_row_expense_debit(invoice))

    if invoice.igst > 0:
        rows.append(_row_igst_debit(invoice))       # inter-state
    else:
        rows.append(_row_sgst_debit(invoice))       # intra-state
        rows.append(_row_cgst_debit(invoice))

    rows.append(_row_vendor_credit_net(invoice))
    rows.append(_row_vendor_credit_gst(invoice))

    # SPYMT — payment booking
    rows.append(_row_payment_debit(invoice))
    rows.append(_row_bank_credit(invoice))

    return rows


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

# if __name__ == "__main__":
#     from datetime import date

# #     invoice = InvoiceExtract(
# #         invoice_number="AIN2526001124876",
# #         invoice_date=date(2025, 7, 2),
# #         vendor_name="Amazon Web Services India Private Limited",
# #         vendor_gst="07AAJCA9880A1ZL",
# #         net_amount=2712845.83,
# #         taxable_amount=2299021.89,
# #         igst=413823.94,
# #         hsn_code="998315",
# #         billing_period="June 1 - June 30, 2025",
# #     )
#     invoice = gene
#     rows = build_journal_entries()
# #     print(rows)

    