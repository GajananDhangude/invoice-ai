import os
from services.llm import llm

from models.invoice_model import InvoiceExtract
from langchain_core.messages import SystemMessage , HumanMessage


SYSTEM_PROMPT = """
    You are an advanced AI Invoice Extraction Engine for Indian GST invoices. Extract structured data from OCR text or images and return ONLY valid JSON matching the schema.

GENERAL RULES:
- Return ONLY valid JSON. Never hallucinate. Use null for genuinely missing optional fields.
- cgst, sgst, igst must be numbers. Use 0.0 if not applicable (never null).
- invoice_date format: YYYY-MM-DD.
- net_amount: Total payable including all taxes and round-offs.
- taxable_amount: Total amount BEFORE GST.
- vendor_name / vendor_gst: Extract SELLER details only. Ignore "Bill To" sections.
- Tax Rule: If IGST > 0 → cgst = 0.0, sgst = 0.0. If CGST/SGST > 0 → igst = 0.0.

GST NUMBER EXTRACTION:
- Valid GSTIN is exactly 15 alphanumeric characters.
- OCR often misreads characters (e.g., 0/O, 1/I/L, 5/S, 8/B, 9/P). Re-read carefully if the count is not 15.
- Prioritize the vendor's GSTIN at the top of the invoice. Never use the buyer's GSTIN.

TAXABLE AMOUNT & GST EXTRACTION (MULTI-PAGE / MIXED-RATE):
- Ignore partial subtotals on intermediate pages (marked "continued...").
- Use exclusively the FINAL tax summary table on the LAST page.
- For mixed GST rates (e.g., 18%, 5%, 0%), taxable_amount must be the SUM of all HSN taxable values across all rates.
- cgst and sgst must be the total SUM of all respective tax amounts across all rates.
- For utility bills: Use the pre-tax energy/service subtotal. Exclude deposits, arrears, or late fees.

MATHEMATICAL VALIDATION:
- Before outputting, mathematically verify: taxable_amount + cgst + sgst + igst ≈ net_amount (within ±2).
- If they do not balance, re-verify your extracted data points.

"""

def generate_response(text: str):

    # text = extract_text(pdf_bytes)  # Replace with your image file path


    res = llm.with_structured_output(InvoiceExtract).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Extract invoice data from this text:\n{text}")
    ])


    return res

# if __name__ == "__main__":

#     with open('C:/Users/dhang/Downloads/VT36546 - Saanvi Trading.pdf', 'rb') as f:
#         pdf_bytes = f.read()
#     res = generate_response(pdf_bytes)
#     print(res)