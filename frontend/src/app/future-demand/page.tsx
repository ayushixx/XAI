"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { LineChart, TrendingUp, TrendingDown, Award, Calendar, Layers, BarChart3 } from "lucide-react";
import { FUTURE_DEMAND_DATA } from "@/lib/data";
import { MathBlock } from "@/components/MathBlock";

export default function FutureDemandPage() {
  const [data, setData] = useState(FUTURE_DEMAND_DATA);
  const emergingSkills = data.filter((d) => d.growthCAGR > 0).sort((a, b) => b.growthCAGR - a.growthCAGR);
  const decliningSkills = data.filter((d) => d.growthCAGR <= 0).sort((a, b) => a.growthCAGR - b.growthCAGR);

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <LineChart className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 9 — Future Demand Forecasting
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            XGBoost & LightGBM Market Demand Projections
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Time-series machine learning forecasting emerging hyper-growth vs. declining legacy skills across 2026-2029 horizons.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="rounded bg-[#10B981]/15 px-3 py-1 font-mono text-xs font-bold text-[#10B981] border border-[#10B981]/30">
            XGBoost R² = 0.6928
          </span>
        </div>
      </div>

      {/* Model Benchmark Card */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 shadow-xl">
        <div className="flex items-center justify-between border-b border-[#222228] pb-3 mb-4">
          <h3 className="font-mono text-sm font-bold text-white">
            Model Architecture Benchmark Comparison
          </h3>
          <span className="font-mono text-[10px] text-[#A1A1AA]">
            Trained on Historical Macro Trend Series
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="rounded-lg border border-[#10B981]/40 bg-[#10B981]/10 p-4">
            <div className="flex items-center justify-between">
              <span className="font-mono text-sm font-bold text-white">XGBoost Regressor</span>
              <span className="rounded bg-[#10B981] px-2 py-0.5 font-mono text-[10px] font-black text-black">
                RANK #1 (PRIMARY)
              </span>
            </div>
            <div className="mt-3 grid grid-cols-3 gap-2 font-mono">
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">R² Score</span>
                <div className="text-lg font-bold text-[#10B981]">0.6928</div>
              </div>
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">MAE Error</span>
                <div className="text-lg font-bold text-white">4,930</div>
              </div>
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">RMSE</span>
                <div className="text-lg font-bold text-white">6,960</div>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-[#27272A] bg-[#0A0A0C] p-4 opacity-75">
            <div className="flex items-center justify-between">
              <span className="font-mono text-sm font-bold text-white">LightGBM Regressor</span>
              <span className="rounded bg-[#27272A] px-2 py-0.5 font-mono text-[10px] font-semibold text-[#A1A1AA]">
                RANK #2 (BENCHMARK)
              </span>
            </div>
            <div className="mt-3 grid grid-cols-3 gap-2 font-mono">
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">R² Score</span>
                <div className="text-lg font-bold text-[#A1A1AA]">-0.1507</div>
              </div>
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">MAE Error</span>
                <div className="text-lg font-bold text-white">11,171</div>
              </div>
              <div>
                <span className="text-[10px] text-[#71717A] uppercase">RMSE</span>
                <div className="text-lg font-bold text-white">13,472</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Emerging vs Declining Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Emerging */}
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#222228] pb-3">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-[#10B981]" />
              <h3 className="font-mono text-sm font-bold text-white">
                Top Emerging Skills (+CAGR %)
              </h3>
            </div>
            <span className="font-mono text-[10px] text-[#10B981]">Hyper-Growth</span>
          </div>

          <div className="space-y-3">
            {emergingSkills.slice(0, 5).map((skill) => (
              <div key={skill.skill} className="space-y-1">
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-white font-semibold">{skill.skill}</span>
                  <span className="text-[#10B981] font-bold">+{skill.growthCAGR}% CAGR</span>
                </div>
                <div className="flex h-3 w-full rounded-full bg-[#0A0A0C] border border-[#27272A] overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(100, skill.growthCAGR * 1.5)}%` }}
                    transition={{ duration: 0.8 }}
                    className="h-full bg-gradient-to-r from-[#059669] to-[#10B981]"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Declining */}
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#222228] pb-3">
            <div className="flex items-center gap-2">
              <TrendingDown className="h-4 w-4 text-red-400" />
              <h3 className="font-mono text-sm font-bold text-white">
                Top Declining Legacy Tech (-CAGR %)
              </h3>
            </div>
            <span className="font-mono text-[10px] text-red-400">Legacy Tech</span>
          </div>

          <div className="space-y-3">
            {decliningSkills.map((skill) => (
              <div key={skill.skill} className="space-y-1">
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-white font-semibold">{skill.skill}</span>
                  <span className="text-red-400 font-bold">{skill.growthCAGR}% CAGR</span>
                </div>
                <div className="flex h-3 w-full rounded-full bg-[#0A0A0C] border border-[#27272A] overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(100, Math.abs(skill.growthCAGR) * 2.5)}%` }}
                    transition={{ duration: 0.8 }}
                    className="h-full bg-gradient-to-r from-red-600 to-red-400"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 2024 - 2029 Timeline Table */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5">
        <h3 className="font-mono text-sm font-bold text-white mb-3">
          Comprehensive 5-Year Market Demand Trajectory (Job Postings Volume)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#222228] text-[#71717A]">
                <th className="pb-2.5">Skill Name</th>
                <th className="pb-2.5">Domain</th>
                <th className="pb-2.5">Growth CAGR</th>
                <th className="pb-2.5">2024 Baseline</th>
                <th className="pb-2.5">2026 (2-Yr)</th>
                <th className="pb-2.5">2029 (5-Yr)</th>
                <th className="pb-2.5">Trajectory Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222228]">
              {data.map((row) => (
                <tr key={row.skill} className="hover:bg-[#18181D]">
                  <td className="py-3 font-semibold text-white">{row.skill}</td>
                  <td className="py-3 text-[#A1A1AA]">{row.domain}</td>
                  <td className={`py-3 font-bold ${row.growthCAGR > 0 ? "text-[#10B981]" : "text-red-400"}`}>
                    {row.growthCAGR > 0 ? `+${row.growthCAGR}%` : `${row.growthCAGR}%`}
                  </td>
                  <td className="py-3 text-white">{row.actualDemand2024.toLocaleString()}</td>
                  <td className="py-3 text-white">{row.projectedDemand2026.toLocaleString()}</td>
                  <td className="py-3 text-[#10B981] font-bold">{row.projectedDemand2029.toLocaleString()}</td>
                  <td className="py-3">
                    <span
                      className={`rounded px-2 py-0.5 text-[10px] font-semibold border ${
                        row.status === "Hyper-Growth"
                          ? "bg-[#10B981]/15 text-[#10B981] border-[#10B981]/30"
                          : row.status === "High Growth"
                          ? "bg-blue-500/15 text-blue-400 border-blue-500/30"
                          : "bg-red-500/15 text-red-400 border-red-500/30"
                      }`}
                    >
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mathematical Breakdown */}
      <MathBlock
        name="XGBoost Second-Order Taylor Objective Function"
        formula="\mathcal{L}^{(t)} \approx \sum_{i=1}^n \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \left( \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2 \right)"
        explanation="Optimizes leaf weights w_j using exact first-order gradients g_i and second-order Hessians h_i to ensure accurate time-series trajectory bounds."
      />
    </div>
  );
}
