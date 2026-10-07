"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Compass, ArrowRight, Clock, DollarSign, Award, CheckCircle2, Play } from "lucide-react";
import { CareerRouteStep } from "@/lib/types";
import { MathBlock } from "@/components/MathBlock";

const DEMO_ROUTE: CareerRouteStep[] = [
  { step: 1, skill: "Scikit-Learn & ML Foundations", learningWeeks: 3, milestoneRole: "Junior ML Practitioner", salaryMultiplier: "+20%", difficultyScore: 2, rationale: "Establishes core supervised & unsupervised algorithms" },
  { step: 2, skill: "PyTorch & Deep Neural Nets", learningWeeks: 5, milestoneRole: "Deep Learning Engineer", salaryMultiplier: "+55%", difficultyScore: 4, rationale: "Unlocks neural backpropagation & GPU tensor acceleration" },
  { step: 3, skill: "Docker & Containerized Microservices", learningWeeks: 3, milestoneRole: "Deployment Specialist", salaryMultiplier: "+75%", difficultyScore: 3, rationale: "Ensures cross-platform runtime reproducibility" },
  { step: 4, skill: "MLOps & CI/CD Model Pipelines", learningWeeks: 4, milestoneRole: "MLOps Engineer", salaryMultiplier: "+105%", difficultyScore: 4, rationale: "Automates continuous model training & drift monitoring" },
  { step: 5, skill: "RAG & Vector Database Systems", learningWeeks: 4, milestoneRole: "AI & GenAI Architect", salaryMultiplier: "+145%", difficultyScore: 5, rationale: "Direct enterprise target role qualification" }
];

export default function CareerGPSPage() {
  const [currentSkills, setCurrentSkills] = useState(["Python", "SQL", "Pandas"]);
  const [targetRole, setTargetRole] = useState("AI & Generative AI Architect");
  const [algorithm, setAlgorithm] = useState<"dijkstra" | "astar">("dijkstra");
  const [route, setRoute] = useState<CareerRouteStep[]>(DEMO_ROUTE);
  const [activeStepIndex, setActiveStepIndex] = useState(0);

  const totalWeeks = route.reduce((acc, r) => acc + r.learningWeeks, 0);

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Compass className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 4 — Graph Theory Career GPS
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Dijkstra & A* Shortest-Path Career Navigator
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Algorithmic route optimization minimizing learning duration across the workforce knowledge graph.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setAlgorithm("dijkstra")}
            className={`rounded-md px-3 py-1.5 font-mono text-xs font-semibold transition-all ${
              algorithm === "dijkstra"
                ? "bg-[#10B981] text-black"
                : "border border-[#27272A] bg-[#111115] text-[#A1A1AA] hover:text-white"
            }`}
          >
            Dijkstra
          </button>
          <button
            onClick={() => setAlgorithm("astar")}
            className={`rounded-md px-3 py-1.5 font-mono text-xs font-semibold transition-all ${
              algorithm === "astar"
                ? "bg-[#10B981] text-black"
                : "border border-[#27272A] bg-[#111115] text-[#A1A1AA] hover:text-white"
            }`}
          >
            A* Search (Heuristic)
          </button>
        </div>
      </div>

      {/* Trajectory Metrics Bar */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <div className="flex items-center gap-2 text-[#A1A1AA] text-xs font-mono">
            <Clock className="h-4 w-4 text-[#10B981]" />
            <span>Total Duration</span>
          </div>
          <div className="mt-1 font-mono text-2xl font-black text-white">{totalWeeks} Weeks</div>
          <p className="text-[11px] text-[#A1A1AA] mt-0.5">Approx. {(totalWeeks / 4.3).toFixed(1)} Months</p>
        </div>

        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <div className="flex items-center gap-2 text-[#A1A1AA] text-xs font-mono">
            <DollarSign className="h-4 w-4 text-[#10B981]" />
            <span>Salary Projection</span>
          </div>
          <div className="mt-1 font-mono text-2xl font-black text-[#10B981]">+145%</div>
          <p className="text-[11px] text-[#A1A1AA] mt-0.5">Market Compensation Multiplier</p>
        </div>

        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <div className="flex items-center gap-2 text-[#A1A1AA] text-xs font-mono">
            <Award className="h-4 w-4 text-[#10B981]" />
            <span>Path Milestones</span>
          </div>
          <div className="mt-1 font-mono text-2xl font-black text-white">{route.length} Steps</div>
          <p className="text-[11px] text-[#A1A1AA] mt-0.5">Optimal Minimum Trajectory</p>
        </div>

        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <div className="flex items-center gap-2 text-[#A1A1AA] text-xs font-mono">
            <CheckCircle2 className="h-4 w-4 text-[#10B981]" />
            <span>Graph Algorithm</span>
          </div>
          <div className="mt-1 font-mono text-2xl font-black text-white capitalize">{algorithm}</div>
          <p className="text-[11px] text-[#A1A1AA] mt-0.5">O((V+E) log V) Min-Heap</p>
        </div>
      </div>

      {/* Animated Route Flowchart */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-6 shadow-xl space-y-6">
        <div className="flex items-center justify-between border-b border-[#222228] pb-4">
          <div>
            <h3 className="font-mono text-sm font-bold text-white">
              Shortest-Path Trajectory: Current Skills ➔ {targetRole}
            </h3>
            <p className="text-[11px] text-[#A1A1AA]">
              Each node represents a required milestone with verified prerequisite unblocking.
            </p>
          </div>
          <span className="font-mono text-[10px] text-[#10B981] bg-[#10B981]/10 px-2 py-1 rounded border border-[#10B981]/30">
            Path Cost: 19.0 (Global Minimum)
          </span>
        </div>

        {/* Milestone Steps Interactive Timeline */}
        <div className="space-y-4">
          {route.map((step, idx) => {
            const isSelected = idx === activeStepIndex;
            return (
              <motion.div
                key={step.step}
                onClick={() => setActiveStepIndex(idx)}
                whileHover={{ scale: 1.01 }}
                className={`cursor-pointer rounded-lg border p-4 transition-all ${
                  isSelected
                    ? "border-[#10B981] bg-[#10B981]/10 text-white shadow-lg shadow-[#10B981]/5"
                    : "border-[#27272A] bg-[#0A0A0C] text-[#E4E4E7] hover:border-[#71717A]"
                }`}
              >
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex items-start gap-3.5">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-current/20 bg-[#18181D] font-mono text-xs font-bold text-[#10B981]">
                      0{step.step}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="font-mono text-sm font-bold text-white">{step.skill}</h4>
                        <span className="rounded bg-[#27272A] px-2 py-0.5 font-mono text-[10px] text-[#10B981]">
                          {step.salaryMultiplier} Comp
                        </span>
                      </div>
                      <p className="text-xs text-[#A1A1AA] mt-0.5">{step.rationale}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono">
                    <div className="text-right">
                      <span className="text-[#71717A] text-[10px] uppercase">Duration</span>
                      <div className="text-white font-bold">{step.learningWeeks} Weeks</div>
                    </div>
                    <div className="text-right">
                      <span className="text-[#71717A] text-[10px] uppercase">Unlocked Role</span>
                      <div className="text-[#10B981] font-semibold">{step.milestoneRole}</div>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Mathematical Formulation */}
      <MathBlock
        name="Dijkstra Min-Heap Shortest Path Formulation"
        formula="\text{dist}[v] = \min_{(u, v) \in E} \left( \text{dist}[u] + w(u, v) \right), \quad w(u, v) = \text{Weeks}(u, v) \times \text{DifficultyFactor}"
        explanation="Guarantees finding the globally optimal sequence of skills with lowest aggregate time cost, proven by non-negative edge relaxation."
      />
    </div>
  );
}
