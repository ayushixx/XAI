"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { BrainCircuit, Sparkles, Sliders, ArrowRight, RefreshCcw } from "lucide-react";
import { RadarChart } from "@/components/RadarChart";
import { MathBlock } from "@/components/MathBlock";
import { calculateWRI } from "@/lib/utils";

export default function DigitalTwinPage() {
  const [currentTraits, setCurrentTraits] = useState({
    conscientiousness: 7.2,
    openness: 7.8,
    extraversion: 6.5,
    agreeableness: 7.0,
    neuroticism: 4.8
  });

  const [adjustments, setAdjustments] = useState({
    deltaConscientiousness: 1.2,
    deltaNeuroticism: -1.4,
    deltaOpenness: 0.6
  });

  const futureTraits = {
    conscientiousness: Math.min(10, Math.max(1, Number((currentTraits.conscientiousness + adjustments.deltaConscientiousness).toFixed(1)))),
    openness: Math.min(10, Math.max(1, Number((currentTraits.openness + adjustments.deltaOpenness).toFixed(1)))),
    extraversion: currentTraits.extraversion,
    agreeableness: currentTraits.agreeableness,
    neuroticism: Math.min(10, Math.max(1, Number((currentTraits.neuroticism + adjustments.deltaNeuroticism).toFixed(1))))
  };

  const currWRI = calculateWRI(currentTraits.conscientiousness, currentTraits.openness, currentTraits.extraversion, currentTraits.agreeableness, currentTraits.neuroticism);
  const futureWRI = calculateWRI(futureTraits.conscientiousness, futureTraits.openness, futureTraits.extraversion, futureTraits.agreeableness, futureTraits.neuroticism);
  const gain = futureWRI.score - currWRI.score;

  // Latent z vector mock projection
  const z1 = (currentTraits.conscientiousness * 0.3 - currentTraits.neuroticism * 0.2).toFixed(3);
  const z2 = (currentTraits.openness * 0.4 + currentTraits.extraversion * 0.1).toFixed(3);
  const z3 = (currentTraits.agreeableness * 0.25).toFixed(3);

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <BrainCircuit className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 8 — Deep Learning Personality Digital Twin
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Psychological Growth Simulation & Latent Autoencoder
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Non-linear neural autoencoder (5 ➔ 16 ➔ 8 ➔ 3) projecting behavioral traits into a compact latent manifold z for digital twin coaching.
          </p>
        </div>

        <span className="rounded bg-[#10B981]/10 px-3 py-1 font-mono text-xs font-bold text-[#10B981] border border-[#10B981]/30">
          Neural Architecture: 5 ➔ 16 ➔ 8 ➔ 3
        </span>
      </div>

      {/* Main Digital Twin Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Interactive Simulation Controls */}
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-6 space-y-5">
          <div className="border-b border-[#222228] pb-3">
            <h3 className="font-mono text-sm font-bold text-white">
              Targeted Behavioral Coaching Interventions
            </h3>
            <p className="text-[11px] text-[#A1A1AA]">
              Simulate the effect of executive coaching, stress resilience training, and leadership cultivation.
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-white">Δ Conscientiousness (Target Focus)</span>
                <span className="text-[#10B981] font-bold">+{adjustments.deltaConscientiousness} pts</span>
              </div>
              <input
                type="range"
                min="-2.0"
                max="2.5"
                step="0.1"
                value={adjustments.deltaConscientiousness}
                onChange={(e) => setAdjustments({ ...adjustments, deltaConscientiousness: parseFloat(e.target.value) })}
                className="mt-1 w-full accent-[#10B981]"
              />
            </div>

            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-white">Δ Neuroticism (Stress Resilience Coaching)</span>
                <span className="text-[#10B981] font-bold">{adjustments.deltaNeuroticism} pts</span>
              </div>
              <input
                type="range"
                min="-3.0"
                max="1.0"
                step="0.1"
                value={adjustments.deltaNeuroticism}
                onChange={(e) => setAdjustments({ ...adjustments, deltaNeuroticism: parseFloat(e.target.value) })}
                className="mt-1 w-full accent-red-400"
              />
            </div>

            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-white">Δ Openness (Innovation & Experimentation)</span>
                <span className="text-[#10B981] font-bold">+{adjustments.deltaOpenness} pts</span>
              </div>
              <input
                type="range"
                min="-1.0"
                max="2.0"
                step="0.1"
                value={adjustments.deltaOpenness}
                onChange={(e) => setAdjustments({ ...adjustments, deltaOpenness: parseFloat(e.target.value) })}
                className="mt-1 w-full accent-[#10B981]"
              />
            </div>
          </div>

          {/* Metric Comparison */}
          <div className="grid grid-cols-2 gap-3 pt-2">
            <div className="rounded-lg border border-[#27272A] bg-[#0A0A0C] p-3 text-center">
              <span className="font-mono text-[10px] text-[#71717A] uppercase">Current State WRI</span>
              <div className="font-mono text-2xl font-black text-white">{currWRI.score}</div>
              <span className="text-[10px] text-[#A1A1AA]">{currWRI.tier}</span>
            </div>

            <div className="rounded-lg border border-[#10B981]/40 bg-[#10B981]/10 p-3 text-center">
              <span className="font-mono text-[10px] text-[#10B981] uppercase font-bold">Future Digital Twin</span>
              <div className="font-mono text-2xl font-black text-[#10B981]">{futureWRI.score}</div>
              <span className="text-[10px] text-[#10B981] font-semibold">+{gain.toFixed(1)} Gain</span>
            </div>
          </div>
        </div>

        {/* Right: Comparative Dual Radar Chart */}
        <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-6 flex flex-col justify-between">
          <div className="border-b border-[#222228] pb-3">
            <h3 className="font-mono text-sm font-bold text-white">
              Current State vs. Future Digital Twin Manifold
            </h3>
            <p className="text-[11px] text-[#A1A1AA]">
              White: Baseline profile · Green Dashed: Simulated Twin trajectory.
            </p>
          </div>

          <div className="py-2">
            <RadarChart
              currentTraits={[
                { trait: "Conscientiousness", value: currentTraits.conscientiousness },
                { trait: "Openness", value: currentTraits.openness },
                { trait: "Extraversion", value: currentTraits.extraversion },
                { trait: "Agreeableness", value: currentTraits.agreeableness },
                { trait: "Stability", value: Number((10 - currentTraits.neuroticism).toFixed(1)) }
              ]}
              futureTraits={[
                { trait: "Conscientiousness", value: futureTraits.conscientiousness },
                { trait: "Openness", value: futureTraits.openness },
                { trait: "Extraversion", value: futureTraits.extraversion },
                { trait: "Agreeableness", value: futureTraits.agreeableness },
                { trait: "Stability", value: Number((10 - futureTraits.neuroticism).toFixed(1)) }
              ]}
              size={290}
            />
          </div>

          <div className="rounded-md border border-[#27272A] bg-[#0A0A0C] p-2.5 text-center font-mono text-xs text-[#A1A1AA]">
            Latent Embedding Coordinates: <span className="text-white">z₁={z1}</span> · <span className="text-white">z₂={z2}</span> · <span className="text-white">z₃={z3}</span>
          </div>
        </div>
      </div>

      {/* Mathematical Breakdown */}
      <MathBlock
        name="Deep Autoencoder Objective Function"
        formula="\mathcal{L}_{AE}(\theta, \phi) = \frac{1}{N} \sum_{i=1}^N \|\mathbf{x}_i - g_\phi(f_\theta(\mathbf{x}_i))\|_2^2 + \lambda \|\Theta\|_2^2, \quad \mathbf{z} = f_\theta(\mathbf{x}) \in \mathbb{R}^3"
        explanation="Trained on standard PyTorch architecture with LeakyReLU activations and bottleneck dimension of 3 to discover intrinsic behavioral representations."
      />
    </div>
  );
}
