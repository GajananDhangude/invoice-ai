from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class JournalEntryInvoice(BaseModel):

    # --- Row identifier ---
    l_id: Optional[str] = Field(
        default=None,
        description="Row identifier e.g. 1;3;6;7 or 6;7"
    )

    # --- Core Accounting Fields ---
    acc_period: Optional[str] = Field(
        default=None,
        description="Accounting period e.g. 2026/001"
    )
    trans_date: Optional[date] = Field(
        default=None,
        description="Transaction date"
    )
    account_code: Optional[str] = Field(
        default=None,
        description="GL or expense account code e.g. 1310020100"
    )
    description: Optional[str] = Field(
        default=None,
        description="Nature of expense e.g. IT CLOUD INFRA EXPENSES"
    )
    curr_code: Optional[str] = Field(
        default="INR",
        description="Currency code"
    )
    trans_amount: Optional[float] = Field(
        default=None,
        description="Transaction amount"
    )
    dr_cr: Optional[str] = Field(
        default=None,
        description="D for Debit, C for Credit"
    )
    jrnal_type: Optional[str] = Field(
        default=None,
        description="Journal type — SEXPS for expense booking, SPYMT for payment"
    )
    jrnal_source: Optional[str] = Field(
        default=None,
        description="Journal source — not applicable, leave blank"
    )
    reference: Optional[str] = Field(
        default=None,
        description="Vendor code and vendor name e.g. CMS0019487/GREEN CLEAN SERVICE"
    )

    # --- Asset Related (always blank) ---
    asset_code: Optional[str] = None
    asset_indicator: Optional[str] = None
    asset_item_qty: Optional[float] = None
    due_date: Optional[date] = None

    # --- Analysis Codes ---
    branch_analysis_code: Optional[str] = Field(
        default=None,
        description="Branch code e.g. LXS00, or GST01/GST02 for vendor credit rows"
    )
    product_analysis_code: Optional[str] = Field(
        default="_NA",
        description="Not applicable — always _NA"
    )
    channel_analysis_code: Optional[str] = Field(
        default=None,
        description="Channel code e.g. CC004"
    )
    sub_channel_analysis_code: Optional[str] = Field(
        default="_NA",
        description="Not applicable — always _NA"
    )
    underwriting_year_analysis_code: Optional[str] = Field(
        default="_NA",
        description="Not applicable — always _NA"
    )
    employee_code_analysis_code: Optional[str] = Field(
        default="_NA",
        description="Not applicable — always _NA"
    )
    tds_applicability_analysis_code: Optional[str] = Field(
        default=None,
        description="TD01 or TD02 if TDS applicable, _NA otherwise"
    )
    department_analysis_code: Optional[str] = Field(
        default=None,
        description="Department code e.g. SRO"
    )
    sequence_code_analysis_code: Optional[str] = Field(
        default="_NA",
        description="Not applicable — always _NA"
    )
    vendor_code_analysis_code: Optional[str] = Field(
        default=None,
        description="Vendor code e.g. CMS0019487"
    )

    # --- Date Fields ---
    invoice_date: Optional[date] = Field(
        default=None,
        description="Invoice date from the vendor invoice"
    )
    from_date: Optional[date] = Field(
        default=None,
        description="Not applicable"
    )
    to_date: Optional[date] = Field(
        default=None,
        description="Not applicable"
    )
    addl_date_4: Optional[date] = None
    addl_date_5: Optional[date] = None

    # --- Invoice Reference Fields ---
    cheque_neft_number: Optional[str] = Field(
        default=None,
        description="Vendor GST number goes here"
    )
    invoice_number: Optional[str] = Field(
        default=None,
        description="Vendor invoice number"
    )
    additional_remarks: Optional[str] = Field(
        default=None,
        description="NEFT or Cheque — filled only on bank credit row"
    )
    additional_remarks_2: Optional[str] = Field(
        default=None,
        description="Not applicable"
    )
    credence_description: Optional[str] = Field(
        default=None,
        description="Not applicable"
    )

    # --- Tax Fields ---
    hsn_sac_no: Optional[str] = Field(
        default=None,
        description="HSN or SAC code — filled only on GST rows"
    )
    taxable_amount: Optional[float] = Field(
        default=None,
        description="Taxable amount before GST — filled only on GST rows"
    )
    reverse_charge: Optional[str] = Field(
        default=None,
        description="Y or N — not applicable"
    )
    reverse_charge_percent: Optional[float] = Field(
        default=None,
        description="Not applicable"
    )
    item_details_sr_no: Optional[str] = Field(
        default=None,
        description="Not applicable"
    )
    goods_service: Optional[str] = Field(
        default=None,
        description="Not applicable"
    )
    gst_tax_rate: Optional[float] = Field(
        default=None,
        description="GST rate % — filled only on GST rows e.g. 9 or 18"
    )

    # --- GST / Challan Reference ---
    original_invoice_no_for_dr_cr_notes: Optional[str] = Field(
        default=None,
        description="Royal Sundaram's own GST number"
    )
    advance_challan_no: Optional[str] = Field(
        default=None,
        description="Expense account code — filled only on GST rows e.g. 1310020100"
    )