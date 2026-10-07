"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, ArrowRight, CheckCircle, RefreshCw, Cpu, Layers } from "lucide-react";
import { MathBlock } from "@/components/MathBlock";

interface SkillPair {
  candidateToken: string;
  jobRequirement: string;
  cosineSim: number;
  embeddingDist: number;
  confidence: string;
  status: "Exact Match" | "High Semantic Syn" | "Related Framework" | "Gap";
}

const DEMO_PAIRS: SkillPair[] = [
  { candidateToken: "ML", jobRequirement: "Machine Learning", cosineSim: 0.942, embeddingDist: 0.058, confidence: "94.2%", status: "High Semantic Syn" },
  { candidateToken: "TensorFlow", jobRequirement: "Deep Learning Frameworks", cosineSim: 0.891, embeddingDist: 0.109, confidence: "89.1%", status: "Related Framework" },
  { candidateToken: "Python", jobRequirement: "Python 3.x Scripting", cosineSim: 0.985, embeddingDist: 0.015, confidence: "98.5%", status: "Exact Match" },
  { candidateToken: "FastAPI", jobRequirement: "REST API Microservices", cosineSim: 0.846, embeddingDist: 0.154, confidence: "84.6%", status: "High Semantic Syn" },
  { candidateToken: "SQL", jobRequirement: "Relational Querying & Postgres", cosineSim: 0.912, embeddingDist: 0.088, confidence: "91.2%", status: "High Semantic Syn" },
  { candidateToken: "Pandas", jobRequirement: "Tabular Data Processing", cosineSim: 0.880, embeddingDist: 0.120, confidence: "88.0%", status: "High Semantic Syn" }
];

export default function SemanticMatchingPage() {
  const [pairs, setPairs] = useState(DEMO_PAIRS);
  const [isClustering, setIsClustering] = useState(false);
  const [selectedPair, setSelectedPair] = useState<SkillPair>(DEMO_PAIRS[0]);

  const triggerClusterAnimation = () => {
    setIsClustering(true);
    setTimeout(() => setIsClustering(false), 2400);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 2 — Semantic Skill Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Sentence-BERT (SBERT) & Dense Vector Matcher
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            384-dimensional dense transformer embeddings mapping candidate skills to job specifications via Cosine Similarity.
          </p>
        </div>

        <button
          onClick={triggerClusterAnimation}
          className="flex items-center gap-2 rounded-lg bg-[#10B981] px-4 py-2 text-xs font-bold text-black hover:bg-[#059669] transition-colors"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${isClustering ? "animate-spin" : ""}`} />
          Simulate Vector Clustering
        </button>
      </div>

      {/* Interactive Vector Space Cluster Visualizer */}
      <div className="relative overflow-hidden rounded-xl border border-[#222228] bg-[#111115] p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-[#222228] pb-4 mb-6">
          <div>
            <h3 className="font-mono text-sm font-bold text-white">
              Interactive 2D Vector Projection (t-SNE / PCA Manifold)
            </h3>
            <p className="text-[11px] text-[#A1A1AA]">
              Candidate skill tokens (White) and Job requirements (Green) converge into semantic clusters.
            </p>
          </div>
          <span className="font-mono text-[10px] text-[#10B981] bg-[#10B981]/10 px-2 py-1 rounded border border-[#10B981]/30">
            Model: all-MiniLM-L6-v2
          </span>
        </div>

        {/* Vector Field Animation Box */}
        <div className="relative h-64 w-full rounded-lg border border-[#27272A] bg-[#0A0A0C] p-4 flex items-center justify-around overflow-hidden">
          {/* Background vector grid lines */}
          <div className="absolute inset-0 bg-dot-pattern opacity-30" />

          {/* Left Candidate Cluster */}
          <motion.div
            animate={{
              x: isClustering ? 120 : 0,
              scale: isClustering ? 1.05 : 1
            }}
            transition={{ duration: 1.2, ease: "easeInOut" }}
            className="relative z-10 flex flex-col items-center gap-2"
          >
            <span className="font-mono text-[10px] uppercase font-bold text-[#A1A1AA] bg-[#18181D] px-2 py-0.5 rounded border border-[#27272A]">
              Candidate Tokens X
            </span>
            <div className="flex flex-wrap max-w-xs gap-2 justify-center">
              {pairs.map((p) => (
                <span
                  key={p.candidateToken}
                  onClick={() => setSelectedPair(p)}
                  className={`cursor-pointer rounded border px-2.5 py-1 font-mono text-xs font-semibold transition-all ${
                    selectedPair.candidateToken === p.candidateToken
                      ? "border-white bg-white text-black shadow-md shadow-white/10"
                      : "border-[#27272A] bg-[#111115] text-white hover:border-[#71717A]"
                  }`}
                >
                  {p.candidateToken}
                </span>
              ))}
            </div>
          </motion.div>

          {/* Center Convergence Indicator */}
          <div className="relative z-10 flex flex-col items-center">
            <div className="flex h-10 w-10 items-center justify-center rounded-full border border-[#10B981]/40 bg-[#10B981]/10 font-mono text-xs font-bold text-[#10B981]">
              ≈
            </div>
            <span className="font-mono text-[9px] text-[#71717A] mt-1">Cosine Sim</span>
          </div>

          {/* Right Job Requirement Cluster */}
          <motion.div
            animate={{
              x: isClustering ? -120 : 0,
              scale: isClustering ? 1.05 : 1
            }}
            transition={{ duration: 1.2, ease: "easeInOut" }}
            className="relative z-10 flex flex-col items-center gap-2"
          >
            <span className="font-mono text-[10px] uppercase font-bold text-[#10B981] bg-[#10B981]/10 px-2 py-0.5 rounded border border-[#10B981]/20">
              Job Requirements Y
            </span>
            <div className="flex flex-wrap max-w-xs gap-2 justify-center">
              {pairs.map((p) => (
                <span
                  key={p.jobRequirement}
                  onClick={() => setSelectedPair(p)}
                  className={`cursor-pointer rounded border px-2.5 py-1 font-mono text-xs font-semibold transition-all ${
                    selectedPair.jobRequirement === p.jobRequirement
                      ? "border-[#10B981] bg-[#10B981] text-black shadow-md shadow-[#10B981]/20"
                      : "border-[#10B981]/30 bg-[#10B981]/5 text-[#10B981] hover:border-[#10B981]"
                  }`}
                >
                  {p.jobRequirement}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Selected Pair Deep Metric Breakdown */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <span className="font-mono text-[10px] uppercase text-[#71717A]">Cosine Similarity Score</span>
          <div className="mt-1 font-mono text-3xl font-black text-[#10B981]">
            {selectedPair.cosineSim.toFixed(3)}
          </div>
          <p className="text-[11px] text-[#A1A1AA] mt-1">Normalized angular alignment in 384-d vector space</p>
        </div>

        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <span className="font-mono text-[10px] uppercase text-[#71717A]">Euclidean Embedding Distance</span>
          <div className="mt-1 font-mono text-3xl font-black text-white">
            {selectedPair.embeddingDist.toFixed(3)}
          </div>
          <p className="text-[11px] text-[#A1A1AA] mt-1">L2 Metric Separation Distance</p>
        </div>

        <div className="rounded-xl border border-[#222228] bg-[#111115] p-4">
          <span className="font-mono text-[10px] uppercase text-[#71717A]">Semantic Confidence</span>
          <div className="mt-1 font-mono text-3xl font-black text-[#10B981]">
            {selectedPair.confidence}
          </div>
          <p className="text-[11px] text-[#A1A1AA] mt-1">Resolved synonym equivalence</p>
        </div>
      </div>

      {/* Matched Token Pairs Table */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5">
        <h3 className="font-mono text-sm font-bold text-white mb-3">
          Semantic Equivalence Registry (Live Match Pairs)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#222228] text-[#71717A]">
                <th className="pb-2.5">Candidate Token</th>
                <th className="pb-2.5">Target Requirement</th>
                <th className="pb-2.5">Cosine Similarity</th>
                <th className="pb-2.5">Embedding Distance</th>
                <th className="pb-2.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222228]">
              {pairs.map((p) => (
                <tr
                  key={p.candidateToken}
                  onClick={() => setSelectedPair(p)}
                  className={`cursor-pointer transition-colors hover:bg-[#18181D] ${
                    selectedPair.candidateToken === p.candidateToken ? "bg-[#18181D]" : ""
                  }`}
                >
                  <td className="py-3 font-semibold text-white">{p.candidateToken}</td>
                  <td className="py-3 text-[#E4E4E7]">{p.jobRequirement}</td>
                  <td className="py-3 text-[#10B981] font-bold">{p.cosineSim.toFixed(3)}</td>
                  <td className="py-3 text-[#A1A1AA]">{p.embeddingDist.toFixed(3)}</td>
                  <td className="py-3">
                    <span className="rounded bg-[#10B981]/15 px-2 py-0.5 text-[10px] font-semibold text-[#10B981] border border-[#10B981]/30">
                      {p.status}
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
        name="Sentence-BERT Siamese Cosine Objective"
        formula="\text{Sim}_{\cos}(\mathbf{u}, \mathbf{v}) = \frac{\sum_{i=1}^{384} u_i v_i}{\sqrt{\sum_{i=1}^{384} u_i^2} \sqrt{\sum_{i=1}^{384} v_i^2}}"
        explanation="Sentence-BERT encodes arbitrary strings into fixed 384-dimensional dense vectors using mean-pooling over contextualized transformer tokens, bypassing the O(n^2) cost of cross-encoders."
      />
    </div>
  );
}
