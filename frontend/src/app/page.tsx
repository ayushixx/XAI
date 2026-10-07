"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Sparkles,
  ArrowRight,
  Sliders,
  Compass,
  Eye,
  LineChart,
  LayoutDashboard,
  Bot,
  Terminal,
  ShieldCheck,
  CheckCircle2,
  Lock,
  Layers,
  Zap,
  TrendingUp,
  Brain
} from "lucide-react";
import { AlgorithmJourney } from "@/components/AlgorithmJourney";

export default function LandingPage() {
  const coreFeatures = [
    {
      title: "1. Semantic Skill Intelligence",
      tag: "Sentence-BERT",
      description: "Maps skills to 384-d dense vector representations using all-MiniLM-L6-v2, computing exact cosine similarities across synonyms and abbreviations.",
      href: "/semantic-matching",
      icon: Sparkles,
      stat: "384-D Embeddings"
    },
    {
      title: "2. Explainable AI (SHAP)",
      tag: "Game Theory",
      description: "Interprets gradient boosted tree predictions through Shapley Additive Explanations, delivering exact local and global feature attribution waterfall charts.",
      href: "/explainable-ai",
      icon: Eye,
      stat: "Zero-Error Attributions"
    },
    {
      title: "3. Counterfactual Intelligence",
      tag: "What-If Simulator",
      description: "Perturbs candidate feature vectors to calculate marginal employability score deltas ΔScore = f(X') - f(X) and synthesize optimal minimal bundles.",
      href: "/counterfactual",
      icon: Sliders,
      stat: "Instant ΔScore Engine"
    },
    {
      title: "4. Career GPS Navigation",
      tag: "Graph Theory",
      description: "Dijkstra and A* shortest-path graph optimization over weighted skill prerequisite edges to chart minimum-time milestone trajectories.",
      href: "/career-gps",
      icon: Compass,
      stat: "Shortest Path (Weeks)"
    },
    {
      title: "5. Workforce Readiness (WRI)",
      tag: "OCEAN Psychology",
      description: "Quantitative Big Five behavioral modeling weighting Conscientiousness, Openness, Extraversion, Agreeableness, and Neuroticism.",
      href: "/dashboard",
      icon: LayoutDashboard,
      stat: "Normalized [0-100]"
    },
    {
      title: "6. Future Demand Forecasting",
      tag: "XGBoost vs LightGBM",
      description: "Predicts 1-year, 2-year, and 5-year macro skill posting volumes with CAGR growth dynamics benchmarked on international labor data.",
      href: "/future-demand",
      icon: LineChart,
      stat: "R² = 0.6928"
    }
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-2xl border border-[var(--border-main)] bg-[var(--bg-card)] p-8 sm:p-14 shadow-sm">
        {/* Ambient subtle green glow */}
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 rounded-full bg-[#00C26E]/5 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          {/* Top Badge */}
          <div className="inline-flex items-center gap-2 rounded-full border border-[#00C26E]/30 bg-[#00C26E]/10 px-3.5 py-1 text-[#00C26E]">
            <span className="h-2 w-2 rounded-full bg-[#00C26E] animate-pulse"></span>
            <span className="font-mono text-xs font-semibold tracking-wider">
              ENTERPRISE WORKFORCE INTELLIGENCE PLATFORM
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl font-extrabold tracking-tight text-[var(--text-main)] sm:text-6xl sm:leading-[1.1]">
            Predict. Explain. <br />
            <span className="text-[#00C26E]">
              Optimize. Upskill.
            </span>
          </h1>

          <p className="text-base leading-relaxed text-[var(--text-muted)] max-w-2xl">
            A mathematically grounded decision support system combining <strong>Sentence-BERT</strong>, 
            <strong> Knowledge Graph Theory</strong>, <strong>XGBoost Regressors</strong>, 
            <strong> Counterfactual Optimization</strong>, and <strong>SHAP Game-Theoretic Explainability</strong> with a strict zero-hallucination policy.
          </p>

          {/* Hero CTAs */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              href="/dashboard"
              className="flex items-center gap-2 rounded-lg bg-[#00C26E] px-6 py-3 text-sm font-semibold text-black hover:bg-[#00E887] active:scale-95 shadow-sm transition-all"
            >
              <LayoutDashboard className="h-4 w-4" />
              Launch Intelligence Dashboard
            </Link>

            <Link
              href="/login"
              className="flex items-center gap-2 rounded-lg border border-[var(--border-main)] bg-[var(--bg-surface)] px-5 py-3 text-sm font-semibold text-[var(--text-main)] hover:border-[#00C26E] hover:text-[#00C26E] transition-all"
            >
              <Lock className="h-4 w-4" />
              Sign In / Demo Login
            </Link>

            <Link
              href="/algorithm-lab"
              className="flex items-center gap-2 rounded-lg border border-[var(--border-main)] bg-transparent px-5 py-3 text-sm font-semibold text-[var(--text-muted)] hover:text-[var(--text-main)] transition-all"
            >
              <Terminal className="h-4 w-4" />
              Algorithm Lab
            </Link>
          </div>
        </div>

        {/* Live Metrics Row */}
        <div className="relative z-10 mt-12 grid grid-cols-2 gap-4 sm:grid-cols-4 border-t border-[var(--border-main)] pt-8">
          <div className="rounded-xl border border-[var(--border-main)] bg-[var(--bg-surface)] p-4">
            <div className="font-mono text-2xl font-black text-[var(--text-main)]">384-D</div>
            <div className="font-mono text-[11px] text-[var(--text-muted)] mt-1">SBERT Embeddings</div>
          </div>
          <div className="rounded-xl border border-[var(--border-main)] bg-[var(--bg-surface)] p-4">
            <div className="font-mono text-2xl font-black text-[#00C26E]">0.6928</div>
            <div className="font-mono text-[11px] text-[var(--text-muted)] mt-1">XGBoost Forecast R²</div>
          </div>
          <div className="rounded-xl border border-[var(--border-main)] bg-[var(--bg-surface)] p-4">
            <div className="font-mono text-2xl font-black text-[var(--text-main)]">O(E log V)</div>
            <div className="font-mono text-[11px] text-[var(--text-muted)] mt-1">Dijkstra Shortest Path</div>
          </div>
          <div className="rounded-xl border border-[var(--border-main)] bg-[var(--bg-surface)] p-4">
            <div className="font-mono text-2xl font-black text-[#00C26E]">100%</div>
            <div className="font-mono text-[11px] text-[var(--text-muted)] mt-1">Deterministic Grounding</div>
          </div>
        </div>
      </section>

      {/* Interactive Candidate Pipeline Animation */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-[var(--text-main)]">End-to-End Intelligence Pipeline</h2>
            <p className="text-xs text-[var(--text-muted)]">
              Candidate Vector ➔ SBERT ➔ Knowledge Graph ➔ XGBoost ➔ SHAP ➔ Counterfactual ➔ Dijkstra ➔ LLM Advisor
            </p>
          </div>
        </div>

        <AlgorithmJourney />
      </section>

      {/* 6 Platform Pillar Cards */}
      <section className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-[var(--text-main)]">Core Intelligence Modules</h2>
          <p className="text-xs text-[var(--text-muted)]">
            Select any dedicated module to perform real-time simulations, explainability audits, and career navigation.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {coreFeatures.map((feat) => {
            const Icon = feat.icon;
            return (
              <Link
                key={feat.href}
                href={feat.href}
                className="group flex flex-col justify-between rounded-xl border border-[var(--border-main)] bg-[var(--bg-card)] p-6 transition-all duration-200 hover:border-[#00C26E] hover:shadow-md"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-[var(--border-main)] bg-[var(--bg-surface)] text-[#00C26E] group-hover:border-[#00C26E]/50">
                      <Icon className="h-5 w-5" />
                    </div>
                    <span className="font-mono text-[11px] font-semibold text-[#00C26E] bg-[#00C26E]/10 px-2.5 py-0.5 rounded-full border border-[#00C26E]/20">
                      {feat.tag}
                    </span>
                  </div>

                  <h3 className="mt-4 text-base font-semibold text-[var(--text-main)] group-hover:text-[#00C26E] transition-colors">
                    {feat.title}
                  </h3>
                  <p className="mt-2 text-xs leading-relaxed text-[var(--text-muted)]">
                    {feat.description}
                  </p>
                </div>

                <div className="mt-6 flex items-center justify-between border-t border-[var(--border-main)] pt-3 text-xs">
                  <span className="font-mono text-[11px] text-[var(--text-muted)]">{feat.stat}</span>
                  <span className="flex items-center gap-1 font-mono text-[11px] font-semibold text-[var(--text-main)] group-hover:translate-x-0.5 transition-transform">
                    Explore <ArrowRight className="h-3 w-3 text-[#00C26E]" />
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Zero Hallucination Guarantee Section */}
      <section className="rounded-xl border border-[var(--border-main)] bg-[var(--bg-card)] p-8 shadow-sm">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-[#00C26E]" />
              <span className="font-mono text-xs font-bold uppercase tracking-wider text-[#00C26E]">
                Zero-Hallucination Policy
              </span>
            </div>
            <h3 className="text-xl font-bold text-[var(--text-main)]">
              Why 8BIT is Mathematically Deterministic
            </h3>
            <p className="text-xs leading-relaxed text-[var(--text-muted)]">
              Unlike consumer platforms that let generative LLMs invent arbitrary match scores, 8BIT computes all metrics via 
              <strong> Harmonic Weighted Employability (HWEF)</strong>, <strong>Tree Regressors</strong>, 
              <strong> Dijkstra Graph Relaxation</strong>, and <strong>Shapley Value Games</strong>. The LLM functions purely as an explanatory synthesizer.
            </p>
          </div>

          <Link
            href="/advisor"
            className="shrink-0 flex items-center gap-2 rounded-lg bg-[#00C26E] px-6 py-3 text-sm font-semibold text-black hover:bg-[#00E887] transition-colors"
          >
            <Bot className="h-4 w-4" />
            Test Grounded Advisor
          </Link>
        </div>
      </section>
    </div>
  );
}

