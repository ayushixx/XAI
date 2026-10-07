"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  GraduationCap,
  Briefcase,
  Users,
  CheckCircle2,
  Lock,
  Mail,
  Zap,
  Network
} from "lucide-react";
import { useAuth, DEMO_PROFILES } from "@/lib/auth-context";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function LoginPage() {
  const router = useRouter();
  const { loginAs } = useAuth();
  const [tab, setTab] = useState<"login" | "signup">("login");
  const [email, setEmail] = useState("alex.chen@stanford.edu");
  const [password, setPassword] = useState("••••••••••••");
  const [isLoading, setIsLoading] = useState(false);

  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      loginAs("analyst");
      router.push("/dashboard");
    }, 600);
  };

  const handleDemoLogin = (role: "student" | "analyst" | "recruiter") => {
    setIsLoading(true);
    loginAs(role);
    setTimeout(() => {
      router.push("/dashboard");
    }, 400);
  };

  return (
    <div className="flex min-h-screen w-full bg-[#FFFFFF] dark:bg-[#0A0A0A] text-[#111111] dark:text-[#FFFFFF] transition-colors">
      {/* Top right theme toggle */}
      <div className="absolute right-6 top-6 z-50">
        <ThemeToggle />
      </div>

      {/* LEFT PANEL: AI Intelligence Showcase */}
      <div className="relative hidden w-1/2 flex-col justify-between overflow-hidden border-r border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#111111] p-12 lg:flex">
        {/* Subtle grid pattern */}
        <div className="absolute inset-0 bg-subtle-grid opacity-50 pointer-events-none" />

        {/* Top Branding */}
        <div className="relative z-10">
          <Link href="/" className="inline-flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#00C26E] font-mono text-base font-black text-black shadow-md shadow-[#00C26E]/20">
              8B
            </div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xl font-bold tracking-wider">8BIT</span>
              <span className="rounded border border-[#00C26E]/40 bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[10px] font-bold text-[#00C26E]">
                ENTERPRISE
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Animated Intelligence Pipeline Graph */}
        <div className="relative z-10 my-auto space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#00C26E]/40 bg-[#00C26E]/10 px-3 py-1">
            <span className="h-2 w-2 rounded-full bg-[#00C26E] animate-pulse" />
            <span className="font-mono text-xs font-semibold tracking-wide text-[#00C26E]">
              DETERMINISTIC ML WORKFORCE ENGINE
            </span>
          </div>

          <div className="space-y-3">
            <h1 className="text-3xl font-black tracking-tight sm:text-4xl sm:leading-tight">
              AI-Powered <br />
              <span className="text-[#00C26E]">Workforce Intelligence</span>
            </h1>
            <p className="font-mono text-sm font-semibold tracking-wide text-[#71717A] dark:text-[#8E8E93]">
              Predict. Explain. Optimize. Upskill.
            </p>
          </div>

          {/* Animated Flow Nodes */}
          <div className="space-y-2.5 pt-2">
            {[
              { title: "Candidate Profile", desc: "Tokenized Skills & OCEAN Personality Vector" },
              { title: "Semantic Matching", desc: "Sentence-BERT 384-D Dense Cosine Sim" },
              { title: "Knowledge Graph", desc: "Prerequisite DAG & PageRank Anchor Scoring" },
              { title: "Counterfactual AI", desc: "Instant What-If ΔScore Optimization" },
              { title: "Career GPS", desc: "Dijkstra Minimum-Time Upskilling Route" },
              { title: "Workforce Intelligence", desc: "Harmonic Calibrated Decision Support" }
            ].map((node, i) => (
              <motion.div
                key={node.title}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="flex items-center gap-3 rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] p-2.5 shadow-sm"
              >
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-[#00C26E]/15 font-mono text-[10px] font-bold text-[#00C26E]">
                  0{i + 1}
                </div>
                <div className="flex-1">
                  <span className="font-mono text-xs font-bold">{node.title}</span>
                  <span className="block text-[10px] text-[#71717A] dark:text-[#8E8E93]">{node.desc}</span>
                </div>
                <CheckCircle2 className="h-3.5 w-3.5 text-[#00C26E]" />
              </motion.div>
            ))}
          </div>
        </div>

        {/* Bottom Guarantee */}
        <div className="relative z-10 flex items-center justify-between border-t border-[#E5E7EB] dark:border-[#262626] pt-4 text-xs font-mono text-[#71717A] dark:text-[#8E8E93]">
          <span>Zero-Hallucination Policy</span>
          <span className="text-[#00C26E] font-bold">100% Deterministic ML</span>
        </div>
      </div>

      {/* RIGHT PANEL: Premium SaaS Authentication Card */}
      <div className="flex w-full flex-col justify-center px-6 py-12 sm:px-12 lg:w-1/2">
        <div className="mx-auto w-full max-w-md space-y-8">
          {/* Header */}
          <div className="space-y-2">
            <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
              {tab === "login" ? "Welcome back" : "Create an enterprise account"}
            </h2>
            <p className="text-xs text-[#71717A] dark:text-[#8E8E93]">
              Enter your credentials or select a one-click demo role below to explore.
            </p>
          </div>

          {/* Quick 1-Click Demo Profiles Box */}
          <div className="rounded-xl border border-[#00C26E]/30 bg-[#00C26E]/5 dark:bg-[#00C26E]/10 p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 font-mono text-[11px] font-bold text-[#00C26E] uppercase">
                <Zap className="h-3.5 w-3.5 fill-[#00C26E]" />
                1-Click Instant Demo Login
              </span>
              <span className="font-mono text-[10px] text-[#71717A] dark:text-[#8E8E93]">No password needed</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => handleDemoLogin("student")}
                className="flex flex-col items-center rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] p-2.5 text-center transition-all hover:border-[#00C26E] hover:shadow-sm"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#E5E7EB] dark:bg-[#262626] text-[#111111] dark:text-[#FFFFFF] mb-1">
                  <GraduationCap className="h-4 w-4 text-[#00C26E]" />
                </div>
                <span className="font-mono text-[11px] font-bold">Student</span>
                <span className="text-[9px] text-[#71717A] dark:text-[#8E8E93] line-clamp-1">Alex Chen</span>
              </button>

              <button
                type="button"
                onClick={() => handleDemoLogin("analyst")}
                className="flex flex-col items-center rounded-lg border border-[#00C26E] bg-[#FFFFFF] dark:bg-[#141414] p-2.5 text-center shadow-sm shadow-[#00C26E]/10 transition-all hover:bg-[#00C26E]/5"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#00C26E]/15 text-[#00C26E] mb-1 font-bold">
                  <Briefcase className="h-4 w-4 text-[#00C26E]" />
                </div>
                <span className="font-mono text-[11px] font-bold text-[#00C26E]">Data Analyst</span>
                <span className="text-[9px] text-[#71717A] dark:text-[#8E8E93] line-clamp-1">Sarah Miller</span>
              </button>

              <button
                type="button"
                onClick={() => handleDemoLogin("recruiter")}
                className="flex flex-col items-center rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] p-2.5 text-center transition-all hover:border-[#00C26E] hover:shadow-sm"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#E5E7EB] dark:bg-[#262626] text-[#111111] dark:text-[#FFFFFF] mb-1">
                  <Users className="h-4 w-4 text-[#00C26E]" />
                </div>
                <span className="font-mono text-[11px] font-bold">Recruiter</span>
                <span className="text-[9px] text-[#71717A] dark:text-[#8E8E93] line-clamp-1">David Vance</span>
              </button>
            </div>
          </div>

          {/* Tab Switcher */}
          <div className="flex rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#141414] p-1 font-mono text-xs">
            <button
              onClick={() => setTab("login")}
              className={`flex-1 rounded-md py-1.5 font-bold transition-all ${
                tab === "login"
                  ? "bg-[#FFFFFF] dark:bg-[#262626] text-[#111111] dark:text-[#FFFFFF] shadow-sm"
                  : "text-[#71717A] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setTab("signup")}
              className={`flex-1 rounded-md py-1.5 font-bold transition-all ${
                tab === "signup"
                  ? "bg-[#FFFFFF] dark:bg-[#262626] text-[#111111] dark:text-[#FFFFFF] shadow-sm"
                  : "text-[#71717A] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              Create Account
            </button>
          </div>

          {/* Social Google Login Button */}
          <button
            type="button"
            onClick={() => handleDemoLogin("analyst")}
            className="flex w-full items-center justify-center gap-2.5 rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] py-2.5 text-xs font-semibold shadow-sm transition-all hover:bg-[#F7F7F7] dark:hover:bg-[#1A1A1A]"
          >
            <svg className="h-4 w-4" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
            <span>Continue with Google Workspace</span>
          </button>

          <div className="relative flex items-center justify-center">
            <div className="w-full border-t border-[#E5E7EB] dark:border-[#262626]" />
            <span className="absolute bg-[#FFFFFF] dark:bg-[#0A0A0A] px-3 font-mono text-[10px] uppercase text-[#71717A]">
              Or continue with work email
            </span>
          </div>

          {/* Form */}
          <form onSubmit={handleAuthSubmit} className="space-y-4">
            <div>
              <label className="block font-mono text-xs font-semibold">Work Email</label>
              <div className="relative mt-1.5 flex items-center">
                <Mail className="absolute left-3 h-4 w-4 text-[#71717A]" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] py-2.5 pl-9 pr-3 font-mono text-xs focus:border-[#00C26E] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label className="block font-mono text-xs font-semibold">Password</label>
                <a href="#forgot" className="text-[11px] text-[#00C26E] hover:underline font-mono">
                  Forgot password?
                </a>
              </div>
              <div className="relative mt-1.5 flex items-center">
                <Lock className="absolute left-3 h-4 w-4 text-[#71717A]" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] py-2.5 pl-9 pr-3 font-mono text-xs focus:border-[#00C26E] focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-[#00C26E] py-2.5 font-mono text-xs font-bold text-black transition-all hover:bg-[#00E887] active:scale-95 disabled:opacity-50 shadow-md shadow-[#00C26E]/20"
            >
              {isLoading ? "Authenticating..." : tab === "login" ? "Sign In to Platform" : "Create Account & Start Onboarding"}
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </form>

          {/* Footer note */}
          <div className="text-center text-[11px] text-[#71717A] dark:text-[#8E8E93]">
            First time? You can start with our interactive{" "}
            <Link href="/onboarding" className="font-semibold text-[#00C26E] hover:underline">
              5-Step Onboarding Wizard ➔
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
