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
  const [results, setResults] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const handleFiles = async (files) => {
    if (!files?.length) return;
    setError("");
    setResults([]);
    setActiveIndex(0);
    setIsExtracting(true);

    try {
      const { data } = await extractInvoice(files);
      const normalizedResults = data.Results || [];
      setResults(normalizedResults);
      const firstSuccessIndex = normalizedResults.findIndex(
        (item) => item.success && item.invoice
      );
      setActiveIndex(firstSuccessIndex === -1 ? 0 : firstSuccessIndex);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Upload failed.");
    } finally {
      setIsExtracting(false);
    }
  };

  const onFieldChange = (field, value) => {
    setResults((prev) =>
      prev.map((item, index) => {
        if (index !== activeIndex || !item.invoice) return item;
        if (numericFields.has(field)) {
          const parsed = Number(value);
          return {
            ...item,
            invoice: {
              ...item.invoice,
              [field]: Number.isNaN(parsed) ? 0 : parsed,
            },
          };
        }
        return {
          ...item,
          invoice: {
            ...item.invoice,
            [field]: value,
          },
        };
      })
    );
  };

  const handleGenerateCsv = async () => {
    const confirmedInvoices = results
      .filter((item) => item.success && item.invoice)
      .map((item) => item.invoice);
    if (!confirmedInvoices.length) return;
    setIsGenerating(true);
    setError("");

    try {
      const { data } = await generateCsv(confirmedInvoices);
      const blob = new Blob([data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "journal_entries.csv";
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
          Drag PDF or image invoices and let the system auto-generate journal entries.
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
          const droppedFiles = Array.from(event.dataTransfer.files || []);
          handleFiles(droppedFiles);
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
              Drop your PDFs or images here
            </div>
            <div className="text-sm text-slate-400">
              or click to browse files
            </div>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,image/*"
          multiple
          className="hidden"
          onChange={(event) => {
            const selectedFiles = Array.from(event.target.files || []);
            handleFiles(selectedFiles);
          }}
        />
      </div>

      {results.length > 0 && (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-4">
            <div className="text-sm font-semibold text-slate-200">
              Extracted files
            </div>
            <div className="mt-3 grid gap-2">
              {results.map((item, index) => (
                <button
                  key={`${item.filename}-${index}`}
                  type="button"
                  onClick={() => setActiveIndex(index)}
                  className={`flex w-full items-center justify-between rounded-xl border px-4 py-3 text-left text-sm transition ${
                    index === activeIndex
                      ? "border-indigo-500/60 bg-indigo-500/10 text-indigo-100"
                      : "border-slate-800/80 bg-slate-950/40 text-slate-300 hover:border-indigo-400/40"
                  }`}
                >
                  <span className="truncate">{item.filename}</span>
                  <span className="text-xs uppercase tracking-wide">
                    {item.success ? "Ready" : "Failed"}
                  </span>
                </button>
              ))}
            </div>
          </div>

          <InvoicePreview
            invoice={results[activeIndex]?.invoice || null}
            onFieldChange={onFieldChange}
            disabled={isExtracting}
          />
        </div>
      )}

      {results.some((item) => item.success && item.invoice) && (
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
