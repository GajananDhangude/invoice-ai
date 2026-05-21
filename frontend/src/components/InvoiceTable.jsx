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
  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

export default function InvoiceTable({
  invoices,
  onDownload,
  emptyMessage,
  loading,
  showActions = true,
}) {
  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6 text-slate-400">
        Loading invoices...
      </div>
    );
  }

  if (!invoices.length) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-800/80 bg-slate-900/40 p-6 text-slate-400">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800/70 bg-slate-900/60">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-900/80 text-slate-400">
            <tr>
              <th className="px-5 py-4 font-medium">Vendor</th>
              <th className="px-5 py-4 font-medium">Invoice No</th>
              <th className="px-5 py-4 font-medium">Amount</th>
              <th className="px-5 py-4 font-medium">GST</th>
              <th className="px-5 py-4 font-medium">Date</th>
              {showActions && <th className="px-5 py-4 font-medium">Action</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {invoices.map((invoice) => (
              <tr key={`${invoice.invoice_number}-${invoice.processed_at}`}>
                <td className="px-5 py-4 text-slate-100">
                  {invoice.vendor_name || "-"}
                </td>
                <td className="px-5 py-4 text-slate-300">
                  {invoice.invoice_number || "-"}
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
                  {formatDate(invoice.invoice_date)}
                </td>
                {showActions && (
                  <td className="px-5 py-4">
                    <button
                      className="rounded-lg border border-indigo-500/40 px-3 py-2 text-xs font-semibold text-indigo-200 transition hover:border-indigo-500 hover:bg-indigo-500/20"
                      onClick={() => onDownload?.(invoice)}
                      type="button"
                    >
                      Download
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
