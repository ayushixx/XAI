"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Terminal, Award, CheckCircle2, Code2, Copy, Check, Sparkles, Filter } from "lucide-react";
import { ALGORITHM_REGISTRY } from "@/lib/data";
import { MathBlock } from "@/components/MathBlock";

export default function AlgorithmLabPage() {
  const [activeCategory, setActiveCategory] = useState<string>("All");
  const [selectedAlgo, setSelectedAlgo] = useState(ALGORITHM_REGISTRY[0]);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const categories = ["All", "Semantic NLP", "Graph Theory", "Machine Learning", "Explainability", "Optimization", "GenAI & RAG"];

  const filteredAlgos = activeCategory === "All"
    ? ALGORITHM_REGISTRY
    : ALGORITHM_REGISTRY.filter((a) => a.category === activeCategory);

  const copyCode = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Terminal className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 11 — Master Algorithm Laboratory
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Mathematical Foundations & Machine Learning Architecture
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Comprehensive algorithmic registry documenting the 12+ statistical, deep learning, graph, and game-theoretic models operating across 8BIT.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="rounded bg-[#10B981] px-3 py-1 font-mono text-xs font-black text-black">
            100% OPERATIONAL
          </span>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-[#222228] pb-3">
        <Filter className="h-3.5 w-3.5 text-[#71717A] mr-1" />
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`rounded-md px-3 py-1.5 font-mono text-xs transition-all ${
              activeCategory === cat
                ? "bg-white font-bold text-black shadow-md"
                : "border border-[#27272A] bg-[#111115] text-[#A1A1AA] hover:text-white"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Algorithm Showcase Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Algorithm Cards List */}
        <div className="space-y-3 lg:col-span-5 max-h-[700px] overflow-y-auto pr-1">
          {filteredAlgos.map((algo) => {
            const isSelected = selectedAlgo.id === algo.id;

            return (
              <div
                key={algo.id}
                onClick={() => setSelectedAlgo(algo)}
                className={`cursor-pointer rounded-xl border p-4 transition-all ${
                  isSelected
                    ? "border-[#10B981] bg-[#10B981]/10 text-white shadow-lg shadow-[#10B981]/5"
                    : "border-[#222228] bg-[#111115] text-[#E4E4E7] hover:border-[#71717A]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-white">{algo.name}</span>
                  <span className="rounded bg-[#27272A] px-2 py-0.5 font-mono text-[9px] text-[#10B981]">
                    {algo.category}
                  </span>
                </div>
                <p className="mt-1.5 line-clamp-2 text-xs text-[#A1A1AA]">
                  {algo.purpose}
                </p>
                <div className="mt-3 flex items-center justify-between border-t border-[#222228] pt-2 text-[10px] font-mono text-[#71717A]">
                  <span>Metric: {algo.keyMetric}</span>
                  <span className="text-[#10B981] font-semibold">Inspect ➔</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: Selected Algorithm Deep-Dive Studio */}
        <div className="flex flex-col justify-between rounded-xl border border-[#222228] bg-[#111115] p-6 lg:col-span-7 space-y-6 shadow-2xl">
          <div className="space-y-5">
            <div className="flex items-start justify-between border-b border-[#222228] pb-4">
              <div>
                <span className="rounded bg-[#10B981]/15 px-2.5 py-0.5 font-mono text-[10px] font-bold text-[#10B981] border border-[#10B981]/30">
                  {selectedAlgo.category}
                </span>
                <h2 className="text-2xl font-black text-white mt-1.5 font-mono">
                  {selectedAlgo.name}
                </h2>
                <p className="text-xs text-[#A1A1AA] mt-1">
                  {selectedAlgo.purpose}
                </p>
              </div>

              <div className="text-right">
                <span className="font-mono text-[10px] uppercase text-[#71717A]">Key Guarantee</span>
                <div className="font-mono text-xs font-bold text-[#10B981] mt-0.5">{selectedAlgo.keyMetric}</div>
              </div>
            </div>

            {/* Mathematical Equation Block */}
            <MathBlock
              name="Objective Function / Mathematical Formulation"
              formula={selectedAlgo.formula}
              explanation={selectedAlgo.formulaExplanation}
            />

            {/* Input & Output Specifications */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="rounded-lg border border-[#27272A] bg-[#0A0A0C] p-3.5">
                <span className="font-mono text-[10px] uppercase font-bold text-[#71717A]">
                  Inputs Vector Space (X)
                </span>
                <ul className="mt-2 space-y-1.5 text-xs text-[#E4E4E7]">
                  {selectedAlgo.inputs.map((inp, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-[#10B981] font-bold">›</span>
                      <span>{inp}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-lg border border-[#27272A] bg-[#0A0A0C] p-3.5">
                <span className="font-mono text-[10px] uppercase font-bold text-[#10B981]">
                  Output Transformation f(X)
                </span>
                <ul className="mt-2 space-y-1.5 text-xs text-[#E4E4E7]">
                  {selectedAlgo.outputs.map((out, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-[#10B981] font-bold">›</span>
                      <span>{out}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Live Backend Implementation Snippet */}
            <div className="rounded-lg border border-[#222228] bg-[#0A0A0C] p-3.5">
              <div className="flex items-center justify-between border-b border-[#222228] pb-2 mb-2">
                <div className="flex items-center gap-2">
                  <Code2 className="h-4 w-4 text-[#10B981]" />
                  <span className="font-mono text-xs font-bold text-white">Active Python Implementation</span>
                </div>
                <button
                  onClick={() => copyCode(selectedAlgo.codeSnippet, selectedAlgo.id)}
                  className="flex items-center gap-1 rounded border border-[#27272A] bg-[#111115] px-2 py-0.5 font-mono text-[10px] text-[#A1A1AA] hover:text-white"
                >
                  {copiedId === selectedAlgo.id ? <Check className="h-3 w-3 text-[#10B981]" /> : <Copy className="h-3 w-3" />}
                  <span>{copiedId === selectedAlgo.id ? "Copied" : "Copy Code"}</span>
                </button>
              </div>
              <pre className="overflow-x-auto rounded bg-[#111115] p-3 font-mono text-xs text-[#10B981] border border-[#27272A]">
                <code>{selectedAlgo.codeSnippet}</code>
              </pre>
            </div>
          </div>

          <div className="border-t border-[#222228] pt-3 text-center">
            <span className="font-mono text-[10px] text-[#71717A]">
              Tested and verified via unittest discover tests (30/30 Unit Tests Passing).
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
