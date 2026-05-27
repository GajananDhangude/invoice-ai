import csv
import io
from models.journal_model import JournalEntryInvoice

# Column order must match the upload format template exactly
HEADERS = [
    "L id",
    "Acc Period",
    "Trans Date",
    "Account Code",
    "Description",
    "Curr Code",
    "Trans Amount",
    "Dr_Cr",
    "Jrnal Type",
    "Jrnal Source",
    "Reference",
    "Asset Code",
    "Asset Indicator",
    "Asset / Item Qty",
    "Due Date",
    "Branch Analysis Code",
    "Product Analysis Code",
    "Channel Analysis Code",
    "Sub-Channel Analysis Code",
    "Underwriting Year Analysis Code",
    "Employee Code Analysis Code",
    "TDS Applicability Analysis Code",
    "Department Analysis Code",
    "Sequence Code Analysis Code",
    "Vendor Code Analysis Code",
    "Invoice Date",
    "From Date",
    "To Date",
    "Addl Date 4",
    "Addl Date 5",
    "Cheque & NEFT Number",
    "Invoice Number",
    "Additional Remarks",
    "Additional Remarks 2",
    "Credence Description",
    "HSN/SAC NO",
    "Taxable on Amount",
    "Reverse Charge (Y/N)",
    "Reverse Charge %",
    "Item Details Sr No",
    "Goods/Service",
    "GST Tax Rate",
    "Original Invoice No for Dr/Cr Notes",
    "Advance Challan No",
]


def _format_date(d) -> str:
    """Convert date to DD/MM/YYYY — Excel reads this cleanly."""
    if d is None:
        return ""
    return d.strftime("%d/%m/%Y")


def _format_amount(amount) -> str:
    """Format float — empty string if None."""
    if amount is None:
        return ""
    return str(round(amount, 2))


def _row_to_values(row: JournalEntryInvoice) -> list:
    """Map one JournalEntryInvoice to a flat list matching HEADERS order."""
    return [
        row.l_id or "",
        row.acc_period or "",
        _format_date(row.trans_date),
        row.account_code or "",
        row.description or "",
        row.curr_code or "INR",
        _format_amount(row.trans_amount),
        row.dr_cr or "",
        row.jrnal_type or "",
        row.jrnal_source or "",
        row.reference or "",
        row.asset_code or "",
        row.asset_indicator or "",
        _format_amount(row.asset_item_qty),
        _format_date(row.due_date),
        row.branch_analysis_code or "",
        row.product_analysis_code or "",
        row.channel_analysis_code or "",
        row.sub_channel_analysis_code or "",
        row.underwriting_year_analysis_code or "",
        row.employee_code_analysis_code or "",
        row.tds_applicability_analysis_code or "",
        row.department_analysis_code or "",
        row.sequence_code_analysis_code or "",
        row.vendor_code_analysis_code or "",
        _format_date(row.invoice_date),
        _format_date(row.from_date),
        _format_date(row.to_date),
        _format_date(row.addl_date_4),
        _format_date(row.addl_date_5),
        row.cheque_neft_number or "",
        row.invoice_number or "",
        row.additional_remarks or "",
        row.additional_remarks_2 or "",
        row.credence_description or "",
        row.hsn_sac_no or "",
        _format_amount(row.taxable_amount),
        row.reverse_charge or "",
        _format_amount(row.reverse_charge_percent),
        row.item_details_sr_no or "",
        row.goods_service or "",
        _format_amount(row.gst_tax_rate),
        row.original_invoice_no_for_dr_cr_notes or "",
        row.advance_challan_no or "",
    ]


def generate_csv(rows: list[JournalEntryInvoice]) -> bytes:
    """
    Takes list of JournalEntryInvoice rows → returns CSV bytes.
    utf-8-sig encoding so Excel on Windows opens without garbling characters.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Header row
    writer.writerow(HEADERS)

    # Data rows
    for row in rows:
        writer.writerow(_row_to_values(row))

    # utf-8-sig adds BOM — required for Excel to read special chars correctly
    return buffer.getvalue().encode("utf-8-sig")


if __name__ == "__main__":
    from datetime import date
    from models.invoice_model import InvoiceExtract
    from core.journal_builder import build_journal_entries
    from backend.core.generate_response import generate_response

    invoice = generate_response('./uploads/AMAZON.pdf')


    rows = build_journal_entries(invoice)
    csv_bytes = generate_csv(rows)

    output_path = f"./output_folder/{invoice.invoice_number}.csv"
    with open(output_path, "wb") as f:
        f.write(csv_bytes)

    print(f"CSV saved to {output_path}")
    print(f"Total rows: {len(rows)}")