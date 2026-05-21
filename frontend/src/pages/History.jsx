import { useEffect, useMemo, useState } from "react";
import { Search, Loader2 } from "lucide-react";
import { generateCsv, getHistory } from "../api/invoice.js";
import Toast from "../components/Toast.jsx";

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(value || 0);

const formatDate = (value) => {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [toast, setToast] = useState("");
  const [activeInvoice, setActiveInvoice] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadHistory = async () => {
      try {
        setLoading(true);
        const { data } = await getHistory();
        if (mounted) setHistory(data.invoices || []);
      } catch (err) {
        if (mounted) setError(err.message || "Failed to load history.");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadHistory();

    return () => {
      mounted = false;
    };
  }, []);

  const filteredHistory = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return history;
    return history.filter((invoice) =>
      `${invoice.vendor_name || ""} ${invoice.invoice_number || ""}`
        .toLowerCase()
        .includes(term)
    );
  }, [history, query]);

  const handleRegenerate = async (invoice) => {
    setActiveInvoice(invoice.invoice_number || invoice.processed_at || "active");
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
      setToast("CSV regenerated successfully.");
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "CSV download failed.");
    } finally {
      setActiveInvoice("");
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <div className="text-2xl font-semibold text-slate-100">History</div>
        <div className="text-sm text-slate-400">
          Review all processed invoices and regenerate journal entries.
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="relative w-full max-w-lg">
          <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          <input
            className="w-full rounded-2xl border border-slate-800/80 bg-slate-950/40 py-3 pl-11 pr-4 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none"
            placeholder="Search by vendor or invoice number"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>
        <div className="text-xs text-slate-400">
          {filteredHistory.length} invoices
        </div>
      </div>

      {loading ? (
        <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6 text-slate-400">
          Loading history...
        </div>
      ) : !filteredHistory.length ? (
        <div className="rounded-2xl border border-dashed border-slate-800/80 bg-slate-900/40 p-6 text-slate-400">
          No invoices found. Upload a GST invoice to build your history.
        </div>
      ) : (
        <div className="overflow-hidden rounded-2xl border border-slate-800/70 bg-slate-900/60">
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-slate-900/80 text-slate-400">
                <tr>
                  <th className="px-5 py-4 font-medium">Vendor</th>
                  <th className="px-5 py-4 font-medium">Invoice No</th>
                  <th className="px-5 py-4 font-medium">Invoice Date</th>
                  <th className="px-5 py-4 font-medium">Taxable Amount</th>
                  <th className="px-5 py-4 font-medium">GST Amount</th>
                  <th className="px-5 py-4 font-medium">Processed At</th>
                  <th className="px-5 py-4 font-medium">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80">
                {filteredHistory.map((invoice) => (
                  <tr key={`${invoice.invoice_number}-${invoice.processed_at}`}>
                    <td className="px-5 py-4 text-slate-100">
                      {invoice.vendor_name || "-"}
                    </td>
                    <td className="px-5 py-4 text-slate-300">
                      {invoice.invoice_number || "-"}
                    </td>
                    <td className="px-5 py-4 text-slate-300">
                      {formatDate(invoice.invoice_date)}
                    </td>
                    <td className="px-5 py-4 text-slate-300">
                      {formatCurrency(invoice.taxable_amount || invoice.net_amount)}
                    </td>
                    <td className="px-5 py-4 text-slate-300">
                      {formatCurrency(
                        invoice.igst || (invoice.cgst || 0) + (invoice.sgst || 0)
                      )}
                    </td>
                    <td className="px-5 py-4 text-slate-300">
                      {formatDate(invoice.processed_at)}
                    </td>
                    <td className="px-5 py-4">
                      <button
                        type="button"
                        onClick={() => handleRegenerate(invoice)}
                        className="inline-flex items-center gap-2 rounded-lg border border-indigo-500/40 px-3 py-2 text-xs font-semibold text-indigo-200 transition hover:border-indigo-500 hover:bg-indigo-500/20"
                        disabled={
                          activeInvoice ===
                          (invoice.invoice_number || invoice.processed_at)
                        }
                      >
                        {activeInvoice ===
                        (invoice.invoice_number || invoice.processed_at) ? (
                          <>
                            <Loader2 className="h-3 w-3 animate-spin" />
                            Generating
                          </>
                        ) : (
                          "Re-generate CSV"
                        )}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <Toast message={toast} onClose={() => setToast("")} />
    </div>
  );
}
