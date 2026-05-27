from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date

class InvoiceExtract(BaseModel):
    invoice_number: str = Field(
        description="The unique invoice identifier. Look for labels like 'Invoice No.' or 'Inv No.' on Page 1. Strip out spaces or fluff, return just the alphanumeric code (e.g., 'ST/25-26/001')."
    )
    invoice_date: date = Field(
        description="The formal invoice date (e.g., '1-Apr-26'). Parse it carefully and strictly convert it into standard ISO format: YYYY-MM-DD (e.g., '2026-04-01')."
    )
    vendor_name: str = Field(
        description="The company SELLING the goods or services. Look at the absolute top left header of Page 1. (e.g., 'Saanvi Trading'). DO NOT extract the buyer/consignee name here."
    )
    vendor_gst: str = Field(
        description="The 15-character GSTIN/UIN code belonging exclusively to the SELLER/VENDOR. Look right under the vendor's name at the top of Page 1. (e.g., '07AGVPT6721E1ZX')."
    )
    net_amount: float = Field(
        description="The final total grand amount payable by the buyer. Look at the absolute bottom right of the last page, near 'Grand Total' or 'Total'. It must include all taxes. Remove commas, extract as a clean float (e.g., 9750.00)."
    )
    taxable_amount: float = Field(
        description= (
            "The final aggregate subtotal BEFORE any GST taxes are added. "
            "CRITICAL: Do NOT pick up subtotals from intermediate pages labeled 'continued...'. "
            "Look exclusively at the absolute final page of the invoice. Find the value positioned directly "
            "above or left of the CGST/SGST breakdowns, or look for the summary label 'Total Taxable Value' "
            "in the final tax summary section (e.g., 8874.00). Must be a single total float value."
        )
    )

    vendor_code: Optional[str] = Field(
        default=None, 
        description="An internal alphanumeric vendor code assigned to the seller. Leave as null/None if it is not explicitly printed as a distinct field on the invoice."
    )
    hsn_code: Optional[str] = Field(
        default=None, 
        description="The dominant or primary HSN/SAC code listed in the items column or the tax table. If multiple are listed, extract the most frequent one (e.g., '3402')."
    )
    billing_period: Optional[str] = Field(
        default=None, 
        description="The date range or service period if specified (e.g., 'April 2026'). Leave as null/None if it is a standard product invoice without a service period."
    )
    place_of_supply: Optional[str] = Field(
        default=None, 
        description="The state name listed under 'Place of Supply' or the State Name of the Vendor/Buyer (e.g., 'Delhi'). Extract only the text name of the state."
    )
    
    gst_rate: float = Field(
        description=(
            "The final combined total GST rate percentage (e.g., 18.0). "
            "If the combined rate is not explicitly printed, you MUST calculate it by adding the "
            "Central Tax percentage rate and the State Tax percentage rate together (e.g., 9% CGST + 9% SGST = 18.0). "
            "CRITICAL: Return ONLY the percentage number (like 18.0), NOT the calculated tax currency amount in Rupees."
        )
    )

    cgst: float = Field(
        default=0.0, 
        description="The grand total Central GST amount summed up across all pages. Look at the final totals table at the absolute bottom of the document. Keep 0.0 if an interstate IGST transaction is active."
    )
    sgst: float = Field(
        default=0.0, 
        description="The grand total State/UT GST amount summed up across all pages. Look at the final totals table at the absolute bottom of the document. Keep 0.0 if an interstate IGST transaction is active."
    )
    igst: float = Field(
        default=0.0, 
        description="The grand total Integrated GST amount from the final totals table. If the transaction is within the same state (Intrastate), this field must be 0.0."
    )



@model_validator(mode="after")
def validate_totals(self):

    total_tax = (
        self.cgst_amount +
        self.sgst_amount +
        self.igst_amount
    )

    expected_total = round(
        self.taxable_amount + total_tax,
        2
    )

    tolerance = 2.0

    if abs(expected_total - self.gross_amount) > tolerance:
        raise ValueError(
            "Invoice totals mismatch"
        )

    return self

