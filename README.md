# InvoiceExtractor

Automate Indian GST invoice extraction and generate accounting-ready journal CSVs — with a FastAPI backend and a review-first React dashboard.

> Replace `YOUR_GITHUB_ORG/YOUR_REPO` in the badge URLs once you publish.

[![CI](https://img.shields.io/github/actions/workflow/status/YOUR_GITHUB_ORG/YOUR_REPO/ci.yml?branch=main)](https://github.com/YOUR_GITHUB_ORG/YOUR_REPO/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Stars](https://img.shields.io/github/stars/YOUR_GITHUB_ORG/YOUR_REPO?style=social)](https://github.com/YOUR_GITHUB_ORG/YOUR_REPO)
[![Backend](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=000)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)

---

## Why this exists

Manual invoice-to-journal data entry is slow, repetitive, and error-prone — especially when you’re processing the same vendors every month.

InvoiceExtractor turns raw vendor PDFs into structured invoice data (JSON), lets you review/edit it in a clean UI, and exports a journal CSV suitable for ERP import workflows.

It’s designed for:

- Accounting / finance teams handling Indian GST invoices
- AP (Accounts Payable) operations looking to reduce manual entry
- Developers building internal tooling for invoice ingestion and journal automation

---

## Demo

- Live demo: _TBD_ (add your deployment link here)
- Video walkthrough: _TBD_

Suggested demo assets:

- `demo.gif` showing upload → review → export
- A sample invoice PDF in `examples/` (avoid real vendor PII)

---

## Screenshots

> Replace placeholders with real images once available.

| Upload | Review | Export |
|---|---|---|
| ![Upload](https://via.placeholder.com/600x340?text=Upload+Screen) | ![Review](https://via.placeholder.com/600x340?text=Review+Table) | ![Export](https://via.placeholder.com/600x340?text=CSV+Download) |

---

## Features

- PDF upload (multi-file) and structured invoice extraction (JSON)
- Review-first UI to validate and adjust extracted fields before exporting
- Vendor master mapping (GST → expense account, department, branch, etc.)
- Journal entry generation and one-click CSV export
- FastAPI interactive docs (`/docs`) and health endpoint (`/health`)

---

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | ⚛️ React + ⚡ Vite + 🎨 Tailwind CSS |
| Backend | 🐍 Python + 🚀 FastAPI + ✅ Pydantic |
| LLM extraction | 🤖 LangChain + Google Gemini (structured output) |
| CSV / data | 📄 pandas |

---

## Project structure

```text
.
├─ backend/
│  ├─ api/                 # FastAPI app (routes)
│  ├─ core/                # extraction + journal + CSV logic
│  ├─ config/              # vendor master mapping JSON
│  ├─ models/              # Pydantic models
│  ├─ services/            # service helpers (LLM integrations, etc.)
│  ├─ requirements.txt
│  └─ pyproject.toml
└─ frontend/
   ├─ src/
   │  ├─ api/              # axios client + API wrappers
   │  ├─ components/
   │  └─ pages/
   └─ package.json
```

---

## Installation

### Prerequisites

- Node.js `>= 18`
- Python `>= 3.10`

### 1) Backend setup (FastAPI)

```bash
cd backend
python -m venv .venv
```

Activate the venv:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your backend environment file:

```bash
# backend/.env
GOOGLE_API_KEY=your_google_api_key_here

# Optional: allow a deployed frontend origin in CORS
# FRONTEND_URL=https://your-frontend.example.com
```

Start the API:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

### 2) Frontend setup (React + Vite)

```bash
cd frontend
npm install
```

Create a frontend env file:

```bash
# frontend/.env
VITE_API_URL=http://127.0.0.1:8000
```

Run the dev server:

```bash
npm run dev
```

Open `http://localhost:5173`.

---

## Usage

### Web app

1. Open the dashboard at `http://localhost:5173`
2. Upload one or more invoice PDFs
3. Review extracted fields (vendor GST, invoice number/date, taxable amount, GST splits, etc.)
4. Export the generated journal as CSV

### API (cURL)

Extract invoice data from one or more PDFs:

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@sample_invoice.pdf" \
  -F "files=@another_invoice.pdf"
```

Generate a CSV from confirmed invoices (send the reviewed JSON back):

```bash
curl -X POST "http://127.0.0.1:8000/generate-csv" \
  -H "Content-Type: application/json" \
  --data-binary @invoices.json \
  --output journal_entries.csv
```

Where `invoices.json` is a JSON array matching the backend schema (see `/docs`).

---

## API documentation

The backend is self-documented via OpenAPI:

- Swagger UI: `GET /docs`
- OpenAPI JSON: `GET /openapi.json`

### Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | API status + docs link |
| `GET` | `/health` | Health check |
| `POST` | `/extract` | Upload PDFs → extracted invoice JSON |
| `POST` | `/generate-csv` | Confirmed invoices → downloadable CSV |

---

## Environment variables

### Backend (`backend/.env`)

This project uses `python-dotenv` to load env vars.

| Variable | Required | Purpose |
|---|---:|---|
| `GOOGLE_API_KEY` | ✅ | Google Gemini API key used by the extraction model |
| `FRONTEND_URL` | ⚠️ | Optional extra CORS origin (in addition to localhost) |

Notes:

- Never commit secrets. `backend/.gitignore` already ignores `.env`.

### Frontend (`frontend/.env`)

| Variable | Required | Purpose |
|---|---:|---|
| `VITE_API_URL` | ✅ | Base URL for the FastAPI server (used by axios) |

---

## Contributing

Contributions are welcome — especially around extraction accuracy, schema coverage, and accounting export formats.

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-change`
3. Make your changes (keep them small and focused)
4. Run checks:
   - Frontend: `cd frontend && npm run lint`
   - Backend: run the API and validate endpoints via `/docs`
5. Commit with a clear message
6. Open a Pull Request describing:
   - What you changed
   - Why you changed it
   - How to test it

---

## Roadmap

- [x] Multi-file PDF upload → structured invoice extraction
- [x] Vendor master mapping (`backend/config/vendor_master.json`)
- [x] Journal generation and CSV export
- [ ] OCR support for scanned PDFs
- [ ] Better validation + UI edit workflows for line items
- [ ] Pluggable exporters (Tally / SAP / QuickBooks / Xero formats)
- [ ] CI (lint, type checks, formatting)

---

## License

MIT (recommended for open-source).

> If you plan to publish this repository, add a `LICENSE` file at the repo root and update this section accordingly.

---

## Author / Maintainer

- Maintainer: Gajanan Dhangude
- Contact: 9579087176

---

## Acknowledgements

- FastAPI for the backend API framework
- React + Vite for the frontend developer experience
- LangChain and Google Gemini for structured extraction
