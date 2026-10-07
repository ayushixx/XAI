"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Award, Zap, Clock, ArrowUpRight, BarChart3 } from "lucide-react";
import { COUNTERFACTUAL_SKILLS } from "@/lib/data";
import { MathBlock } from "@/components/MathBlock";

export default function SkillROIPage() {
  const [skills, setSkills] = useState(
    [...COUNTERFACTUAL_SKILLS].sort((a, b) => b.roiIndex - a.roiIndex)
  );

  const topSkill = skills[0];

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 7 — Skill ROI Optimizer
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Learning Return on Investment (ROI) Leaderboard
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Maximizes upskilling efficiency by ranking skills by Employability Score Gain per unit of Learning Time: {"ROI = ΔGain / Weeks"}.
          </p>
        </div>

        <span className="rounded bg-[#10B981]/10 px-3 py-1 font-mono text-xs font-bold text-[#10B981] border border-[#10B981]/30">
          Ranked by Efficiency Index
        </span>
      </div>

      {/* Top ROI Highlight Card */}
      <div className="rounded-xl border border-[#10B981]/40 bg-gradient-to-r from-[#10B981]/15 via-[#111115] to-[#111115] p-6 shadow-xl">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 rounded bg-[#10B981] px-2.5 py-0.5 font-mono text-[10px] font-black text-black">
              <Zap className="h-3 w-3 fill-black" />
              #1 HIGHEST ROI RECOMMENDATION
            </div>
            <h2 className="text-2xl font-bold text-white mt-1">{topSkill.skill}</h2>
            <p className="text-xs text-[#A1A1AA]">
              Delivers maximum score impact (<strong>+{topSkill.marginalGain}%</strong>) with only <strong>{topSkill.learningTimeWeeks} weeks</strong> required duration.
            </p>
          </div>

          <div className="flex items-center gap-6 rounded-lg border border-[#10B981]/30 bg-[#0A0A0C] p-4 font-mono">
            <div className="text-center">
              <span className="text-[10px] uppercase text-[#71717A]">ROI Index</span>
              <div className="text-2xl font-black text-[#10B981]">{topSkill.roiIndex.toFixed(2)}</div>
            </div>
            <div className="h-8 w-px bg-[#27272A]" />
            <div className="text-center">
              <span className="text-[10px] uppercase text-[#71717A]">Score Gain</span>
              <div className="text-2xl font-black text-white">+{topSkill.marginalGain}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* ROI Bar Visualizer & Comparison */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-6 shadow-xl space-y-6">
        <div className="border-b border-[#222228] pb-4">
          <h3 className="font-mono text-sm font-bold text-white">
            Skill ROI Efficiency Spectrum (Gain ÷ Duration)
          </h3>
          <p className="text-[11px] text-[#A1A1AA]">
            Visual comparison of score yield per study week.
          </p>
        </div>

        <div className="space-y-4">
          {skills.map((skill, idx) => {
            const barWidth = (skill.roiIndex / topSkill.roiIndex) * 100;

            return (
              <div key={skill.skill} className="space-y-1">
                <div className="flex justify-between font-mono text-xs">
                  <div className="flex items-center gap-2">
                    <span className="text-[#71717A] font-bold">#{idx + 1}</span>
                    <span className="text-white font-semibold">{skill.skill}</span>
                    <span className="text-[#A1A1AA]">({skill.learningTimeWeeks} wks)</span>
                  </div>
                  <span className="text-[#10B981] font-bold">
                    ROI: {skill.roiIndex.toFixed(2)} pts/wk
                  </span>
                </div>

                <div className="flex h-5 w-full items-center rounded bg-[#0A0A0C] border border-[#27272A] px-1 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${barWidth}%` }}
                    transition={{ duration: 0.8, delay: idx * 0.1 }}
                    className="h-3 rounded-sm bg-gradient-to-r from-white via-[#10B981] to-[#10B981]"
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Full Leaderboard Table */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5">
        <h3 className="font-mono text-sm font-bold text-white mb-3">
          Complete ROI Ranked Registry
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#222228] text-[#71717A]">
                <th className="pb-2.5">Rank</th>
                <th className="pb-2.5">Skill Name</th>
                <th className="pb-2.5">Score Gain (Δf(X))</th>
                <th className="pb-2.5">Learning Time</th>
                <th className="pb-2.5">Calculated ROI Index</th>
                <th className="pb-2.5">Difficulty Tier</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222228]">
              {skills.map((s, idx) => (
                <tr key={s.skill} className="hover:bg-[#18181D]">
                  <td className="py-3 font-bold text-[#10B981]">#{idx + 1}</td>
                  <td className="py-3 font-semibold text-white">{s.skill}</td>
                  <td className="py-3 text-[#10B981]">+{s.marginalGain}%</td>
                  <td className="py-3 text-[#E4E4E7]">{s.learningTimeWeeks} Weeks</td>
                  <td className="py-3 text-white font-bold">{s.roiIndex.toFixed(2)}</td>
                  <td className="py-3">
                    <span className="rounded bg-[#27272A] px-2 py-0.5 text-[10px] text-[#A1A1AA]">
                      {s.difficulty}
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
        name="Skill Return on Investment (ROI) Metric"
        formula="\text{ROI}(s_k) = \frac{\Delta \text{Score}(s_k)}{\text{LearningTimeWeeks}(s_k)} = \frac{f(\mathbf{x} \cup \{s_k\}) - f(\mathbf{x})}{\text{Duration}(s_k)}"
        explanation="Provides candidates and enterprise L&D teams with a deterministic metric to prioritize upskilling interventions based on efficiency rather than raw difficulty."
      />
    </div>
  );
}
