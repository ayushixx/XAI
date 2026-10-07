"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText,
  Sparkles,
  Network,
  Cpu,
  Eye,
  Sliders,
  Compass,
  Bot,
  ArrowRight,
  CheckCircle2,
  Play,
  RotateCcw
} from "lucide-react";

interface PipelineStage {
  id: string;
  title: string;
  subtitle: string;
  algorithm: string;
  formula: string;
  inputPayload: string;
  outputPayload: string;
  icon: any;
  metric: string;
}

const STAGES: PipelineStage[] = [
  {
    id: "profile",
    title: "1. Candidate Profile Ingestion",
    subtitle: "Raw Profile & Experience Normalization",
    algorithm: "Data Standardization & Tokenization",
    formula: "\\mathbf{x}_{raw} = [\\text{Skills}, \\text{OCEAN Traits}, \\text{Years Exp}]",
    inputPayload: JSON.stringify({ name: "Alex Chen", skills: ["Python", "SQL", "Pandas"], yearsExp: 3.5 }, null, 2),
    outputPayload: JSON.stringify({ tokenizedSkills: 6, normalizedExpRatio: 0.875, traitVector: [8.4, 8.8, 7.2, 7.6, 3.2] }, null, 2),
    icon: FileText,
    metric: "Raw Vector Extracted"
  },
  {
    id: "sbert",
    title: "2. Sentence-BERT Semantic Matching",
    subtitle: "384-dimensional dense semantic projection",
    algorithm: "all-MiniLM-L6-v2 Siamese Transformer",
    formula: "\\text{Sim}_{\\cos}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2}",
    inputPayload: JSON.stringify({ candidate: ["ML", "FastAPI"], requirements: ["Machine Learning", "Python Backend"] }, null, 2),
    outputPayload: JSON.stringify({ cosineSimilarity: 0.942, embeddingDimension: 384, semanticScore: "88.4%" }, null, 2),
    icon: Sparkles,
    metric: "Cosine Sim: 0.942"
  },
  {
    id: "kg",
    title: "3. Knowledge Graph Topology",
    subtitle: "Prerequisite chaining & graph centrality",
    algorithm: "PageRank & Composite Centrality",
    formula: "\\mathbf{PR}(v_i) = \\frac{1-d}{|V|} + d \\sum_{v_j \\in \\mathcal{M}(v_i)} \\frac{\\mathbf{PR}(v_j)}{L(v_j)}",
    inputPayload: JSON.stringify({ currentNodes: ["python", "pandas"], targetRole: "AI Engineer" }, null, 2),
    outputPayload: JSON.stringify({ unblockedNodes: ["scikit-learn", "pytorch"], topAnchor: "Python (PR: 0.142)" }, null, 2),
    icon: Network,
    metric: "Graph Centrality: 0.89"
  },
  {
    id: "xgboost",
    title: "4. XGBoost Baseline Evaluation",
    subtitle: "Second-order gradient boosted decision trees",
    algorithm: "XGBoost Regressor + HWEF Harmonization",
    formula: "\\mathcal{L}^{(t)} \\approx \\sum [g_i f_t + \\frac{1}{2}h_i f_t^2] + \\Omega(f_t)",
    inputPayload: JSON.stringify({ coding: 8.5, aiml: 9.0, stats: 8.0, bigdata: 4.0, dashboard: 6.5 }, null, 2),
    outputPayload: JSON.stringify({ baseScore: "74.0%", successProbability: "86.2%", skillGap: "26.0%" }, null, 2),
    icon: Cpu,
    metric: "Baseline: 74.0%"
  },
  {
    id: "shap",
    title: "5. SHAP Axiomatic Attribution",
    subtitle: "Game-theoretic fair feature attribution",
    algorithm: "TreeExplainer Shapley Values",
    formula: "f(\\mathbf{x}) = \\phi_0 + \\sum_{i=1}^M \\phi_i(f, \\mathbf{x})",
    inputPayload: JSON.stringify({ baselineExpectedVal: 0.50, candidateFeatures: 5 }, null, 2),
    outputPayload: JSON.stringify({ positivePushes: { "AI/ML": "+14.2%", "Coding": "+11.8%" }, negativePushes: { "Missing Docker": "-7.8%" } }, null, 2),
    icon: Eye,
    metric: "+/- Attributions Calculated"
  },
  {
    id: "counterfactual",
    title: "6. Counterfactual Optimization",
    subtitle: "Perturbation delta score & minimal bundle search",
    algorithm: "Counterfactual AI Engine",
    formula: "\\Delta \\text{Score}(s_k) = f(X \\cup \\{s_k\\}) - f(X)",
    inputPayload: JSON.stringify({ testInterventions: ["Docker", "PyTorch", "RAG"] }, null, 2),
    outputPayload: JSON.stringify({ topGain: "RAG (+14.5%)", bestROI: "Docker (ROI: 3.17)", optimalBundle: ["Docker", "PyTorch"] }, null, 2),
    icon: Sliders,
    metric: "Max ΔScore: +14.5%"
  },
  {
    id: "gps",
    title: "7. Career GPS Shortest Path",
    subtitle: "Min-heap weighted distance graph relaxation",
    algorithm: "Dijkstra & A* Path Optimization",
    formula: "\\text{dist}[v] = \\min_{(u,v) \\in E} (\\text{dist}[u] + w(u, v))",
    inputPayload: JSON.stringify({ origin: ["Python", "SQL"], destination: "AI Engineer" }, null, 2),
    outputPayload: JSON.stringify({ sequence: ["Scikit-Learn", "PyTorch", "MLOps"], totalDurationWeeks: 15, compMultiplier: "+130%" }, null, 2),
    icon: Compass,
    metric: "15 Weeks Optimal Route"
  },
  {
    id: "advisor",
    title: "8. Grounded LLM Career Advisor",
    subtitle: "Zero-hallucination narrative generation",
    algorithm: "ChromaDB RAG + Structured Executive Synthesis",
    formula: "P(\\text{Advice} \\mid \\text{ML Results}, D^*_{\\text{WEF}})",
    inputPayload: JSON.stringify({ jobFit: "74.0%", optimalBundle: "Docker + PyTorch", gpsWeeks: 15 }, null, 2),
    outputPayload: JSON.stringify({ strategicRecommendation: "Prioritize Docker in Wks 1-3 for +9.5% gain, unblocking MLOps pipeline.", interviewFocus: "Distributed PyTorch training" }, null, 2),
    icon: Bot,
    metric: "Zero Hallucinations Verified"
  }
];

export function AlgorithmJourney() {
  const [activeStep, setActiveStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying) {
      interval = setInterval(() => {
        setActiveStep((prev) => (prev + 1) % STAGES.length);
      }, 3200);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  const currentStage = STAGES[activeStep];
  const Icon = currentStage.icon;

  return (
    <div className="rounded-xl border border-[#222228] bg-[#0A0A0C] p-6 shadow-2xl">
      {/* Header Controls */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-[#10B981]"></span>
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Live Pipeline Simulation
            </span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            End-to-End Algorithm Journey
          </h2>
          <p className="text-xs text-[#A1A1AA]">
            Watch deterministic ML data transform from raw profile tokens to optimal career decisions.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-1.5 rounded-md bg-[#10B981] px-3.5 py-1.5 text-xs font-semibold text-black transition-colors hover:bg-[#059669]"
          >
            {isPlaying ? (
              <>Pause Stream</>
            ) : (
              <>
                <Play className="h-3.5 w-3.5 fill-black" />
                Play Pipeline
              </>
            )}
          </button>
          <button
            onClick={() => {
              setIsPlaying(false);
              setActiveStep(0);
            }}
            className="rounded-md border border-[#27272A] bg-[#111115] p-1.5 text-[#A1A1AA] hover:text-white"
            title="Reset Pipeline"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Stepper Flow Nodes */}
      <div className="mt-6 grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-8">
        {STAGES.map((stage, idx) => {
          const StageIcon = stage.icon;
          const isCurrent = idx === activeStep;
          const isPassed = idx < activeStep;

          return (
            <button
              key={stage.id}
              onClick={() => {
                setIsPlaying(false);
                setActiveStep(idx);
              }}
              className={`flex flex-col items-center rounded-lg border p-2.5 text-center transition-all ${
                isCurrent
                  ? "border-[#10B981] bg-[#10B981]/10 text-white shadow-md shadow-[#10B981]/10"
                  : isPassed
                  ? "border-[#27272A] bg-[#111115] text-[#E4E4E7]"
                  : "border-[#1F1F23] bg-[#0E0E12] text-[#71717A] opacity-60 hover:opacity-100"
              }`}
            >
              <div className="mb-1 flex h-7 w-7 items-center justify-center rounded-md border border-current/20">
                <StageIcon className={`h-3.5 w-3.5 ${isCurrent ? "text-[#10B981]" : ""}`} />
              </div>
              <span className="line-clamp-1 font-mono text-[10px] font-bold">
                {stage.title.split(". ")[1]}
              </span>
              <span className="font-mono text-[9px] text-[#A1A1AA] mt-0.5">
                {isCurrent ? "ACTIVE" : isPassed ? "DONE" : `STEP ${idx + 1}`}
              </span>
            </button>
          );
        })}
      </div>

      {/* Active Stage Deep-Dive Inspector */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeStep}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.25 }}
          className="mt-6 rounded-lg border border-[#27272A] bg-[#111115] p-5"
        >
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between border-b border-[#222228] pb-4">
            <div className="flex items-start gap-3.5">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-[#10B981]/30 bg-[#10B981]/15 text-[#10B981]">
                <Icon className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-semibold text-[#10B981]">
                    {currentStage.algorithm}
                  </span>
                  <span className="rounded bg-[#27272A] px-2 py-0.5 font-mono text-[10px] text-[#A1A1AA]">
                    Stage {activeStep + 1} of 8
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white mt-0.5">{currentStage.title}</h3>
                <p className="text-xs text-[#A1A1AA]">{currentStage.subtitle}</p>
              </div>
            </div>

            <div className="rounded-md border border-[#10B981]/30 bg-[#10B981]/10 px-3.5 py-2 text-right">
              <span className="font-mono text-[10px] uppercase text-[#A1A1AA]">Stage Output Key Metric</span>
              <div className="font-mono text-base font-bold text-[#10B981]">{currentStage.metric}</div>
            </div>
          </div>

          {/* Math Formula & Payload Breakdown */}
          <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-12">
            {/* Mathematical Equation */}
            <div className="rounded-md border border-[#222228] bg-[#0A0A0C] p-3.5 lg:col-span-4">
              <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-[#71717A]">
                Mathematical Formulation
              </span>
              <div className="mt-2 rounded border border-[#27272A] bg-[#111115] p-3 font-mono text-xs text-[#10B981]">
                {currentStage.formula}
              </div>
              <p className="mt-2 text-[11px] leading-relaxed text-[#A1A1AA]">
                Rigorous mathematical guarantee driving deterministic score calibration.
              </p>
            </div>

            {/* Input Data Stream */}
            <div className="rounded-md border border-[#222228] bg-[#0A0A0C] p-3.5 lg:col-span-4">
              <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-[#71717A]">
                Incoming Vector Payload (X)
              </span>
              <pre className="mt-2 max-h-36 overflow-auto rounded border border-[#27272A] bg-[#111115] p-2.5 font-mono text-[10px] text-[#E4E4E7]">
                {currentStage.inputPayload}
              </pre>
            </div>

            {/* Output Data Stream */}
            <div className="rounded-md border border-[#222228] bg-[#0A0A0C] p-3.5 lg:col-span-4">
              <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-[#10B981]">
                Computed Transformation f(X)
              </span>
              <pre className="mt-2 max-h-36 overflow-auto rounded border border-[#10B981]/30 bg-[#10B981]/5 p-2.5 font-mono text-[10px] text-[#10B981]">
                {currentStage.outputPayload}
              </pre>
            </div>
          </div>

          {/* Progression Actions */}
          <div className="mt-5 flex items-center justify-between border-t border-[#222228] pt-4">
            <button
              disabled={activeStep === 0}
              onClick={() => setActiveStep((prev) => Math.max(0, prev - 1))}
              className="rounded-md border border-[#27272A] px-3 py-1.5 text-xs text-[#A1A1AA] hover:text-white disabled:opacity-40"
            >
              Previous Stage
            </button>

            <span className="font-mono text-xs text-[#71717A]">
              Deterministic Data Pipeline
            </span>

            <button
              disabled={activeStep === STAGES.length - 1}
              onClick={() => setActiveStep((prev) => Math.min(STAGES.length - 1, prev + 1))}
              className="flex items-center gap-1.5 rounded-md bg-white px-3.5 py-1.5 text-xs font-semibold text-black hover:bg-[#E4E4E7] disabled:opacity-40"
            >
              Next Algorithm
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
