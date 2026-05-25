import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="space-y-10">
      <section className="relative overflow-hidden rounded-3xl border border-slate-800/70 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
        <div className="absolute -right-24 -top-20 h-64 w-64 rounded-full bg-indigo-500/20 blur-3xl" />
        <div className="absolute -bottom-20 left-10 h-48 w-48 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="relative z-10 space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-slate-700/60 bg-slate-900/70 px-3 py-1 text-xs uppercase tracking-[0.2em] text-slate-300">
            GST Journal
          </div>
          <div className="max-w-2xl space-y-3">
            <h1 className="text-3xl font-semibold text-slate-100 md:text-4xl">
              Turn GST invoices into journal entries in minutes.
            </h1>
            <p className="text-sm text-slate-400 md:text-base">
              Upload a PDF, review extracted fields, and generate a clean CSV for your
              accounting workflow. OCR plus LLM validation keeps entries consistent and
              audit-ready.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <Link
              to="/upload"
              className="inline-flex items-center justify-center rounded-xl bg-indigo-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:bg-indigo-400"
            >
              Upload Invoice
            </Link>
            <div className="text-xs text-slate-400">
              Preferred format: PDF GST invoice
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.3fr_1fr]">
        <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6">
          <div className="text-lg font-semibold text-slate-100">How it works</div>
          <div className="mt-4 grid gap-4 sm:grid-cols-3">
            {[
              {
                title: "Upload",
                body: "Drop a GST invoice PDF and let the extractor handle the text.",
              },
              {
                title: "Review",
                body: "Validate HSN codes, GST rates, and totals before export.",
              },
              {
                title: "Export",
                body: "Generate a journal-ready CSV in one click.",
              },
            ].map((step, index) => (
              <div
                key={step.title}
                className="rounded-2xl border border-slate-800/70 bg-slate-950/50 p-4"
              >
                <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Step {index + 1}
                </div>
                <div className="mt-2 text-sm font-semibold text-slate-100">
                  {step.title}
                </div>
                <div className="mt-2 text-xs text-slate-400">{step.body}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6">
          <div className="text-lg font-semibold text-slate-100">What you get</div>
          <div className="mt-4 space-y-3 text-sm text-slate-400">
            <div className="rounded-xl border border-slate-800/70 bg-slate-950/50 p-4">
              Structured invoice fields ready for ledger posting.
            </div>
            <div className="rounded-xl border border-slate-800/70 bg-slate-950/50 p-4">
              GST totals and taxable amounts validated for accuracy.
            </div>
            <div className="rounded-xl border border-slate-800/70 bg-slate-950/50 p-4">
              CSV output tailored for journal entry workflows.
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            title: "OCR + LLM extraction",
            body: "Blends document OCR with structured validation for GST fields.",
          },
          {
            title: "Fast turnaround",
            body: "From upload to CSV in a single flow, no extra screens.",
          },
          {
            title: "Audit ready",
            body: "Keep consistent entries with GST totals and invoice metadata.",
          },
        ].map((item) => (
          <div
            key={item.title}
            className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-5"
          >
            <div className="text-sm font-semibold text-slate-100">{item.title}</div>
            <div className="mt-2 text-xs text-slate-400">{item.body}</div>
          </div>
        ))}
      </section>
    </div>
  );
}
