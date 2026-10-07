"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Sparkles,
  Network,
  Compass,
  Sliders,
  Eye,
  TrendingUp,
  BrainCircuit,
  LineChart,
  Bot,
  Terminal,
  Home,
  User,
  ChevronRight,
  LogOut,
  GraduationCap,
  Briefcase,
  Users
} from "lucide-react";
import { useAuth, DEMO_PROFILES } from "@/lib/auth-context";

export function Sidebar() {
  const pathname = usePathname();
  const { activeProfile, currentRoleType, loginAs } = useAuth();

  const navGroups = [
    {
      group: "ANALYTICS",
      items: [
        { label: "Overview Home", href: "/", icon: Home },
        { label: "Workforce Dashboard", href: "/dashboard", icon: LayoutDashboard },
        { label: "Future Demand Forecast", href: "/future-demand", icon: LineChart }
      ]
    },
    {
      group: "AI MODELS",
      items: [
        { label: "Semantic Matching", href: "/semantic-matching", icon: Sparkles },
        { label: "Counterfactual AI", href: "/counterfactual", icon: Sliders, badge: "Core" },
        { label: "SHAP Explainability", href: "/explainable-ai", icon: Eye },
        { label: "Skill ROI Optimizer", href: "/skill-roi", icon: TrendingUp }
      ]
    },
    {
      group: "INTELLIGENCE",
      items: [
        { label: "Knowledge Graph", href: "/knowledge-graph", icon: Network },
        { label: "Career GPS", href: "/career-gps", icon: Compass },
        { label: "Digital Twin", href: "/digital-twin", icon: BrainCircuit }
      ]
    },
    {
      group: "ASSISTANT",
      items: [
        { label: "AI Career Advisor", href: "/advisor", icon: Bot, badge: "RAG" }
      ]
    },
    {
      group: "LAB",
      items: [
        { label: "Algorithm Lab", href: "/algorithm-lab", icon: Terminal, badge: "Judges" }
      ]
    }
  ];

  return (
    <aside className="sticky top-14 hidden h-[calc(100vh-3.5rem)] w-64 flex-col justify-between border-r border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#0A0A0A] p-3 lg:flex">
      {/* Scrollable Navigation Area */}
      <nav className="flex flex-1 flex-col gap-5 overflow-y-auto pr-1">
        {navGroups.map((grp) => (
          <div key={grp.group} className="space-y-1">
            <div className="px-2.5 py-0.5">
              <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-[#71717A] dark:text-[#8E8E93]">
                {grp.group}
              </span>
            </div>

            <div className="space-y-0.5">
              {grp.items.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`group flex items-center justify-between rounded-lg px-2.5 py-1.5 text-xs font-medium transition-all ${
                      isActive
                        ? "bg-[#00C26E]/10 text-[#111111] dark:text-[#FFFFFF] border border-[#00C26E]/30 font-semibold"
                        : "text-[#71717A] dark:text-[#8E8E93] hover:bg-[#F7F7F7] dark:hover:bg-[#141414] hover:text-[#111111] dark:hover:text-[#FFFFFF]"
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon
                        className={`h-4 w-4 transition-colors ${
                          isActive
                            ? "text-[#00C26E]"
                            : "text-[#71717A] dark:text-[#8E8E93] group-hover:text-[#111111] dark:group-hover:text-[#FFFFFF]"
                        }`}
                      />
                      <span>{item.label}</span>
                    </div>

                    {item.badge && (
                      <span
                        className={`rounded px-1.5 py-0.2 font-mono text-[9px] font-bold ${
                          item.badge === "Judges" || item.badge === "Core"
                            ? "bg-[#00C26E]/20 text-[#00C26E]"
                            : "bg-[#E5E7EB] dark:bg-[#262626] text-[#71717A] dark:text-[#8E8E93]"
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* User Profile & Demo Switcher Footer */}
      <div className="border-t border-[#E5E7EB] dark:border-[#262626] pt-3 space-y-2">
        <div className="flex items-center justify-between rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#141414] p-2">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#00C26E]/15 font-mono text-xs font-bold text-[#00C26E]">
              {currentRoleType === "student" ? "ST" : currentRoleType === "analyst" ? "DA" : "RC"}
            </div>
            <div className="overflow-hidden">
              <span className="block truncate font-mono text-xs font-bold">
                {activeProfile.name}
              </span>
              <span className="block truncate text-[10px] text-[#71717A] dark:text-[#8E8E93]">
                {activeProfile.currentRole}
              </span>
            </div>
          </div>

          <Link href="/login" title="Switch Demo Profile" className="p-1 text-[#71717A] hover:text-[#00C26E]">
            <LogOut className="h-3.5 w-3.5" />
          </Link>
        </div>

        {/* Quick Demo Role Pill Selector */}
        <div className="grid grid-cols-3 gap-1 text-center font-mono text-[9px]">
          <button
            onClick={() => loginAs("student")}
            className={`rounded py-1 font-semibold transition-all ${
              currentRoleType === "student"
                ? "bg-[#00C26E] text-black"
                : "border border-[#E5E7EB] dark:border-[#262626] hover:bg-[#E5E7EB] dark:hover:bg-[#262626]"
            }`}
          >
            Student
          </button>
          <button
            onClick={() => loginAs("analyst")}
            className={`rounded py-1 font-semibold transition-all ${
              currentRoleType === "analyst"
                ? "bg-[#00C26E] text-black"
                : "border border-[#E5E7EB] dark:border-[#262626] hover:bg-[#E5E7EB] dark:hover:bg-[#262626]"
            }`}
          >
            Analyst
          </button>
          <button
            onClick={() => loginAs("recruiter")}
            className={`rounded py-1 font-semibold transition-all ${
              currentRoleType === "recruiter"
                ? "bg-[#00C26E] text-black"
                : "border border-[#E5E7EB] dark:border-[#262626] hover:bg-[#E5E7EB] dark:hover:bg-[#262626]"
            }`}
          >
            Recruiter
          </button>
        </div>
      </div>
    </aside>
  );
}
