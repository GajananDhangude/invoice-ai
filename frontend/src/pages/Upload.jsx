import { useRef, useState } from "react";
import { CloudUpload, Loader2 } from "lucide-react";
import { extractInvoice, generateCsv } from "../api/invoice.js";
import InvoicePreview from "../components/InvoicePreview.jsx";
import Toast from "../components/Toast.jsx";

const numericFields = new Set([
  "taxable_amount",
  "cgst",
  "sgst",
  "igst",
  "gst_rate",
  "net_amount",
]);

export default function Upload() {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [invoice, setInvoice] = useState(null);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const handleFile = async (file) => {
    if (!file) return;
    setError("");
    setInvoice(null);
    setIsExtracting(true);

    try {
      const { data } = await extractInvoice(file);
      setInvoice(data.invoice);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Upload failed.");
    } finally {
      setIsExtracting(false);
    }
  };

  const onFieldChange = (field, value) => {
    setInvoice((prev) => {
      if (!prev) return prev;
      if (numericFields.has(field)) {
        const parsed = Number(value);
        return { ...prev, [field]: Number.isNaN(parsed) ? 0 : parsed };
      }
      return { ...prev, [field]: value };
    });
  };

  const handleGenerateCsv = async () => {
    if (!invoice) return;
    setIsGenerating(true);
    setError("");

    try {
      const { data } = await generateCsv(invoice);
      const blob = new Blob([data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `journal_${invoice.invoice_number || "invoice"}.csv`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setToast("CSV generated and downloaded successfully.");
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "CSV generation failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <div className="text-2xl font-semibold text-slate-100">
          Upload GST Invoice
        </div>
        <div className="text-sm text-slate-400">
          Drag a PDF invoice and let the system auto-generate journal entries.
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      <div
        className={`flex cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed px-6 py-16 text-center transition ${
          isDragging
            ? "border-indigo-500 bg-indigo-500/10"
            : "border-slate-800/80 bg-slate-900/40 hover:border-indigo-400/60"
        }`}
        onDragEnter={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={(event) => {
          event.preventDefault();
          setIsDragging(false);
        }}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          const file = event.dataTransfer.files?.[0];
          handleFile(file);
        }}
        onClick={() => inputRef.current?.click()}
      >
        {isExtracting ? (
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="h-10 w-10 animate-spin text-indigo-400" />
            <div className="text-sm text-slate-300">
              Extracting invoice data...
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div className="rounded-full bg-indigo-500/15 p-4 text-indigo-200">
              <CloudUpload size={28} />
            </div>
            <div className="text-lg font-semibold text-slate-100">
              Drop your PDF here
            </div>
            <div className="text-sm text-slate-400">
              or click to browse files
            </div>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(event) => handleFile(event.target.files?.[0])}
        />
      </div>

      <InvoicePreview
        invoice={invoice}
        onFieldChange={onFieldChange}
        disabled={isExtracting}
      />

      {invoice && (
        <button
          type="button"
          onClick={handleGenerateCsv}
          disabled={isGenerating}
          className="w-full rounded-2xl bg-indigo-500 px-6 py-4 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isGenerating ? "Generating CSV..." : "Generate CSV"}
        </button>
      )}

      <Toast message={toast} onClose={() => setToast("")} />
    </div>
  );
}
