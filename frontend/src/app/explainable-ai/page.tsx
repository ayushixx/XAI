"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Eye, ArrowUpRight, ArrowDownRight, Info, Award, HelpCircle } from "lucide-react";
import { DEFAULT_SHAP_CONTRIBUTIONS } from "@/lib/data";
import { MathBlock } from "@/components/MathBlock";

export default function ExplainableAIPage() {
  const [contributions, setContributions] = useState(DEFAULT_SHAP_CONTRIBUTIONS);
  const baseValue = 0.50; // Expected base value E[f(x)]
  const candidateScore = 0.74; // Final score f(x)

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Eye className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 6 — Explainable AI (XAI)
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            SHAP (Shapley Additive Explanations) Feature Attribution
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Game-theoretic decomposition explaining exactly why the candidate scored 74.0% relative to the baseline expectation E[f(x)] = 50.0%.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="rounded bg-[#111115] px-3 py-1.5 font-mono text-xs text-white border border-[#27272A]">
            Base E[f(x)]: 0.50 ➔ f(x): 0.74
          </span>
        </div>
      </div>

      {/* Waterfall & Attribution Visualization */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-6 shadow-xl space-y-6">
        <div className="flex items-center justify-between border-b border-[#222228] pb-4">
          <div>
            <h3 className="font-mono text-sm font-bold text-white">
              Local SHAP Attribution Waterfall Chart
            </h3>
            <p className="text-[11px] text-[#A1A1AA]">
              Green bars increase qualification probability; Red bars decrease probability due to skill/experience deficits.
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="flex items-center gap-1.5 text-[#10B981]">
              <span className="h-2.5 w-2.5 rounded-sm bg-[#10B981]"></span> Positive Impact
            </span>
            <span className="flex items-center gap-1.5 text-red-400">
              <span className="h-2.5 w-2.5 rounded-sm bg-red-500"></span> Negative Deficit
            </span>
          </div>
        </div>

        {/* Custom High-Contrast Waterfall Bars */}
        <div className="space-y-3.5 pt-2">
          {contributions.map((item, idx) => {
            const isPositive = item.shapValue >= 0;
            const barWidth = Math.abs(item.shapValue) * 350; // visual scaling factor

            return (
              <div key={item.feature} className="space-y-1">
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-white font-medium">{item.feature}</span>
                  <span className={isPositive ? "text-[#10B981] font-bold" : "text-red-400 font-bold"}>
                    {isPositive ? `+${(item.shapValue * 100).toFixed(1)}%` : `${(item.shapValue * 100).toFixed(1)}%`}
                  </span>
                </div>

                <div className="flex h-6 w-full items-center rounded bg-[#0A0A0C] border border-[#27272A] px-1 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(100, Math.max(5, barWidth))}%` }}
                    transition={{ duration: 0.8, delay: idx * 0.1 }}
                    className={`h-4 rounded-sm ${
                      isPositive
                        ? "bg-gradient-to-r from-[#059669] to-[#10B981]"
                        : "bg-gradient-to-r from-red-600 to-red-400"
                    }`}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Attributions Table & Decision Rationale */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-8">
          <h3 className="font-mono text-sm font-bold text-white mb-3">
            Individual Feature Contribution Registry
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead>
                <tr className="border-b border-[#222228] text-[#71717A]">
                  <th className="pb-2.5">Feature Dimension</th>
                  <th className="pb-2.5">Raw Value</th>
                  <th className="pb-2.5">SHAP Attribution φ_i</th>
                  <th className="pb-2.5">Net Contribution</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#222228]">
                {contributions.map((c) => (
                  <tr key={c.feature} className="hover:bg-[#18181D]">
                    <td className="py-2.5 font-semibold text-white">{c.feature}</td>
                    <td className="py-2.5 text-[#A1A1AA]">{c.featureValue.toFixed(1)} / 10</td>
                    <td className={`py-2.5 font-bold ${c.shapValue >= 0 ? "text-[#10B981]" : "text-red-400"}`}>
                      {c.shapValue >= 0 ? `+${c.shapValue.toFixed(4)}` : c.shapValue.toFixed(4)}
                    </td>
                    <td className="py-2.5">
                      <span
                        className={`rounded px-2 py-0.5 text-[10px] font-semibold border ${
                          c.shapValue >= 0
                            ? "bg-[#10B981]/15 text-[#10B981] border-[#10B981]/30"
                            : "bg-red-500/15 text-red-400 border-red-500/30"
                        }`}
                      >
                        {c.direction === "positive" ? "Positive Driver" : "Deficit Penalty"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Explainability Summary Card */}
        <div className="flex flex-col justify-between rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-4">
          <div className="space-y-3">
            <span className="font-mono text-[10px] uppercase text-[#71717A]">Decision Summary</span>
            <h4 className="text-base font-bold text-white">Why 74.0% Was Awarded</h4>
            <p className="text-xs leading-relaxed text-[#A1A1AA]">
              The model awards high positive attribution for <strong>AI/ML Competency (+14.2%)</strong> and <strong>Coding (+11.8%)</strong>, but penalizes the candidate by <strong>-7.8%</strong> for missing production containerization (Docker) and <strong>-6.2%</strong> for Big Data deficits.
            </p>
          </div>

          <div className="rounded-md border border-[#10B981]/30 bg-[#10B981]/10 p-3 text-xs text-[#10B981]">
            <strong>Actionable Resolution:</strong> Acquiring Docker eliminates the largest single negative attribution penalty.
          </div>
        </div>
      </div>

      {/* Mathematical Formulation */}
      <MathBlock
        name="Shapley Value Additive Axiomatic Model"
        formula="f(\mathbf{x}) = \phi_0 + \sum_{i=1}^M \phi_i(f, \mathbf{x}), \quad \phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right]"
        explanation="Guarantees unique axiomatic fairness across Efficiency, Symmetry, Dummy, and Additivity axioms, proving exact mathematical contribution for each skill."
      />
    </div>
  );
}
