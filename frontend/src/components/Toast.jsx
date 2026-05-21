import { useEffect } from "react";
import { CheckCircle2, X } from "lucide-react";

export default function Toast({ message, onClose }) {
  useEffect(() => {
    if (!message) return undefined;
    const timer = setTimeout(() => onClose?.(), 3000);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 rounded-2xl border border-emerald-500/40 bg-slate-950/90 px-4 py-3 text-sm text-emerald-200 shadow-lg shadow-emerald-500/20">
      <CheckCircle2 size={18} />
      <span>{message}</span>
      <button
        type="button"
        onClick={onClose}
        className="ml-2 rounded-full p-1 text-emerald-200/70 transition hover:text-emerald-100"
      >
        <X size={14} />
      </button>
    </div>
  );
}
