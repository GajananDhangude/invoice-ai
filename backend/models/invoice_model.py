from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date

class InvoiceExtract(BaseModel):
    # Required
    invoice_number: str = Field(description="Invoice number from the GST invoice")
    invoice_date: date = Field(description="Invoice date — YYYY-MM-DD")
    vendor_name: str = Field(description="Vendor company name (seller, not buyer)")
    vendor_gst: str = Field(description="Vendor GST number from seller section")
    net_amount: float = Field(description="Total amount payable including GST")
    taxable_amount: float = Field(description="Amount before GST")

    # Optional
    vendor_code: Optional[str] = Field(default=None, description="Vendor code if printed")
    hsn_code: Optional[str] = Field(default=None, description="HSN or SAC code")
    billing_period: Optional[str] = Field(default=None, description="Billing period if mentioned")
    place_of_supply: Optional[str] = Field(default=None, description="Place of supply state")
    gst_rate: Optional[float] = Field(default=None, description="GST rate percentage")

    # GST amounts — always 0.0 if not applicable, never null
    cgst: float = Field(default=0.0, description="CGST amount")
    sgst: float = Field(default=0.0, description="SGST amount")
    igst: float = Field(default=0.0, description="IGST amount")

    @model_validator(mode="after")
    def derive_missing_fields(self) -> "InvoiceExtract":
        # Derive gst_rate from amounts if missing
        if self.gst_rate is None and self.taxable_amount > 0:
            total_gst = self.igst or (self.cgst + self.sgst)
            if total_gst > 0:
                self.gst_rate = round((total_gst / self.taxable_amount) * 100, 2)

        # Derive vendor_code from name if missing
        if self.vendor_code is None:
            self.vendor_code = self.vendor_name.upper().replace(" ", "")[:10]

        # Enforce IGST vs CGST/SGST mutual exclusivity
        if self.igst > 0:
            self.cgst = 0.0
            self.sgst = 0.0

        return self
    

