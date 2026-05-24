import { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Sparkles } from "lucide-react";
import { extractInvoice, generateCsv } from "../api/invoice.js";
import DropZone from "../components/DropZone.jsx";
import InvoicePreview from "../components/InvoicePreview.jsx";
import AmountCard from "../components/AmountCard.jsx";
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
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");
  const [toast, setToast] = useState({ message: "", type: "success" });
  const [showConfetti, setShowConfetti] = useState(false);
  const [typedText, setTypedText] = useState("");

  const gstTotal = useMemo(() => {
    if (!invoice) return 0;
    return invoice.igst || (invoice.cgst || 0) + (invoice.sgst || 0);
  }, [invoice]);

  const handleFile = async (file) => {
    if (!file) return;
    setError("");
    setInvoice(null);
    setFileName(file.name || "GST Invoice.pdf");
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

  useEffect(() => {
    if (!isExtracting) {
      setTypedText("");
      return undefined;
    }
    const message = "Extracting invoice data...";
    let index = 0;
    const timer = setInterval(() => {
      index += 1;
      setTypedText(message.slice(0, index));
      if (index >= message.length) clearInterval(timer);
    }, 60);
    return () => clearInterval(timer);
  }, [isExtracting]);

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
      setToast({ message: "Journal entry ready!", type: "success" });
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 2200);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "CSV generation failed.");
      setToast({ message: "Export failed. Please retry.", type: "error" });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-12 pb-20">
      <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
        <div>
          <div className="text-xs font-semibold uppercase tracking-widest text-indigo-300">
            Extraction Command Center
          </div>
          <h2 className="brand-heading mt-4 text-4xl font-semibold leading-tight text-white">
            Upload invoices. <span className="text-gradient">Ship journal-ready CSVs.</span>
          </h2>
          <p className="mt-4 text-lg text-slate-300">
            Drag and drop GST PDFs. The engine extracts every field with GST-aware validation
            and keeps you in control with inline editing.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            {["SOC 2 aligned", "99.9% uptime", "Audit-ready outputs"].map((item) => (
              <span
                key={item}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-slate-300"
              >
                {item}
              </span>
            ))}
          </div>
        </div>
        <div className="glass-card rounded-[2rem] border border-white/5 p-6">
          <div className="brand-heading text-lg font-semibold text-white">Processing SLA</div>
          <div className="mt-4 grid gap-4">
            {[
              { label: "Median extraction time", value: "4.2s" },
              { label: "First-pass accuracy", value: "98.7%" },
              { label: "Retention window", value: "30 days" },
            ].map((item) => (
              <div key={item.label} className="rounded-2xl border border-white/5 bg-slate-950/40 px-4 py-3">
                <div className="text-xs font-semibold uppercase tracking-widest text-slate-400">
                  {item.label}
                </div>
                <div className="brand-heading mt-2 text-lg font-semibold text-white">{item.value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {error && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 px-5 py-4 text-sm text-rose-100">
          {error}
        </div>
      )}

      <div className="grid gap-10 lg:grid-cols-[1.05fr_0.95fr]">
        <div>
          <DropZone
            isDragging={isDragging}
            isExtracting={isExtracting}
            fileName={fileName}
            onClick={() => inputRef.current?.click()}
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
          />
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(event) => handleFile(event.target.files?.[0])}
          />
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <AmountCard label="Taxable Amount" value={invoice?.taxable_amount || 0} />
            <AmountCard label="GST Total" value={gstTotal} highlight />
            <AmountCard label="Net Amount" value={invoice?.net_amount || 0} />
          </div>
        </div>

        <AnimatePresence mode="wait">
          {invoice ? (
            <motion.div
              key="preview"
              initial={{ opacity: 0, x: 40 }}
              animate={{ opacity: 1, x: 0, transition: { duration: 0.5 } }}
              exit={{ opacity: 0, x: 20, transition: { duration: 0.3 } }}
            >
              <InvoicePreview
                invoice={invoice}
                onFieldChange={onFieldChange}
                disabled={isExtracting}
              />
            </motion.div>
          ) : (
            <motion.div
              key="placeholder"
              initial={{ opacity: 0, x: 40 }}
              animate={{ opacity: 1, x: 0, transition: { duration: 0.5 } }}
              exit={{ opacity: 0, x: 20, transition: { duration: 0.3 } }}
              className="glass-card flex h-full flex-col items-center justify-center rounded-[2rem] border border-white/5 p-8 text-center"
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-500/15 text-indigo-200">
                <Sparkles className="h-6 w-6" />
              </div>
              <div className="brand-heading mt-6 text-xl font-semibold text-white">
                Preview appears here
              </div>
              <p className="mt-3 text-sm text-slate-400">
                Upload a GST invoice to inspect, edit, and export.
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {invoice && (
        <button
          type="button"
          onClick={handleGenerateCsv}
          disabled={isGenerating}
          className="shimmer glow-button w-full rounded-2xl bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400 px-8 py-5 text-base font-semibold text-white shadow-[0_0_40px_rgba(99,102,241,0.35)] transition-all hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              Finalizing CSV export...
            </span>
          ) : (
            "Generate Journal Entry CSV"
          )}
        </button>
      )}

      <Toast
        message={toast.message}
        type={toast.type}
        onClose={() => setToast({ message: "", type: "success" })}
      />

      <AnimatePresence>
        {showConfetti && (
          <motion.div
            className="pointer-events-none fixed inset-0 z-50 flex items-start justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="mt-16 flex gap-2">
              {Array.from({ length: 12 }, (_, index) => (
                <span
                  key={index}
                  className="h-3 w-3 rounded-full bg-indigo-400"
                  style={{
                    animation: `fadeUp 1.6s ease ${index * 0.05}s forwards`,
                    opacity: 0,
                  }}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {isExtracting && (
          <motion.div
            className="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/80 backdrop-blur-xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="glass-card rounded-[2rem] border border-white/10 px-10 py-12 text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-cyan-400 text-white shadow-[0_0_30px_rgba(99,102,241,0.4)]">
                <Sparkles className="h-7 w-7" />
              </div>
              <div className="brand-heading mt-6 text-2xl font-semibold text-white">Gemini is working</div>
              <p className="typewriter mt-3 text-sm text-indigo-200">{typedText}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
