import { BrowserRouter, Routes, Route, Navigate, NavLink } from "react-router-dom";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Upload from "./pages/Upload.jsx";
import History from "./pages/History.jsx";

const mobileNav = [
  { to: "/", label: "Dashboard" },
  { to: "/upload", label: "Upload" },
  { to: "/history", label: "History" },
];

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="flex-1 px-6 py-8 lg:px-10">
          <div className="mb-6 flex flex-col gap-4 lg:hidden">
            <div>
              <div className="text-lg font-semibold text-slate-100">
                GST Journal
              </div>
              <div className="text-xs text-slate-400">
                Invoice to entry automation
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {mobileNav.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `rounded-full px-4 py-2 text-xs font-semibold transition ${
                      isActive
                        ? "bg-indigo-500/20 text-indigo-200"
                        : "bg-slate-900/70 text-slate-400 hover:text-slate-200"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/history" element={<History />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
