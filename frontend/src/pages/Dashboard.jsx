import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, FileSpreadsheet, Sparkles, BadgeCheck } from "lucide-react";
import ParticleBackground from "../components/ParticleBackground.jsx";
import FeatureCard from "../components/FeatureCard.jsx";

const features = [
  {
    title: "AI Extraction",
    description: "Gemini reads any invoice format with human-grade accuracy.",
    icon: <Sparkles className="h-5 w-5" />,
  },
  {
    title: "Instant CSV",
    description: "Journal entry files generated in seconds, ready for ERP import.",
    icon: <FileSpreadsheet className="h-5 w-5" />,
  },
  {
    title: "GST Compliant",
    description: "CGST, SGST, IGST, and HSN breakdowns validated automatically.",
    icon: <BadgeCheck className="h-5 w-5" />,
  },
];

export default function Dashboard() {
  return (
    <div className="space-y-20 pb-20">
      <section className="relative min-h-[70vh] overflow-hidden rounded-[2.8rem] border border-white/5">
        <ParticleBackground />
        <div className="absolute inset-0 hero-gradient" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-950/30 to-slate-950" />
        <div className="relative z-10 flex h-full flex-col justify-center px-8 py-16 md:px-14 md:py-20 lg:px-20">
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-400/30 bg-indigo-500/10 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-indigo-200">
            <span className="h-2 w-2 rounded-full bg-indigo-400 animate-pulse" />
            YC-grade finance automation
          </div>
          <div className="mt-8 max-w-3xl">
            <h1 className="brand-heading text-4xl font-semibold leading-tight text-white sm:text-5xl lg:text-6xl">
              Transform Invoices Into Journal Entries Instantly
            </h1>
            <p className="mt-5 text-lg text-slate-300">
              AI-powered GST invoice extraction for Royal Sundaram. Build journal-ready CSVs,
              verified for compliance, in seconds.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
              <Link
                to="/upload"
                className="glow-button pulse-glow inline-flex items-center justify-center gap-2 rounded-full bg-indigo-500 px-7 py-4 text-sm font-semibold text-white shadow-[0_0_32px_rgba(99,102,241,0.45)] transition-all hover:-translate-y-0.5"
              >
                Process Invoice →
                <ArrowRight className="h-4 w-4" />
              </Link>
              <div className="rounded-full border border-white/10 bg-slate-900/60 px-5 py-3 text-xs font-semibold uppercase tracking-widest text-slate-300">
                ₹2,71,28,45.83 processed this quarter
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {features.map((feature, index) => (
          <FeatureCard key={feature.title} {...feature} delay={index * 0.1} />
        ))}
      </section>

      <motion.section
        className="glass-card rounded-[2.5rem] border border-white/5 px-8 py-12 md:px-14"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <div className="grid gap-8 md:grid-cols-3">
          {[
            { label: "Median extraction time", value: "4.2s" },
            { label: "Field level accuracy", value: "98.7%" },
            { label: "Invoices processed", value: "1.2M+" },
          ].map((stat) => (
            <div key={stat.label} className="rounded-2xl border border-white/5 bg-slate-950/40 px-5 py-4">
              <div className="brand-heading text-2xl font-semibold text-white">{stat.value}</div>
              <div className="mt-2 text-xs font-semibold uppercase tracking-widest text-slate-400">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </motion.section>
    </div>
  );
}
