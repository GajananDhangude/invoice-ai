import io
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
import fitz


def extract_with_fitz(pdf_bytes: bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()
    
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
        return None



def extract_with_docling(pdf_bytes: bytes):
    try:
        source_stream = DocumentStream(
            name="invoice.pdf",
            stream=io.BytesIO(pdf_bytes) 
        )
        print("Converting PDF bytes to text using Docling")
        converter = DocumentConverter()
        extracted_text = converter.convert(source_stream)
        markdown_text = extracted_text.document.export_to_markdown()

        return markdown_text
    
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return None
    
def extract_text(pdf_bytes: bytes):
    text = extract_with_fitz(pdf_bytes)
    if text and len(text) > 100:  # Arbitrary threshold to check if extraction was successful
        print("Successfully extracted text with PyMuPDF")
        return text
    else:
        print("Falling back to Docling for extraction")
        
        text = extract_with_docling(pdf_bytes)

        return text