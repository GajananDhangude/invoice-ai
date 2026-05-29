from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


class InvoiceExtract(BaseModel):
    invoice_number: str = Field(
        description=(
            "The unique invoice identifier. Look for labels like 'Invoice No.' or 'Inv No.' on Page 1. "
            "Strip out spaces or fluff, return just the alphanumeric code (e.g., 'ST/25-26/001')."
        )
    )
    invoice_date: date = Field(
        description=(
            "The formal invoice date (e.g., '1-Apr-26'). Parse it carefully and strictly convert it "
            "into standard ISO format: YYYY-MM-DD (e.g., '2026-04-01')."
        )
    )
    vendor_name: str = Field(
        description=(
            "The company SELLING the goods or services. Look at the absolute top left header of Page 1. "
            "(e.g., 'Saanvi Trading'). DO NOT extract the buyer/consignee name here."
        )
    )
    vendor_gst: str = Field(
        description=(
            "The 15-character GSTIN/UIN code belonging exclusively to the SELLER/VENDOR. "
            "Look right under the vendor's name at the top of Page 1. (e.g., '07AGVPT6721E1ZX'). "
            "Must be exactly 15 characters. Common OCR errors: 0↔O, 1↔I↔L, 5↔S, 8↔B, 9↔P, 6↔G."
        )
    )
    net_amount: float = Field(
        description=(
            "The final total grand amount payable by the buyer. Look at the absolute bottom right "
            "of the last page, near 'Grand Total' or 'Total' or 'Balance Due'. "
            "It must include all taxes. Remove commas, extract as a clean float (e.g., 9750.00)."
        )
    )
    taxable_amount: float = Field(
        description=(
            "The final aggregate subtotal BEFORE any GST taxes are added. "
            "CRITICAL: Do NOT pick up subtotals from intermediate pages labeled 'continued...'. "
            "Look exclusively at the absolute final page of the invoice. "
            "For MIXED GST RATE invoices, sum ALL HSN-wise taxable values across all rates. "
            "Find the value in the final tax summary section labelled 'Total Taxable Value' or 'Total'. "
            "Must be a single grand total float value (e.g., 8874.00)."
        )
    )
    vendor_code: Optional[str] = Field(
        default=None,
        description=(
            "An internal alphanumeric vendor code assigned to the seller. "
            "Leave as null/None if it is not explicitly printed as a distinct field on the invoice."
        )
    )
    hsn_code: Optional[str] = Field(
        default=None,
        description=(
            "The dominant or primary HSN/SAC code listed in the items column or the tax table. "
            "If multiple are listed, extract the most frequent one (e.g., '3402')."
        )
    )
    billing_period: Optional[str] = Field(
        default=None,
        description=(
            "The date range or service period if specified (e.g., 'April 2026'). "
            "Leave as null/None if it is a standard product invoice without a service period."
        )
    )
    place_of_supply: Optional[str] = Field(
        default=None,
        description=(
            "The state name listed under 'Place of Supply' or the State Name of the Vendor/Buyer "
            "(e.g., 'Delhi'). Extract only the text name of the state."
        )
    )
    gst_rate: float = Field(
        description=(
            "The dominant combined GST rate percentage (e.g., 18.0). "
            "If not explicitly printed, calculate by adding CGST% + SGST% (e.g., 9% + 9% = 18.0). "
            "For mixed-rate invoices, use the most prevalent rate. "
            "CRITICAL: Return ONLY the percentage number (like 18.0), NOT the rupee amount."
        )
    )
    cgst: float = Field(
        default=0.0,
        description=(
            "The grand total Central GST amount summed across ALL HSN rows and ALL pages. "
            "Look at the final totals table at the absolute bottom of the last page. "
            "For mixed-rate invoices, add all CGST amounts together (e.g., 348.39 + 5.98 = 354.37). "
            "Keep 0.0 if this is an interstate IGST transaction."
        )
    )
    sgst: float = Field(
        default=0.0,
        description=(
            "The grand total State/UT GST amount summed across ALL HSN rows and ALL pages. "
            "Look at the final totals table at the absolute bottom of the last page. "
            "For mixed-rate invoices, add all SGST amounts together. "
            "Keep 0.0 if this is an interstate IGST transaction."
        )
    )
    igst: float = Field(
        default=0.0,
        description=(
            "The grand total Integrated GST amount from the final totals table on the last page. "
            "If the transaction is intrastate (same state buyer and seller), this must be 0.0."
        )
    )

    @model_validator(mode="after")
    def validate_totals(self):
        total_tax = round(self.cgst + self.sgst + self.igst, 2)
        expected_net = round(self.taxable_amount + total_tax, 2)
        tolerance = 2.0

        if abs(expected_net - self.net_amount) > tolerance:
            raise ValueError(
                f"Invoice totals mismatch: "
                f"taxable({self.taxable_amount}) + tax({total_tax}) = {expected_net} "
                f"but net_amount is {self.net_amount}. "
                f"Difference: {round(abs(expected_net - self.net_amount), 2)}. "
                f"Re-check taxable_amount and GST figures from the final summary table."
            )
        return self