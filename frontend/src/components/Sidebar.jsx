export default function Sidebar() {
  return (
    <section className="border-b border-white/10 bg-slate-900/40">
      <div className="page-wrap grid gap-4 py-3 text-xs font-medium text-slate-400 sm:flex sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <div className="h-1.5 w-1.5 rounded-full bg-teal-400 animate-pulse"></div>
          Precision OCR tuned for Indian GST formats.
        </div>
        <div className="hidden sm:flex items-center gap-2">
          <div className="h-1 w-1 rounded-full bg-slate-600"></div>
          Human-in-the-loop review
        </div>
        <div className="hidden md:flex items-center gap-2">
          <div className="h-1 w-1 rounded-full bg-slate-600"></div>
          ERP-ready CSV exports
        </div>
      </div>
    </section>
  );
}
