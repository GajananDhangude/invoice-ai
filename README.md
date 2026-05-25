# 🧾 InvoiceExtractor
> Supercharge your accounting workflow by automating invoice data extraction and journal generation.

![Hero Banner](https://via.placeholder.com/1200x400/0f172a/ffffff.png?text=InvoiceExtractor+Hero+Banner)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Frontend: React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)

## 🚀 Overview

Manual data entry is tedious, slow, and prone to costly human errors. **InvoiceExtractor** bridges the gap between raw invoice PDFs and your accounting software. It automatically reads vendor invoices, maps them to journal entries, and exports CSVs ready for immediate ERP import. 

## ✨ Key Features

- **⚡ Automated Extraction:** Instantly extract line items, totals, dates, and metadata from PDF invoices.
- **🧠 Smart Journal Builder:** Automatically categorize and map extracted data to correct ledger accounts using a customizable vendor master configuration.
- **📊 Interactive Dashboard:** Review, edit, and approve extracted data in a fast, clean React interface before finalizing.
- **📥 One-Click Export:** Seamlessly generate formatted accounting journals as CSVs ready for import into QuickBooks, Xero, or custom ERPs.

## 🛠️ Tech Stack

| Domain | Technology | Description |
|---|---|---|
| **Frontend** | React, Vite | Fast, interactive user interface for invoice preview and review |
| **Backend** | Python, FastAPI, Pydantic | High-performance API and data validation |
| **Logic** | PDF Extraction Libs | Core invoice logic, parsing, and CSV generation |

## 🏁 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Node.js** v18+
- **Python** 3.10+
- **Git**

### Installation

Clone the repository to your local machine:
\\\ash
git clone https://github.com/yourusername/InvoiceExtractor.git
cd InvoiceExtractor
\\\

**1. Backend Setup**
\\\ash
cd backend
python -m venv .venv
# On Windows use: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
\\\

**2. Frontend Setup**
\\\ash
cd frontend
npm install
\\\

### Running the App

Start both the backend and frontend servers in separate terminals.

**Start the Backend API:**
\\\ash
cd backend
# Make sure your virtual environment is active
uvicorn api.main:app --reload
\\\

**Start the Frontend Client:**
\\\ash
cd frontend
npm run dev
\\\

Your app should now be running! Open your browser and navigate to \http://localhost:5173\.

## 💻 Usage Example

You can interact with InvoiceExtractor either via the intuitive UI or directly via the API. 

**API Example:** Extracting data from an invoice PDF via cURL:
\\\ash
curl -X POST "http://localhost:8000/api/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_invoice.pdf"
\\\

## 🗺️ Roadmap

- [x] Basic PDF text extraction
- [x] Vendor-to-Account mapping via configuration
- [x] CSV Journal export
- [ ] OCR support for scanned PDFs
- [ ] Advanced visual bounding-box extraction
- [ ] Direct ERP integration (e.g., Xero & QuickBooks APIs)

## 🤝 Contributing

We welcome contributions! Whether it is a bug report, new feature proposal, or a pull request, your input is highly valued.

1. Fork the repo and create your branch from \main\.
2. Ensure any new logic has robust tests.
3. Open a Pull Request with a clear description of your changes.

Please read our [Contributing Guidelines](#) prior to submitting a PR.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments / Contact

- Built with ❤️ by [Your Name/Team](#)
- Connect with us on [Twitter/X](#) or reach out via [Email](#).
