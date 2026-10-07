"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Activity,
  TrendingUp,
  Award,
  Sparkles,
  Info,
  ShieldCheck,
  CheckCircle2,
  Sliders,
  ArrowUpRight,
  UserCheck,
  Compass
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { calculateWRI } from "@/lib/utils";
import { RadarChart } from "@/components/RadarChart";
import { MathBlock } from "@/components/MathBlock";

export default function WorkforceDashboardPage() {
  const { activeProfile, currentRoleType } = useAuth();

  // Local interactive trait adjustment
  const [traits, setTraits] = useState(activeProfile.personalityTraits);

  const wriResult = calculateWRI(
    traits.conscientiousness,
    traits.openness,
    traits.extraversion,
    traits.agreeableness,
    traits.neuroticism
  );

  return (
    <div className="space-y-8 pb-12">
      {/* Top Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#E5E7EB] dark:border-[#262626] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <LayoutDashboard className="h-5 w-5 text-[#00C26E]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#00C26E]">
              ANALYTICS & READINESS
            </span>
          </div>
          <h1 className="text-2xl font-black tracking-tight mt-1 sm:text-3xl">
            Workforce Intelligence Dashboard
          </h1>
          <p className="text-xs text-[#71717A] dark:text-[#8E8E93]">
            Multi-pillar diagnostic evaluating technical competency, Big Five behavioral psychology, and employability trajectory.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] px-4 py-2 text-right shadow-sm">
            <span className="font-mono text-[10px] uppercase text-[#71717A] dark:text-[#8E8E93]">
              Active Profile ({currentRoleType.toUpperCase()})
            </span>
            <div className="font-mono text-xs font-bold text-[#111111] dark:text-[#FFFFFF]">
              {activeProfile.name}
            </div>
          </div>
        </div>
      </div>

      {/* 4 Redesigned Stripe/Linear-Style KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* Card 1: Workforce Readiness Index */}
        <div className="saas-card p-5 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[11px] font-bold uppercase text-[#71717A] dark:text-[#8E8E93]">
                Workforce Readiness
              </span>
              <span className="inline-flex items-center gap-1 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[10px] font-bold text-[#00C26E]">
                <TrendingUp className="h-3 w-3" /> +5.4%
              </span>
            </div>

            <div className="metric-number text-3xl font-black text-[#111111] dark:text-[#FFFFFF]">
              {wriResult.score} <span className="text-sm font-normal text-[#71717A]">/ 100</span>
            </div>

            {/* Mini Progress Bar */}
            <div className="h-1.5 w-full rounded-full bg-[#E5E7EB] dark:bg-[#262626] overflow-hidden">
              <div className="h-full bg-[#00C26E]" style={{ width: `${wriResult.score}%` }} />
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#E5E7EB] dark:border-[#262626] text-[11px] text-[#71717A] dark:text-[#8E8E93]">
            <strong className="text-[#111111] dark:text-[#FFFFFF]">Tier:</strong> {wriResult.tier} based on Big Five behavioral weighting.
          </div>
        </div>

        {/* Card 2: Success Probability */}
        <div className="saas-card p-5 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[11px] font-bold uppercase text-[#71717A] dark:text-[#8E8E93]">
                Success Probability
              </span>
              <span className="inline-flex items-center gap-1 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[10px] font-bold text-[#00C26E]">
                Top 8%
              </span>
            </div>

            <div className="metric-number text-3xl font-black text-[#111111] dark:text-[#FFFFFF]">
              {activeProfile.metrics.successProbability}%
            </div>

            {/* Mini Progress Bar */}
            <div className="h-1.5 w-full rounded-full bg-[#E5E7EB] dark:bg-[#262626] overflow-hidden">
              <div className="h-full bg-[#00C26E]" style={{ width: `${activeProfile.metrics.successProbability}%` }} />
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#E5E7EB] dark:border-[#262626] text-[11px] text-[#71717A] dark:text-[#8E8E93]">
            <strong className="text-[#111111] dark:text-[#FFFFFF]">Classifier:</strong> Logistic + Tree Ensemble hiring calibration.
          </div>
        </div>

        {/* Card 3: Job Fit Score */}
        <div className="saas-card p-5 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[11px] font-bold uppercase text-[#71717A] dark:text-[#8E8E93]">
                Job Fit Score (HWEF)
              </span>
              <span className="inline-flex items-center gap-1 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[10px] font-bold text-[#00C26E]">
                Harmonized
              </span>
            </div>

            <div className="metric-number text-3xl font-black text-[#111111] dark:text-[#FFFFFF]">
              {activeProfile.metrics.jobFitScore}%
            </div>

            {/* Mini Progress Bar */}
            <div className="h-1.5 w-full rounded-full bg-[#E5E7EB] dark:bg-[#262626] overflow-hidden">
              <div className="h-full bg-[#00C26E]" style={{ width: `${activeProfile.metrics.jobFitScore}%` }} />
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#E5E7EB] dark:border-[#262626] text-[11px] text-[#71717A] dark:text-[#8E8E93]">
            <strong className="text-[#111111] dark:text-[#FFFFFF]">Coverage:</strong> Penalizes single-point technical or experience deficits.
          </div>
        </div>

        {/* Card 4: Career Alignment */}
        <div className="saas-card p-5 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[11px] font-bold uppercase text-[#71717A] dark:text-[#8E8E93]">
                Career Alignment
              </span>
              <span className="inline-flex items-center gap-1 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[10px] font-bold text-[#00C26E]">
                Dijkstra Min
              </span>
            </div>

            <div className="metric-number text-3xl font-black text-[#111111] dark:text-[#FFFFFF]">
              {activeProfile.metrics.careerAlignmentScore}%
            </div>

            {/* Mini Progress Bar */}
            <div className="h-1.5 w-full rounded-full bg-[#E5E7EB] dark:bg-[#262626] overflow-hidden">
              <div className="h-full bg-[#00C26E]" style={{ width: `${activeProfile.metrics.careerAlignmentScore}%` }} />
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#E5E7EB] dark:border-[#262626] text-[11px] text-[#71717A] dark:text-[#8E8E93]">
            <strong className="text-[#111111] dark:text-[#FFFFFF]">Target:</strong> Direct topology alignment with {activeProfile.targetRole}.
          </div>
        </div>
      </div>

      {/* Main Analysis Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Interactive Big Five Sliders */}
        <div className="saas-card p-6 lg:col-span-6 space-y-5">
          <div className="flex items-center justify-between border-b border-[#E5E7EB] dark:border-[#262626] pb-3">
            <div>
              <h3 className="font-mono text-sm font-bold">
                Big Five (OCEAN) Trait Calibration
              </h3>
              <p className="text-[11px] text-[#71717A] dark:text-[#8E8E93]">
                Adjust sliders to dynamically recompute Workforce Readiness (WRI).
              </p>
            </div>
            <span className="font-mono text-xs font-bold text-[#00C26E] bg-[#00C26E]/10 px-2.5 py-1 rounded-md border border-[#00C26E]/20">
              WRI: {wriResult.score}
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs font-mono">
                <span>Conscientiousness (Weight: +30%)</span>
                <span className="text-[#00C26E] font-bold">{traits.conscientiousness} / 10</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="10.0"
                step="0.1"
                value={traits.conscientiousness}
                onChange={(e) => setTraits({ ...traits, conscientiousness: parseFloat(e.target.value) })}
                className="mt-1.5 w-full accent-[#00C26E]"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono">
                <span>Openness to Experience (Weight: +25%)</span>
                <span className="text-[#00C26E] font-bold">{traits.openness} / 10</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="10.0"
                step="0.1"
                value={traits.openness}
                onChange={(e) => setTraits({ ...traits, openness: parseFloat(e.target.value) })}
                className="mt-1.5 w-full accent-[#00C26E]"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono">
                <span>Extraversion (Weight: +20%)</span>
                <span className="text-[#00C26E] font-bold">{traits.extraversion} / 10</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="10.0"
                step="0.1"
                value={traits.extraversion}
                onChange={(e) => setTraits({ ...traits, extraversion: parseFloat(e.target.value) })}
                className="mt-1.5 w-full accent-[#00C26E]"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono">
                <span>Agreeableness (Weight: +15%)</span>
                <span className="text-[#00C26E] font-bold">{traits.agreeableness} / 10</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="10.0"
                step="0.1"
                value={traits.agreeableness}
                onChange={(e) => setTraits({ ...traits, agreeableness: parseFloat(e.target.value) })}
                className="mt-1.5 w-full accent-[#00C26E]"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono">
                <span>Neuroticism / Stress Sensitivity (Penalty: -10%)</span>
                <span className="text-[#71717A] dark:text-[#8E8E93] font-bold">{traits.neuroticism} / 10</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="10.0"
                step="0.1"
                value={traits.neuroticism}
                onChange={(e) => setTraits({ ...traits, neuroticism: parseFloat(e.target.value) })}
                className="mt-1.5 w-full accent-[#71717A]"
              />
            </div>
          </div>

          <div className="rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] p-3 text-xs text-[#71717A] dark:text-[#8E8E93]">
            <strong className="text-[#111111] dark:text-[#FFFFFF] font-mono">Readiness Status:</strong> {wriResult.tier} — Candidate profile demonstrates strong perseverance and self-regulation.
          </div>
        </div>

        {/* Right: Radar Chart Visualization */}
        <div className="saas-card p-6 lg:col-span-6 flex flex-col justify-between">
          <div className="border-b border-[#E5E7EB] dark:border-[#262626] pb-3">
            <h3 className="font-mono text-sm font-bold">
              Psychological Trait Radar Geometry
            </h3>
            <p className="text-[11px] text-[#71717A] dark:text-[#8E8E93]">
              Pentagonal personality manifold representation.
            </p>
          </div>

          <div className="py-2">
            <RadarChart
              currentTraits={[
                { trait: "Conscientiousness", value: traits.conscientiousness },
                { trait: "Openness", value: traits.openness },
                { trait: "Extraversion", value: traits.extraversion },
                { trait: "Agreeableness", value: traits.agreeableness },
                { trait: "Stability (10-N)", value: Number((10 - traits.neuroticism).toFixed(1)) }
              ]}
              size={280}
            />
          </div>

          <div className="rounded-lg border border-[#00C26E]/30 bg-[#00C26E]/5 p-3 text-center">
            <span className="font-mono text-xs text-[#00C26E] font-bold">
              WRI = 0.30·C + 0.25·O + 0.20·E + 0.15·A - 0.10·N
            </span>
          </div>
        </div>
      </div>

      {/* Mathematical Formulation Footer */}
      <MathBlock
        name="Workforce Readiness Index (WRI) Objective Function"
        formula="\text{WRI}_{\text{normalized}} = \text{clip}\left( 0.30 \cdot C + 0.25 \cdot O + 0.20 \cdot E + 0.15 \cdot A - 0.10 \cdot N + 10.0, \, 0.0, \, 100.0 \right)"
        explanation="Standardized psychological formulation ensuring positive alignment with Conscientiousness and Openness while penalizing emotional instability (Neuroticism)."
      />
    </div>
  );
}
