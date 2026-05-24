from fastapi import FastAPI , UploadFile , File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from core.extract_invoice import extract_text
from core.csv_writer import generate_csv
from core.journal_builder import build_journal_entries
from models.invoice_model import InvoiceExtract
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
            invoice = extract_text(pdf_bytes)
            results.append({
                "filename":file.filename,
                "success": True,
                "invoice": invoice.model_dump(mode="json")
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error":str(e)
            })
        
        return {"Total Files": len(files), "Results": results}
    
 
@app.post("/generate-csv")
async def generate_csv_endpoint(invoices: list[InvoiceExtract]):
    """
    Send confirmed invoice data → returns CSV file for download.
    React calls this after user reviews extracted fields.
    """
    try:
        all_rows = []
        for invoice in invoices:
            rows = build_journal_entries(invoice)
            all_rows.extend(rows)
        csv_bytes = generate_csv(all_rows)
        filename = f"journal_entries.csv"
        return Response(
            content=csv_bytes,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ =="__main__":

    uvicorn.run(
        "api.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )