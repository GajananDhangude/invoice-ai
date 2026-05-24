import { useEffect } from "react";
import { CheckCircle2, X, AlertTriangle } from "lucide-react";

export default function Toast({ message, type = "success", onClose }) {
  useEffect(() => {
    if (!message) return undefined;
    const timer = setTimeout(() => onClose?.(), 3000);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  const isError = type === "error";

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 rounded-2xl border border-white/10 bg-slate-950/90 backdrop-blur-xl px-5 py-4 text-sm text-white shadow-2xl animate-fade-up">
      {isError ? (
        <AlertTriangle size={18} className="text-rose-400" />
      ) : (
        <CheckCircle2 size={18} className="text-emerald-400" />
      )}
      <span className="font-medium tracking-tight">{message}</span>
      <button
        type="button"
        onClick={onClose}
        className="ml-2 rounded-full lg:p-1 text-slate-500 transition hover:text-white"
      >
        <X size={16} />
      </button>
    </div>
  );
}
