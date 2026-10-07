"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Sparkles,
  Terminal,
  Menu,
  X,
  User,
  Sliders,
  Compass,
  LayoutDashboard,
  Eye,
  LineChart,
  Bot
} from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useAuth } from "@/lib/auth-context";

export function Navbar() {
  const pathname = usePathname();
  const { activeProfile, currentRoleType } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // If on login or onboarding page, display minimal header
  if (pathname === "/login" || pathname === "/onboarding") {
    return null;
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF]/90 dark:bg-[#0A0A0A]/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
        {/* Left Branding */}
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2.5 font-bold tracking-tight hover:opacity-90">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#00C26E] font-mono text-sm font-black text-black shadow-sm shadow-[#00C26E]/20">
              8B
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-mono text-base font-bold tracking-wider">8BIT</span>
              <span className="rounded border border-[#00C26E]/40 bg-[#00C26E]/10 px-1.5 py-0.5 font-mono text-[9px] font-bold text-[#00C26E]">
                ENTERPRISE
              </span>
            </div>
          </Link>

          {/* Quick Header Nav */}
          <nav className="hidden md:flex items-center gap-1 text-xs">
            <Link
              href="/dashboard"
              className={`rounded-md px-2.5 py-1.5 font-medium transition-colors ${
                pathname === "/dashboard"
                  ? "bg-[#E5E7EB] dark:bg-[#1A1A1A] font-semibold"
                  : "text-[#71717A] dark:text-[#8E8E93] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              Dashboard
            </Link>
            <Link
              href="/counterfactual"
              className={`rounded-md px-2.5 py-1.5 font-medium transition-colors ${
                pathname === "/counterfactual"
                  ? "bg-[#E5E7EB] dark:bg-[#1A1A1A] font-semibold"
                  : "text-[#71717A] dark:text-[#8E8E93] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              Counterfactual AI
            </Link>
            <Link
              href="/career-gps"
              className={`rounded-md px-2.5 py-1.5 font-medium transition-colors ${
                pathname === "/career-gps"
                  ? "bg-[#E5E7EB] dark:bg-[#1A1A1A] font-semibold"
                  : "text-[#71717A] dark:text-[#8E8E93] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              Career GPS
            </Link>
            <Link
              href="/explainable-ai"
              className={`rounded-md px-2.5 py-1.5 font-medium transition-colors ${
                pathname === "/explainable-ai"
                  ? "bg-[#E5E7EB] dark:bg-[#1A1A1A] font-semibold"
                  : "text-[#71717A] dark:text-[#8E8E93] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
              }`}
            >
              SHAP XAI
            </Link>
            <Link
              href="/algorithm-lab"
              className={`flex items-center gap-1 rounded-md px-2.5 py-1.5 font-mono text-[11px] font-semibold transition-colors ${
                pathname === "/algorithm-lab"
                  ? "bg-[#00C26E]/15 text-[#00C26E]"
                  : "text-[#00C26E] hover:bg-[#00C26E]/10"
              }`}
            >
              <Terminal className="h-3 w-3" />
              Algorithm Lab
            </Link>
          </nav>
        </div>

        {/* Right Status, Theme & Profile */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 rounded-full border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#141414] px-2.5 py-1 text-[11px]">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#00C26E] opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-[#00C26E]"></span>
            </span>
            <span className="font-mono text-[11px]">ML Engines Active</span>
          </div>

          <Link
            href="/advisor"
            className="hidden sm:flex items-center gap-1.5 rounded-lg bg-[#00C26E] px-3 py-1.5 font-mono text-xs font-bold text-black transition-all hover:bg-[#00E887] shadow-sm shadow-[#00C26E]/15"
          >
            <Sparkles className="h-3.5 w-3.5 fill-black" />
            <span>AI Advisor</span>
          </Link>

          {/* Theme Toggle Button */}
          <ThemeToggle />

          {/* User Profile Avatar Link */}
          <Link
            href="/login"
            className="flex h-8 items-center gap-1.5 rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] px-2 text-xs font-mono font-semibold transition-colors hover:border-[#00C26E]"
            title="User Profile & Role Switcher"
          >
            <User className="h-3.5 w-3.5 text-[#00C26E]" />
            <span className="hidden md:inline capitalize">{currentRoleType}</span>
          </Link>

          {/* Mobile Menu Hamburger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-[#E5E7EB] dark:border-[#262626] lg:hidden"
          >
            {mobileMenuOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="border-b border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#0A0A0A] p-4 lg:hidden space-y-2">
          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
            <Link
              href="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#E5E7EB] dark:border-[#262626] p-2.5"
            >
              <LayoutDashboard className="h-4 w-4 text-[#00C26E]" />
              <span>Dashboard</span>
            </Link>
            <Link
              href="/counterfactual"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#E5E7EB] dark:border-[#262626] p-2.5"
            >
              <Sliders className="h-4 w-4 text-[#00C26E]" />
              <span>Counterfactual</span>
            </Link>
            <Link
              href="/career-gps"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#E5E7EB] dark:border-[#262626] p-2.5"
            >
              <Compass className="h-4 w-4 text-[#00C26E]" />
              <span>Career GPS</span>
            </Link>
            <Link
              href="/explainable-ai"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#E5E7EB] dark:border-[#262626] p-2.5"
            >
              <Eye className="h-4 w-4 text-[#00C26E]" />
              <span>SHAP XAI</span>
            </Link>
            <Link
              href="/advisor"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#00C26E] bg-[#00C26E]/10 p-2.5 text-[#00C26E] font-bold"
            >
              <Bot className="h-4 w-4" />
              <span>AI Advisor</span>
            </Link>
            <Link
              href="/algorithm-lab"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 rounded-lg border border-[#00C26E] bg-[#00C26E]/10 p-2.5 text-[#00C26E] font-bold"
            >
              <Terminal className="h-4 w-4" />
              <span>Algorithm Lab</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
