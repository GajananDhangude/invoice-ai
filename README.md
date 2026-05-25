## Invoice Extractor

Extract structured data from Indian GST invoices and generate accounting-ready journal entries. The system combines a FastAPI backend that performs LLM-powered extraction with a React + Vite frontend for review and CSV export.

## Key Features

- Batch upload GST invoices (PDF or images)
- LLM extraction into a validated JSON schema
- Review and edit extracted fields before export
- Generate journal entry CSV for downstream accounting systems
- Simple REST API for integration

## Architecture

- Backend: FastAPI service that accepts files, runs extraction, and builds CSV
- Frontend: React UI for upload, review, and download
- Data rules: GST-specific parsing rules enforced in the extraction prompt

## Tech Stack

- Python 3.13+, FastAPI, Pydantic, LangChain, Google GenAI
- React 19, Vite, Tailwind CSS, Axios

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 18+
- A Google GenAI API key (for Gemini)

### Backend Setup

From the repository root:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend` with:

```bash
GOOGLE_API_KEY=your_key_here
FRONTEND_URL=http://localhost:5173
```

Run the API:

```bash
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

From the repository root:

```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend` with:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

Start the UI:

```bash
npm run dev
```

Open the app at `http://localhost:5173`.

## API Overview

Base URL: `http://127.0.0.1:8000`

- `GET /` Health message and docs link
- `GET /health` Service health check
- `POST /extract` Upload files and return extracted fields
- `POST /generate-csv` Submit confirmed invoices and download CSV

Swagger UI is available at `http://127.0.0.1:8000/docs`.

## Environment Variables

Backend:

- `GOOGLE_API_KEY` (required) Google GenAI key
- `FRONTEND_URL` (optional) Allowlist for CORS

Frontend:

- `VITE_API_URL` (required) Base URL for the backend API

## Notes

- The extractor is tuned for Indian GST invoices and will enforce GST-specific rules.
- If you run in a different environment, update CORS and API URLs accordingly.

## Troubleshooting

- If requests fail with CORS errors, confirm `FRONTEND_URL` matches the UI origin.
- If extraction fails, verify the GenAI key and internet access.

## License

Specify your license here.
