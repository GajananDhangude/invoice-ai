import os
from services.docling_extractor import extract_text
from services.llm import llm
# from core.extract_invoice import extract_text
from models.invoice_model import InvoiceExtract
from langchain_core.messages import SystemMessage , HumanMessage


SYSTEM_PROMPT = """
    You are an advanced AI Invoice Extraction Engine specialized in Indian GST invoices.

Your task is to accurately extract structured invoice information from OCR text or invoice images and return ONLY valid JSON.

    Rules:
    - Return ONLY valid JSON matching the schema exactly
    - Never hallucinate — use null for genuinely missing optional fields
    - cgst, sgst, igst are always numbers — use 0.0 if not applicable, never null
    - invoice_date must be YYYY-MM-DD
    - net_amount is the TOTAL payable including GST
    - taxable_amount is the amount BEFORE GST
    - vendor_name is the SELLER — ignore the "Issued To / Bill To" section
    - vendor_gst is the SELLER's GST number — not the buyer's
    - If IGST is present → cgst and sgst are 0.0
    - If CGST+SGST present → igst is 0.0

MATHEMATICAL INVARIANT VALIDATION RULE:
    Before outputting the JSON payload, verify that the fields conform to this exact formula:
    [taxable_amount] + [cgst] + [sgst] + [igst] must roughly equal [net_amount] (accounting for small rounding variances). 
    If the 'taxable_amount' you selected does not satisfy this formula balance, you have picked an incorrect intermediate page subtotal line. Recalculate and pull the master total value from the absolute final page matrix.
"""

def generate_response(pdf_bytes: bytes):

    text = extract_text(pdf_bytes)  # Replace with your image file path


    res = llm.with_structured_output(InvoiceExtract).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Extract invoice data from this text:\n{text}")
    ])


    return res

if __name__ == "__main__":

    with open('C:/Users/dhang/Downloads/VT36546 - Saanvi Trading.pdf', 'rb') as f:
        pdf_bytes = f.read()
    res = generate_response(pdf_bytes)
    print(res)