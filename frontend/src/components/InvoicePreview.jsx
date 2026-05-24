import { useEffect, useState } from "react";

const fieldLabelClass = "text-[11px] font-semibold uppercase tracking-widest text-slate-400";
const displayValueClass =
  "mt-2 rounded-xl border border-transparent bg-slate-950/40 px-4 py-2 text-sm text-white transition-all hover:border-indigo-400/40";
const inputClass =
  "mt-2 w-full rounded-xl border border-indigo-500/30 bg-slate-950/70 px-4 py-2 text-sm text-white focus:outline-none";

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

function EditableField({ label, value, type = "text", disabled, onChange }) {
  const [isEditing, setIsEditing] = useState(false);
  const [draft, setDraft] = useState(value ?? "");

  useEffect(() => {
    setDraft(value ?? "");
  }, [value]);

  const commit = () => {
    setIsEditing(false);
    onChange?.(draft);
  };

  return (
    <div>
      <div className={fieldLabelClass}>{label}</div>
      {isEditing ? (
        <input
          className={inputClass}
          value={draft}
          type={type}
          onChange={(event) => setDraft(event.target.value)}
          onBlur={commit}
          onKeyDown={(event) => {
            if (event.key === "Enter") commit();
          }}
          disabled={disabled}
          autoFocus
        />
      ) : (
        <button
          type="button"
          className={displayValueClass}
          onClick={() => !disabled && setIsEditing(true)}
          disabled={disabled}
        >
          {value || "—"}
        </button>
      )}
    </div>
  );
}

export default function InvoicePreview({ invoice, onFieldChange, disabled }) {
  if (!invoice) return null;

  const gstMode = invoice.igst ? "IGST" : "CGST + SGST";

  return (
    <div className="glass-card rounded-[2rem] border border-white/5 p-8">
      <div className="flex flex-col gap-6">
        <div className="rounded-2xl border border-white/5 bg-slate-950/40 px-5 py-4">
          <div className="text-xs font-semibold uppercase tracking-widest text-slate-400">Invoice Header</div>
          <div className="brand-heading mt-3 text-2xl font-semibold text-white">
            {invoice.vendor_name || "Unnamed Vendor"}
          </div>
          <div className="mt-2 text-sm text-slate-400">
            {invoice.invoice_number || "Invoice #"} • {formatDate(invoice.invoice_date)}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-indigo-500/40 bg-indigo-500/15 px-3 py-1 text-xs font-semibold text-indigo-200">
            {gstMode}
          </span>
          <span className="rounded-full border border-cyan-500/40 bg-cyan-500/15 px-3 py-1 text-xs font-semibold text-cyan-200">
            GST {invoice.gst_rate ?? 0}%
          </span>
          <span className="rounded-full border border-slate-600/60 bg-slate-800/40 px-3 py-1 text-xs font-semibold text-slate-300">
            HSN {invoice.hsn_code || "-"}
          </span>
        </div>

        <div className="grid gap-5 md:grid-cols-2">
          <EditableField
            label="Vendor Name"
            value={invoice.vendor_name}
            disabled={disabled}
            onChange={(value) => onFieldChange("vendor_name", value)}
          />
          <EditableField
            label="Vendor GST"
            value={invoice.vendor_gst}
            disabled={disabled}
            onChange={(value) => onFieldChange("vendor_gst", value)}
          />
          <EditableField
            label="Billing Period"
            value={invoice.billing_period}
            disabled={disabled}
            onChange={(value) => onFieldChange("billing_period", value)}
          />
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          <EditableField
            label="Invoice Number"
            value={invoice.invoice_number}
            disabled={disabled}
            onChange={(value) => onFieldChange("invoice_number", value)}
          />
          <EditableField
            label="Invoice Date"
            value={(invoice.invoice_date || "").slice(0, 10)}
            type="date"
            disabled={disabled}
            onChange={(value) => onFieldChange("invoice_date", value)}
          />
          <EditableField
            label="Taxable Amount"
            value={String(invoice.taxable_amount ?? 0)}
            type="number"
            disabled={disabled}
            onChange={(value) => onFieldChange("taxable_amount", value)}
          />
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          <EditableField
            label="CGST"
            value={String(invoice.cgst ?? 0)}
            type="number"
            disabled={disabled}
            onChange={(value) => onFieldChange("cgst", value)}
          />
          <EditableField
            label="SGST"
            value={String(invoice.sgst ?? 0)}
            type="number"
            disabled={disabled}
            onChange={(value) => onFieldChange("sgst", value)}
          />
          <EditableField
            label="IGST"
            value={String(invoice.igst ?? 0)}
            type="number"
            disabled={disabled}
            onChange={(value) => onFieldChange("igst", value)}
          />
        </div>
      </div>
    </div>
  );
}
