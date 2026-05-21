import { useEffect, useMemo, useState } from "react";
import {
  FileText,
  IndianRupee,
  BadgePercent,
  CalendarCheck2,
} from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, Tooltip } from "recharts";
import { getHistory, getStats } from "../api/invoice.js";
import StatsCard from "../components/StatsCard.jsx";
import InvoiceTable from "../components/InvoiceTable.jsx";

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

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const loadStats = async () => {
      try {
        setLoadingStats(true);
        const { data } = await getStats();
        if (mounted) setStats(data);
      } catch (err) {
        if (mounted) setError(err.message || "Failed to load stats.");
      } finally {
        if (mounted) setLoadingStats(false);
      }
    };

    const loadHistory = async () => {
      try {
        setLoadingHistory(true);
        const { data } = await getHistory();
        if (mounted) setHistory(data.invoices || []);
      } catch (err) {
        if (mounted) setError(err.message || "Failed to load history.");
      } finally {
        if (mounted) setLoadingHistory(false);
      }
    };

    loadStats();
    loadHistory();

    return () => {
      mounted = false;
    };
  }, []);

  const recentInvoices = useMemo(
    () => history.slice(-5).reverse(),
    [history]
  );

  const chartData = useMemo(() => {
    const lastSix = history.slice(-6);
    return lastSix.map((item) => ({
      name: item.invoice_number || "Invoice",
      value: item.taxable_amount || item.net_amount || 0,
    }));
  }, [history]);

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-2">
        <div className="text-2xl font-semibold text-slate-100">
          Dashboard Overview
        </div>
        <div className="text-sm text-slate-400">
          Real-time invoice extraction metrics with GST insights.
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatsCard
          title="Total Invoices"
          value={stats?.total_invoices ?? "-"}
          icon={FileText}
          loading={loadingStats}
        />
        <StatsCard
          title="Total Amount"
          value={
            loadingStats
              ? "-"
              : formatCurrency(stats?.total_amount || 0)
          }
          icon={IndianRupee}
          loading={loadingStats}
        />
        <StatsCard
          title="Total GST"
          value={
            loadingStats ? "-" : formatCurrency(stats?.total_gst || 0)
          }
          icon={BadgePercent}
          loading={loadingStats}
        />
        <StatsCard
          title="This Month"
          value={stats?.this_month ?? "-"}
          icon={CalendarCheck2}
          loading={loadingStats}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <div className="text-lg font-semibold text-slate-100">
                Recent Activity
              </div>
              <div className="text-xs text-slate-400">
                Last six invoices by taxable amount.
              </div>
            </div>
            <div className="text-xs text-slate-500">
              Updated {formatDate(new Date().toISOString())}
            </div>
          </div>
          {chartData.length ? (
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ left: 0, right: 0 }}>
                  <defs>
                    <linearGradient id="chartGlow" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6366f1" stopOpacity={0.4} />
                      <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Tooltip
                    contentStyle={{
                      background: "#0f172a",
                      border: "1px solid rgba(148, 163, 184, 0.2)",
                      borderRadius: 12,
                      color: "#e2e8f0",
                    }}
                    formatter={(value) => formatCurrency(value)}
                  />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#6366f1"
                    strokeWidth={2}
                    fill="url(#chartGlow)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="rounded-xl border border-dashed border-slate-800/80 p-6 text-sm text-slate-400">
              No invoice data yet. Upload a GST invoice to start tracking.
            </div>
          )}
        </div>
        <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6">
          <div className="mb-5 text-lg font-semibold text-slate-100">
            Insights
          </div>
          <div className="space-y-4 text-sm text-slate-400">
            <div className="rounded-xl border border-slate-800/70 bg-slate-950/50 p-4">
              Automated GST extraction accuracy is improved by validating HSN codes
              in your uploads.
            </div>
            <div className="rounded-xl border border-slate-800/70 bg-slate-950/50 p-4">
              Track taxable amounts and GST totals to streamline journal entries
              per vendor.
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-lg font-semibold text-slate-100">
              Recent Invoices
            </div>
            <div className="text-xs text-slate-400">
              Last five processed invoices.
            </div>
          </div>
        </div>
        <InvoiceTable
          invoices={recentInvoices}
          loading={loadingHistory}
          emptyMessage="No invoices processed yet. Upload a PDF to get started."
          showActions={false}
        />
      </div>
    </div>
  );
}
