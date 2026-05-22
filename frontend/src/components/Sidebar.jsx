import { NavLink } from "react-router-dom";
import { LayoutDashboard, FileUp } from "lucide-react";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/upload", label: "Upload", icon: FileUp },
];

export default function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-800/60 bg-slate-950/60 px-6 py-8 backdrop-blur lg:flex">
      <div className="mb-10">
        <div className="text-xl font-semibold text-slate-100">GST Journal</div>
        <div className="text-sm text-slate-400">Invoice to Entry</div>
      </div>
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all ${
                  isActive
                    ? "bg-indigo-500/20 text-indigo-200 shadow-lg shadow-indigo-500/10"
                    : "text-slate-300 hover:bg-slate-800/60 hover:text-slate-100"
                }`
              }
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
      <div className="mt-auto rounded-2xl border border-slate-800/70 bg-slate-900/70 p-4 text-xs text-slate-400">
        Powered by OCR + LLM extraction with GST validation.
      </div>
    </aside>
  );
}
