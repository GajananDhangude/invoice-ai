export default function StatsCard({ title, value, icon: Icon, loading }) {
  return (
    <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-5 shadow-lg shadow-slate-900/20">
      <div className="flex items-start justify-between">
        <div>
          <div className="text-xs uppercase tracking-wide text-slate-400">
            {title}
          </div>
          <div className="mt-2 text-2xl font-semibold text-slate-100">
            {loading ? "..." : value}
          </div>
        </div>
        <div className="rounded-xl bg-indigo-500/15 p-3 text-indigo-200">
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}
