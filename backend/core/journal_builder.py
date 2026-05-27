import json
import os
from models.invoice_model import InvoiceExtract
from models.journal_model import JournalEntryInvoice

# ---------------------------------------------------------------------------
# Fixed constants — never change
# ---------------------------------------------------------------------------
CGST_INPUT_ACCOUNT   = "1120599007"
SGST_INPUT_ACCOUNT   = "1120599005"
IGST_INPUT_ACCOUNT   = "1120599003"
BANK_ACCOUNT         = "1113411000"
RS_GST_NUMBER        = "33AABCR7106G1ZQ"   # FIX 1
ACC_PERIOD           = "2026/001"

# ---------------------------------------------------------------------------
# Vendor master loader
# ---------------------------------------------------------------------------
VENDOR_MASTER_PATH = os.path.join(
    os.path.dirname(__file__), "../config/vendor_master.json"
)

def _load_vendor_config(vendor_gst: str) -> dict:
    """Look up vendor config by GST number, fall back to DEFAULT."""
    with open(VENDOR_MASTER_PATH, "r") as f:
        master = json.load(f)

    config = master.get(vendor_gst)

    if config is None:
        print(f"Vendor {vendor_gst} not in master — using DEFAULT config")
        config = master["DEFAULT"]

    # Use vendor_code from invoice if not in master
    return config


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _common(invoice: InvoiceExtract, config: dict) -> dict:
    return dict(
        acc_period=ACC_PERIOD,
        trans_date=invoice.invoice_date,
        curr_code="INR",
        jrnal_source=None,
        asset_code=None,
        asset_indicator=None,
        asset_item_qty=None,
        due_date=None,
        product_analysis_code="",
        channel_analysis_code=config["channel"],
        sub_channel_analysis_code="",
        underwriting_year_analysis_code="",
        employee_code_analysis_code="",
        department_analysis_code=config["department"],
        sequence_code_analysis_code=None,          # FIX 3 — blank not _NA
        vendor_code_analysis_code=invoice.vendor_code,
        invoice_date=invoice.invoice_date,
        from_date=None,
        to_date=None,
        addl_date_4=None,
        addl_date_5=None,
        cheque_neft_number=invoice.vendor_gst,
        invoice_number=invoice.invoice_number,
        additional_remarks=None,
        additional_remarks_2=invoice.billing_period or None,  # FIX 2
        credence_description=None,
        reverse_charge=None,
        reverse_charge_percent=None,
        item_details_sr_no=None,
        goods_service=None,
        original_invoice_no_for_dr_cr_notes=RS_GST_NUMBER,    # FIX 1
    )


def _vendor_ref(invoice: InvoiceExtract) -> str:
    return f"{invoice.vendor_code}/{invoice.vendor_name.upper()}"


def _payment_ref(invoice: InvoiceExtract) -> str:
    return "VT" + invoice.invoice_number[-5:]


def _safe_hsn(invoice: InvoiceExtract) -> str | None:
    if invoice.hsn_code is None:
        return None
    if invoice.hsn_code.replace(".", "").isdigit():
        return str(int(float(invoice.hsn_code)))
    return invoice.hsn_code


# ---------------------------------------------------------------------------
# Row builders — now accept config
# ---------------------------------------------------------------------------

def _row_expense_debit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    return JournalEntryInvoice(
        **_common(invoice, config),
        l_id="1;3;6;7",
        account_code=config["expense_account"],   # dynamic
        description=config["description"],         # dynamic
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code=config["tds_code"],  # dynamic
        hsn_sac_no=None,
        taxable_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_igst_debit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    return JournalEntryInvoice(
        **_common(invoice, config),
        l_id="6;7",
        account_code=IGST_INPUT_ACCOUNT,
        description="GST input cr exps-IGST",
        trans_amount=round(invoice.igst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code="",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=invoice.gst_rate,
        advance_challan_no=config["expense_account"],  # dynamic
    )


def _row_sgst_debit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    return JournalEntryInvoice(
        **_common(invoice, config),
        l_id="6;7",
        account_code=SGST_INPUT_ACCOUNT,
        description="GST input cr exps-SGST",
        trans_amount=round(invoice.sgst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code=" ",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=round(invoice.gst_rate / 2, 2) if invoice.gst_rate else None,
        advance_challan_no=config["expense_account"],  # dynamic
    )


def _row_cgst_debit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    return JournalEntryInvoice(
        **_common(invoice, config),
        l_id="6;7",
        account_code=CGST_INPUT_ACCOUNT,
        description="GST input cr exps-CGST",
        trans_amount=round(invoice.cgst, 2),
        dr_cr="D",
        jrnal_type="SEXPS",
        reference=_vendor_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code=" ",
        hsn_sac_no=_safe_hsn(invoice),
        taxable_amount=round(invoice.taxable_amount, 2),
        gst_tax_rate=round(invoice.gst_rate / 2, 2) if invoice.gst_rate else None,
        advance_challan_no=config["expense_account"],  # dynamic
    )


def _row_vendor_credit_net(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    common = _common(invoice, config)
    common["branch_analysis_code"] = "GST02"
    return JournalEntryInvoice(
        **common,
        l_id="6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="C",
        jrnal_type="SEXPS",
        reference=_payment_ref(invoice),
        tds_applicability_analysis_code=" ",
        hsn_sac_no=None,
        taxable_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_vendor_credit_gst(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    total_gst = round(invoice.igst or (invoice.cgst + invoice.sgst), 2)
    common = _common(invoice, config)
    common["branch_analysis_code"] = "GST01"
    return JournalEntryInvoice(
        **common,
        l_id="6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=total_gst,
        dr_cr="C",
        jrnal_type="SEXPS",
        reference=_payment_ref(invoice),
        tds_applicability_analysis_code=" ",
        hsn_sac_no=None,
        taxable_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_payment_debit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    return JournalEntryInvoice(
        **_common(invoice, config),
        l_id="1;3;6;7",
        account_code=invoice.vendor_code,
        description=invoice.vendor_name,
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="D",
        jrnal_type="SPYMT",
        reference=_payment_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code=" ",
        hsn_sac_no=None,
        taxable_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


def _row_bank_credit(invoice: InvoiceExtract, config: dict) -> JournalEntryInvoice:
    common = _common(invoice, config)
    common["additional_remarks"] = "NEFT"
    common["underwriting_year_analysis_code"] = "EXPMG"  # FIX 4
    return JournalEntryInvoice(
        **common,
        l_id="6;7",
        account_code=BANK_ACCOUNT,
        description="HDFC EXPENSES CORPORATE",
        trans_amount=round(invoice.taxable_amount, 2),
        dr_cr="C",
        jrnal_type="SPYMT",
        reference=_payment_ref(invoice),
        branch_analysis_code=config["branch"],
        tds_applicability_analysis_code=" ",
        hsn_sac_no=None,
        taxable_amount=None,
        gst_tax_rate=None,
        advance_challan_no=None,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_journal_entries(invoice: InvoiceExtract) -> list[JournalEntryInvoice]:

    # Load vendor config — dynamic per vendor
    config = _load_vendor_config(invoice.vendor_gst)

    # Use vendor_code from master if invoice didn't have one
    if config["vendor_code"] and not invoice.vendor_code:
        invoice.vendor_code = config["vendor_code"]

    rows = []

    rows.append(_row_expense_debit(invoice, config))

    total_gst = invoice.igst or (invoice.cgst + invoice.sgst)
    if total_gst > 0:
        if invoice.igst > 0:
            rows.append(_row_igst_debit(invoice, config))
        else:
            rows.append(_row_sgst_debit(invoice, config))
            rows.append(_row_cgst_debit(invoice, config))

    rows.append(_row_vendor_credit_net(invoice, config))
    rows.append(_row_vendor_credit_gst(invoice, config))
    rows.append(_row_payment_debit(invoice, config))
    rows.append(_row_bank_credit(invoice, config))

    return rows