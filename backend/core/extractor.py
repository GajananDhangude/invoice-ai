import os
from core.llm import llm
from services.ocr import extract_text
from models.invoice_model import InvoiceExtract
import pandas as pd
from langchain_core.messages import SystemMessage , HumanMessage

output_dir = './output_folder'
file_path = os.path.join(output_dir, 'data.csv')

def generate_response(pdf_path:str) -> pd.DataFrame:
    print(f"extracting text from pdf: {pdf_path}")
    text = extract_text(pdf_path)  # Replace with your image file path
    print(text)
    print("text extracted:")

    SYSTEM_PROMPT = """
    You are an expert Indian GST invoice data extractor.

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
    """


    res = llm.with_structured_output(InvoiceExtract).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Extract invoice data from this text:\n{text}")
    ])


    return res

# if __name__ == "__main__":
#     res = generate_response('./uploads/AMAZON.pdf')
#     print(res)