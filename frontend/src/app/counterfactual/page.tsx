"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sliders, Sparkles, TrendingUp, Check, ArrowRight, Zap, CheckCircle2 } from "lucide-react";
import { MathBlock } from "@/components/MathBlock";

interface ToggleSkill {
  id: string;
  name: string;
  category: string;
  marginalGain: number; // in %
  learningWeeks: number;
  difficulty: string;
  enabled: boolean;
}

const INITIAL_SKILLS: ToggleSkill[] = [
  { id: "docker", name: "Docker & Containerization", category: "DevOps", marginalGain: 9.5, learningWeeks: 3, difficulty: "Intermediate", enabled: false },
  { id: "pytorch", name: "PyTorch & Deep Neural Nets", category: "Deep Learning", marginalGain: 13.0, learningWeeks: 5, difficulty: "Advanced", enabled: false },
  { id: "rag", name: "RAG & Vector Database Systems", category: "GenAI", marginalGain: 14.5, learningWeeks: 4, difficulty: "Expert", enabled: false },
  { id: "mlops", name: "MLOps & CI/CD Pipeline Automation", category: "DevOps", marginalGain: 7.0, learningWeeks: 4, difficulty: "Advanced", enabled: false },
  { id: "fastapi", name: "FastAPI Production Backend Serving", category: "Backend", marginalGain: 6.0, learningWeeks: 3, difficulty: "Intermediate", enabled: false },
  { id: "kubernetes", name: "Kubernetes Orchestration", category: "Cloud", marginalGain: 8.0, learningWeeks: 5, difficulty: "Expert", enabled: false }
];

export default function CounterfactualPage() {
  const [baseScore, setBaseScore] = useState(74.0);
  const [skills, setSkills] = useState<ToggleSkill[]>(INITIAL_SKILLS);

  const toggleSkill = (id: string) => {
    setSkills(
      skills.map((s) => (s.id === id ? { ...s, enabled: !s.enabled } : s))
    );
  };

  const enabledSkills = skills.filter((s) => s.enabled);
  // Diminishing returns formula for multiple simultaneous skills
  const rawTotalGain = enabledSkills.reduce((acc, s) => acc + s.marginalGain, 0);
  const synergyDiscount = enabledSkills.length > 1 ? (enabledSkills.length - 1) * 1.5 : 0;
  const netGain = Math.max(0, rawTotalGain - synergyDiscount);
  const newScore = Math.min(100.0, Number((baseScore + netGain).toFixed(1)));
  const totalWeeks = enabledSkills.reduce((acc, s) => acc + s.learningWeeks, 0);

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Sliders className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 5 — Counterfactual AI Engine
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Counterfactual "What-If" Employability Simulator
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Instant perturbation of candidate feature vector (X ➔ X&apos;) to calculate marginal gain ΔScore = f(X&apos;) - f(X).
          </p>
        </div>

        <span className="rounded bg-[#10B981]/15 px-3 py-1 font-mono text-xs font-bold text-[#10B981] border border-[#10B981]/30">
          ΔScore Engine Active
        </span>
      </div>

      {/* Main Score Delta Showcase */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Interactive Intervention Toggles */}
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between border-b border-[#222228] pb-3">
            <div>
              <h3 className="font-mono text-sm font-bold text-white">
                Hypothetical Skill Interventions
              </h3>
              <p className="text-[11px] text-[#A1A1AA]">
                Toggle skills on/off to observe real-time score recomputation.
              </p>
            </div>
            <button
              onClick={() => setSkills(INITIAL_SKILLS)}
              className="text-[11px] font-mono text-[#A1A1AA] hover:text-white"
            >
              Reset All
            </button>
          </div>

          {/* Skill Toggles List */}
          <div className="space-y-2.5">
            {skills.map((skill) => {
              return (
                <div
                  key={skill.id}
                  onClick={() => toggleSkill(skill.id)}
                  className={`flex cursor-pointer items-center justify-between rounded-lg border p-3.5 transition-all ${
                    skill.enabled
                      ? "border-[#10B981] bg-[#10B981]/10 text-white shadow-md shadow-[#10B981]/5"
                      : "border-[#27272A] bg-[#0A0A0C] text-[#A1A1AA] hover:border-[#71717A] hover:text-white"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-5 w-5 items-center justify-center rounded border transition-colors ${
                        skill.enabled
                          ? "border-[#10B981] bg-[#10B981] text-black font-bold"
                          : "border-[#3F3F46] bg-[#18181D]"
                      }`}
                    >
                      {skill.enabled && <Check className="h-3.5 w-3.5 stroke-[3]" />}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-bold text-white">{skill.name}</span>
                        <span className="rounded bg-[#27272A] px-1.5 py-0.2 font-mono text-[9px] text-[#71717A]">
                          {skill.category}
                        </span>
                      </div>
                      <span className="text-[11px] text-[#71717A]">
                        {skill.learningWeeks} Weeks · {skill.difficulty}
                      </span>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="font-mono text-xs font-bold text-[#10B981]">
                      +{skill.marginalGain}%
                    </span>
                    <div className="font-mono text-[9px] text-[#71717A]">Marginal Delta</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Real-Time Score Delta Box */}
        <div className="flex flex-col justify-between rounded-xl border border-[#222228] bg-[#111115] p-6 lg:col-span-5 shadow-2xl">
          <div className="space-y-6">
            <div className="border-b border-[#222228] pb-3">
              <span className="font-mono text-[10px] uppercase text-[#71717A]">Simulation Output</span>
              <h3 className="text-xl font-bold text-white mt-0.5">Counterfactual Score State</h3>
            </div>

            {/* Score Comparison Display */}
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg border border-[#27272A] bg-[#0A0A0C] p-4 text-center">
                <span className="font-mono text-[10px] text-[#71717A] uppercase">Current Score f(X)</span>
                <div className="mt-1 font-mono text-3xl font-black text-white">{baseScore.toFixed(1)}%</div>
                <span className="text-[11px] text-[#A1A1AA]">Baseline Candidate</span>
              </div>

              <div className="rounded-lg border border-[#10B981]/40 bg-[#10B981]/10 p-4 text-center">
                <span className="font-mono text-[10px] text-[#10B981] uppercase font-bold">New Score f(X')</span>
                <motion.div
                  key={newScore}
                  initial={{ scale: 0.8 }}
                  animate={{ scale: 1 }}
                  className="mt-1 font-mono text-3xl font-black text-[#10B981]"
                >
                  {newScore.toFixed(1)}%
                </motion.div>
                <span className="text-[11px] text-[#10B981] font-semibold">
                  +{netGain.toFixed(1)}% Total Gain
                </span>
              </div>
            </div>

            {/* Visual Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-[#A1A1AA]">Qualification Threshold: 85.0%</span>
                <span className={newScore >= 85 ? "text-[#10B981] font-bold" : "text-white"}>
                  {newScore >= 85 ? "QUALIFIED" : "IN PROGRESS"}
                </span>
              </div>
              <div className="h-3 w-full rounded-full bg-[#0A0A0C] border border-[#27272A] overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-white via-[#10B981] to-[#10B981]"
                  initial={{ width: `${baseScore}%` }}
                  animate={{ width: `${newScore}%` }}
                  transition={{ duration: 0.5, ease: "easeOut" }}
                />
              </div>
            </div>

            {/* Summary Insights */}
            <div className="rounded-md border border-[#27272A] bg-[#0A0A0C] p-3 text-xs text-[#A1A1AA]">
              {enabledSkills.length === 0 ? (
                <>Select hypothetical skills to recompute employability delta.</>
              ) : (
                <>
                  Acquiring <strong>{enabledSkills.map((s) => s.name.split(" ")[0]).join(", ")}</strong> elevates candidate from <strong>{baseScore}%</strong> to <strong>{newScore}%</strong> (+{netGain.toFixed(1)}% total improvement) in approximately <strong>{totalWeeks} weeks</strong>.
                </>
              )}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#222228]">
            <span className="font-mono text-[10px] text-[#10B981] font-semibold">
              Optimal Bundle Recommendation: Docker + PyTorch (+21.0% Gain)
            </span>
          </div>
        </div>
      </div>

      {/* Mathematical Formulation */}
      <MathBlock
        name="Counterfactual AI Delta Scoring Formula"
        formula="\Delta \text{Score}(s_k) = f(\mathbf{x} \cup \{s_k\}) - f(\mathbf{x}), \quad \mathbf{x}^* = \arg\min_{\mathbf{x}'} \left[ \text{dist}(\mathbf{x}, \mathbf{x}') + \lambda \max(0, \gamma - f(\mathbf{x}'))^2 \right]"
        explanation="Solves the inverse optimization problem: finding the minimal sparse modification to a candidate's skill vector to guarantee crossing target qualification threshold γ."
      />
    </div>
  );
}
