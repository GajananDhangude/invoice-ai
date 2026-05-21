import easyocr
import cv2
from langchain_community.document_loaders import PyMuPDFLoader
from services.pdf_converter import convert_pdf_to_images


def extract_text(file_path:str):
    
    try:
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        text = "\n".join([doc.page_content for doc in documents])

        if text.strip():          # if we got meaningful text, stop here
            return text

    except Exception as e:
        print(f"PyMuPDF failed: {e}")

    # --- Level 2: EasyOCR (fallback for scanned/image-based PDFs) ---
    print("PyMuPDF returned no text — falling back to EasyOCR...")
    
    try:
        img_path = convert_pdf_to_images(file_path)
        img = cv2.imread(img_path)
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(img, detail=0)  # Perform OCR on the image

        extracted_text = '\n'.join(result)

        return extracted_text

    except Exception as e:
        print(f"EasyOCR failed: {e}")

if __name__ == "__main__":
    file_path = './uploads/AMAZON.pdf'  # Replace with your image file path
    text = extract_text(file_path)
    print(text)