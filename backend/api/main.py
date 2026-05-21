from fastapi import FastAPI , UploadFile , File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from core.extractor import generate_response
from core.csv_writer import generate_csv
from core.journal_builder import build_journal_entries
from models.invoice_model import InvoiceExtract
from datetime import datetime
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
    "http://127.0.0.1:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


HISTORY_FILE = "./data/history.json"
os.makedirs("./data", exist_ok=True)
os.makedirs("./uploads", exist_ok=True)
 
 
def _load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)
 
 
def _save_to_history(invoice: InvoiceExtract):
    history = _load_history()
    history.append({
        "invoice_number": invoice.invoice_number,
        "invoice_date":   str(invoice.invoice_date),
        "vendor_name":    invoice.vendor_name,
        "vendor_gst":     invoice.vendor_gst,
        "net_amount":     invoice.net_amount,
        "taxable_amount": invoice.taxable_amount,
        "igst":           invoice.igst,
        "cgst":           invoice.cgst,
        "sgst":           invoice.sgst,
        "gst_rate":       invoice.gst_rate,
        "hsn_code":       invoice.hsn_code,
        "billing_period": invoice.billing_period,
        "processed_at":   datetime.now().isoformat(),
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
 
 
# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
 
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
async def extract(file: UploadFile = File(...)):
    """
    Upload PDF → returns extracted invoice fields as JSON.
    React shows this to user for review.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
 
    try:
        pdf_bytes = await file.read()
        temp_path = f"./uploads/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes)
 
        invoice = generate_response(temp_path)
        _save_to_history(invoice)
 
        return {
            "success": True,
            "invoice": invoice.model_dump(mode="json")
        }
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.post("/generate-csv")
async def generate_csv_endpoint(invoice: InvoiceExtract):
    """
    Send confirmed invoice data → returns CSV file for download.
    React calls this after user reviews extracted fields.
    """
    try:
        rows = build_journal_entries(invoice)
        csv_bytes = generate_csv(rows)
        filename = f"journal_{invoice.invoice_number}.csv"
        return Response(
            content=csv_bytes,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/history")
def get_history():
    """Returns all previously processed invoices for the history page."""
    try:
        history = _load_history()
        return {
            "success": True,
            "total": len(history),
            "invoices": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/stats")
def get_stats():
    """Returns summary stats for the dashboard."""
    try:
        history = _load_history()
        total_amount = sum(h["net_amount"] for h in history)
        total_gst = sum(
            h["igst"] or (h["cgst"] + h["sgst"])
            for h in history
        )
        current_month = datetime.now().strftime("%Y-%m")
        this_month = [
            h for h in history
            if h["processed_at"].startswith(current_month)
        ]
        return {
            "success":        True,
            "total_invoices": len(history),
            "total_amount":   round(total_amount, 2),
            "total_gst":      round(total_gst, 2),
            "this_month":     len(this_month),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ =="__main__":

    uvicorn.run(
        "api.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )