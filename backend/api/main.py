
from fastapi import FastAPI , UploadFile , File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
from core.journal_builder import build_journal_excel
from models.invoice_model import InvoiceExtract
from core.generate_response import generate_response
from config.config_acc import ACC_PERIOD
from services.text_extractor import extract_with_fitz
from services.extract_invoice import extract_text
import json
import os
import uvicorn

app = FastAPI(
    title="Invoice Extractor API",
    description="API for extracting structured data from Indian GST invoices using OCR and LLMs.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    os.environ.get("FRONTEND_URL")
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("config/vendor_master.json") as f:
    VENDOR_MASTER = json.load(f)


@app.get("/")
def root():
    return {
        "message": "Invoice Journal Entry API is running",
        "docs": "/docs",
    }
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
 
@app.post("/extract")
async def extract(files: list[UploadFile] = File(...)):
    """
    Upload PDF → returns extracted invoice fields as JSON.
    React shows this to user for review.
    """
    results = []

    for file in files:
        # if file.content_type != "application/pdf":
        #     raise HTTPException(status_code=400, detail="Only PDF files are accepted")
 
        try:
            pdf_bytes = await file.read()
            
            text = extract_with_fitz(pdf_bytes)
            if text and len(text) > 100:
                print("Successfully extracted text with PyMuPDF")
                invoice = generate_response(text)
            
            else:
                print("Falling back to LLM for extraction")
                invoice  = extract_text(pdf_bytes)

            results.append({
                "filename":file.filename,
                "success": True,
                "invoice": invoice
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error":str(e)
            })

    return {"Total Files": len(files), "Results": results}



@app.post("/export-excel")
async def export(invoice_list: list[InvoiceExtract]):
    """
    Receives confirmed invoice JSON (from the /extract step) and
    returns a formatted Excel journal entry file for download.
    """
    invoices = []
 
    for invoice in invoice_list:
        try:
            data = invoice.model_dump()
 
            vendor_config = VENDOR_MASTER.get(data["vendor_gst"], VENDOR_MASTER["DEFAULT"])
 
            if data["vendor_gst"] not in VENDOR_MASTER:
                vendor_config = {
                    **VENDOR_MASTER["DEFAULT"],
                    "description": data["vendor_name"].upper() + " EXPENSES"
                }
 
            invoices.append({
                **data,
                **vendor_config,
                "acc_period": ACC_PERIOD,
                "narration": data.get("billing_period") or "",
            })
 
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Error processing invoice {invoice.invoice_number}: {str(e)}"
            )
 
    if not invoices:
        raise HTTPException(status_code=422, detail={"message": "No invoices provided"})
 
    excel_bytes = build_journal_excel(invoices)
 
    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=journal_entries.xlsx"}
    )


if __name__ =="__main__":

    uvicorn.run(
        "api.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )