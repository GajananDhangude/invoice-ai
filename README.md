# Invoice Extractor

**GST invoices to accounting-ready journals. Fast. Reliable. Reviewable.**

![Hero banner placeholder](docs/hero.png)

![License](https://img.shields.io/badge/license-TBD-blue) ![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Version](https://img.shields.io/badge/version-0.1.0-informational)

## Intro

Invoice Extractor turns Indian GST invoices into clean, validated data and downloadable journal entries. It combines LLM-powered extraction with strict schema validation, then gives reviewers a fast UI to correct fields before export. The result is a practical pipeline from invoice PDFs to accounting-ready CSVs.

## Key Features

- **Batch-friendly ingestion**: Upload multiple GST invoices as PDFs or images in one shot.
- **Schema-locked extraction**: LLM output is validated against a strict JSON model.
- **Human-in-the-loop review**: Edit extracted fields before generating journal entries.
- **Accounting-grade exports**: Generate CSV journal entries ready for downstream systems.
- **API-first design**: Simple REST endpoints for integration or automation.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python 3.13+, FastAPI, Pydantic, LangChain, Google GenAI |
| Frontend | React 19, Vite, Tailwind CSS, Axios |

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 18+
- Google GenAI API key (Gemini)

### Installation

From the repository root:

```bash
cd backend
python -m venv .venv
\.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend`:

```bash
GOOGLE_API_KEY=your_key_here
FRONTEND_URL=http://localhost:5173
```

Then install the frontend:

```bash
cd ../frontend
npm install
```

Create a `.env` file inside `frontend`:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

### Running the App

Start the API:

```bash
cd backend
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Start the UI:

```bash
cd frontend
npm run dev
```

Open the app at `http://localhost:5173`.

## Usage Example

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
	-F "files=@/path/to/invoice.pdf"
```

## Roadmap

- [x] GST-tuned extraction prompts and schema validation
- [x] Review and edit flow before export
- [x] Journal CSV generation
- [ ] Saved templates for frequent vendors
- [ ] Multi-company workspaces and roles
- [ ] Background batch processing and queueing

## Contributing

Contributions are welcome. Please open an issue for bugs or feature requests. If you want to submit a PR, describe the change clearly, keep commits focused, and include tests or reproduction steps when relevant.

## License

This project is licensed under the [TBD](LICENSE) license.

## Acknowledgments / Contact

Thanks to all contributors and reviewers who help improve extraction accuracy. For support or collaboration, open an issue or reach out via your preferred contact channel.
