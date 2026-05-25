const fieldClassName =
  "mt-1 w-full rounded-xl border border-slate-800/80 bg-slate-950/40 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none";

const labelClassName = "text-xs uppercase tracking-wide text-slate-400";

export default function InvoicePreview({ invoice, onFieldChange, disabled }) {
  if (!invoice) return null;

  return (
    <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6 shadow-lg shadow-slate-900/20">
      <div className="mb-6 text-lg font-semibold text-slate-100">
        Extracted Invoice Details
      </div>
      <div className="grid gap-5 md:grid-cols-2">
        <div>
          <div className={labelClassName}>Invoice Number</div>
          <input
            className={fieldClassName}
            value={invoice.invoice_number || ""}
            onChange={(event) => onFieldChange("invoice_number", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>Invoice Date</div>
          <input
            className={fieldClassName}
            type="date"
            value={(invoice.invoice_date || "").slice(0, 10)}
            onChange={(event) => onFieldChange("invoice_date", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>Vendor Name</div>
          <input
            className={fieldClassName}
            value={invoice.vendor_name || ""}
            onChange={(event) => onFieldChange("vendor_name", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>Vendor GST</div>
          <input
            className={fieldClassName}
            value={invoice.vendor_gst || ""}
            onChange={(event) => onFieldChange("vendor_gst", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>Taxable Amount</div>
          <input
            className={fieldClassName}
            type="number"
            value={invoice.taxable_amount ?? 0}
            onChange={(event) => onFieldChange("taxable_amount", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>CGST</div>
          <input
            className={fieldClassName}
            type="number"
            value={invoice.cgst ?? 0}
            onChange={(event) => onFieldChange("cgst", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>SGST</div>
          <input
            className={fieldClassName}
            type="number"
            value={invoice.sgst ?? 0}
            onChange={(event) => onFieldChange("sgst", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>IGST</div>
          <input
            className={fieldClassName}
            type="number"
            value={invoice.igst ?? 0}
            onChange={(event) => onFieldChange("igst", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>GST Rate</div>
          <input
            className={fieldClassName}
            type="number"
            value={invoice.gst_rate ?? 0}
            onChange={(event) => onFieldChange("gst_rate", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>Billing Period</div>
          <input
            className={fieldClassName}
            value={invoice.billing_period || ""}
            onChange={(event) => onFieldChange("billing_period", event.target.value)}
            disabled={disabled}
          />
        </div>
        <div>
          <div className={labelClassName}>HSN Code</div>
          <input
            className={fieldClassName}
            value={invoice.hsn_code || ""}
            onChange={(event) => onFieldChange("hsn_code", event.target.value)}
            disabled={disabled}
          />
        </div>
      </div>
    </div>
  );
}
