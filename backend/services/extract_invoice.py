import base64
import io
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.messages import SystemMessage , HumanMessage
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from models.invoice_model import InvoiceExtract
from dotenv import load_dotenv
from pdf2image import convert_from_bytes

load_dotenv()

client = genai.Client()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


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
    """



def extract_text(pdf_bytes: bytes):

    
    try:
        print("Reading PDF bytes and encoding to base64")
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
        mime_type = "application/pdf"

        # images = convert_from_bytes(pdf_bytes , dpi=300)

        # for img in images:
        #     buffered = io.BytesIO()
        #     img.save(buffered, format="PNG")
        #     image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        #     mime_type = "image/png"

        human_message = HumanMessage(
            content=[
                {"type": "text", "text": "Extract all invoice fields from this GST invoice:"},
                {"type": "image", "base64": pdf_base64, "mime_type": mime_type}
            ]
        )

        print("Extracting Invoice data")
        response = model.with_structured_output(InvoiceExtract).invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            human_message
        ])

        return response
    
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return ""  # Return empty string if all methods fail

