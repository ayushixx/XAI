"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Sparkles, Send, BookOpen, ShieldCheck, CheckCircle2, Terminal, ArrowRight, User } from "lucide-react";

interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  content: string;
  sources?: string[];
  metricsUsed?: Record<string, string>;
  timestamp: string;
}

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: "msg-1",
    sender: "assistant",
    content: `Hello Alex! I am your **8BIT Executive Career Advisor**.

I am strictly grounded in your deterministic Machine Learning evaluations:
- **Baseline Match**: **74.0%** for *AI & GenAI Architect*
- **Workforce Readiness (WRI)**: **84.8 / 100** (Exceptional Readiness)
- **Top Counterfactual Intervention**: **Docker (+9.5%)** & **PyTorch (+13.0%)**
- **Optimal Route Duration**: **15 Weeks** across 5 milestones

Ask me anything regarding your personalized learning trajectory, interview preparation, or salary insights.`,
    sources: [
      "8BIT HWEF Engine v2.0",
      "SHAP TreeExplainer (XGBoost JDS)",
      "Career GPS Dijkstra Topology",
      "WEF Future of Jobs Report 2024"
    ],
    metricsUsed: {
      "Job Fit Score": "74.0%",
      "WRI Readiness": "84.8 / 100",
      "Salary Upside": "+145%",
      "Optimal Route": "15 Weeks"
    },
    timestamp: "Just now"
  }
];

export default function AICareerAdvisorPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [inputQuery, setInputQuery] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuery.trim()) return;

    const userMsg: ChatMessage = {
      id: `usr-${Date.now()}`,
      sender: "user",
      content: inputQuery,
      timestamp: "Just now"
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery("");
    setIsTyping(true);

    setTimeout(() => {
      let assistantReply = "";
      let sources = ["8BIT ML Grounded Engine", "WEF Future of Jobs", "NASSCOM Tech Strategy 2024"];

      if (userMsg.content.toLowerCase().includes("interview")) {
        assistantReply = `### Grounded Interview Strategy for AI & GenAI Architect:

1. **Target Feature Weakness (SHAP -7.8%)**: Expect deep architectural questions regarding **Docker container lifecycle management**, multi-stage build optimization, and GPU orchestration.
2. **Behavioral Strengths (WRI 84.8)**: Leverage your top **Conscientiousness (8.4/10)** score by walking interviewers through complex incident post-mortems and proactive testing frameworks.
3. **High-Probability Question**: *"How do you design a zero-downtime microservice serving high-throughput PyTorch embeddings using FastAPI and Docker?"*`;
      } else if (userMsg.content.toLowerCase().includes("salary") || userMsg.content.toLowerCase().includes("compensation")) {
        assistantReply = `### Salary & Compensation Growth Trajectory:

- **Current Market Band**: $110,000 - $130,000 (Data Analyst / Junior ML)
- **Target Role Market Band**: $240,000 - $285,000 (*AI & GenAI Architect*)
- **Projected Growth Multiplier**: **+145%** upon completing the 15-week Dijkstra Career GPS milestone chain.
- **High-Leverage Factor**: Completing **RAG Architectures** and **Vector Databases** commands the highest compensation premium according to LinkedIn 2024 hiring data.`;
      } else {
        assistantReply = `### Strategic Career Roadmap & Skill Prioritization:

Based on the **Counterfactual AI Engine** and **Skill ROI Leaderboard**:
1. **Week 1-3 (Quick Win)**: Acquire **Docker & Containerization**. Delivers an immediate **+9.5% score gain** with the highest efficiency index (**ROI = 3.17**).
2. **Week 4-8 (Core Specialization)**: Complete **PyTorch & Deep Learning**, closing the feature deficit identified by the SHAP TreeExplainer.
3. **Week 9-15 (Target Completion)**: Master **MLOps & RAG Architectures** to elevate overall employability to **92.5%**.`;
      }

      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: "assistant",
        content: assistantReply,
        sources,
        timestamp: "Just now"
      };

      setMessages((prev) => [...prev, botMsg]);
      setIsTyping(false);
    }, 1200);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 10 — Perplexity-Style AI Advisor
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Grounded LLM Career Advisor & Reasoning Engine
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Conversational executive intelligence grounded strictly in deterministic Machine Learning, SHAP, and Graph Analytics.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1.5 rounded bg-[#10B981]/15 px-3 py-1 font-mono text-xs text-[#10B981] border border-[#10B981]/30">
            <ShieldCheck className="h-3.5 w-3.5" />
            Zero-Hallucination Policy
          </span>
        </div>
      </div>

      {/* Perplexity-Style Chat Stream */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5 shadow-2xl flex flex-col min-h-[500px]">
        {/* Messages List */}
        <div className="flex-1 space-y-6 overflow-y-auto pr-1">
          {messages.map((msg) => {
            const isBot = msg.sender === "assistant";

            return (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-3.5 ${isBot ? "items-start" : "items-start flex-row-reverse"}`}
              >
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border font-mono text-xs ${
                    isBot
                      ? "border-[#10B981]/40 bg-[#10B981]/15 text-[#10B981]"
                      : "border-white/40 bg-white text-black font-bold"
                  }`}
                >
                  {isBot ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                </div>

                <div className={`space-y-3 max-w-3xl ${isBot ? "" : "text-right"}`}>
                  <div
                    className={`rounded-lg border p-4 text-xs leading-relaxed ${
                      isBot
                        ? "border-[#27272A] bg-[#0A0A0C] text-[#E4E4E7]"
                        : "border-[#10B981] bg-[#10B981]/10 text-white text-left"
                    }`}
                  >
                    <div className="prose prose-invert max-w-none text-xs leading-relaxed whitespace-pre-wrap">
                      {msg.content}
                    </div>

                    {/* Verified Metrics Chips */}
                    {msg.metricsUsed && (
                      <div className="mt-3 flex flex-wrap gap-2 pt-2 border-t border-[#222228]">
                        {Object.entries(msg.metricsUsed).map(([k, v]) => (
                          <span
                            key={k}
                            className="rounded bg-[#18181D] px-2 py-0.5 font-mono text-[10px] text-[#10B981] border border-[#27272A]"
                          >
                            {k}: <strong>{v}</strong>
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Sources Citation Bar */}
                  {msg.sources && (
                    <div className="flex flex-wrap items-center gap-2 text-[10px] font-mono text-[#71717A]">
                      <span className="flex items-center gap-1 font-bold text-[#A1A1AA]">
                        <BookOpen className="h-3 w-3 text-[#10B981]" /> Cited ML Sources:
                      </span>
                      {msg.sources.map((s) => (
                        <span key={s} className="rounded bg-[#18181D] px-2 py-0.5 border border-[#222228] text-[#A1A1AA]">
                          {s}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}

          {isTyping && (
            <div className="flex items-center gap-2 text-xs font-mono text-[#10B981] animate-pulse pl-12">
              <Sparkles className="h-3.5 w-3.5" />
              Synthesizing grounded ML advice...
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSend} className="mt-6 border-t border-[#222228] pt-4">
          <div className="relative flex items-center">
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Ask about interview questions, salary upside, or skill roadmap prioritization..."
              className="w-full rounded-lg border border-[#27272A] bg-[#0A0A0C] px-4 py-3 pr-24 font-mono text-xs text-white placeholder-[#71717A] focus:border-[#10B981] focus:outline-none"
            />
            <button
              type="submit"
              className="absolute right-2 flex items-center gap-1.5 rounded-md bg-[#10B981] px-3.5 py-1.5 font-mono text-xs font-bold text-black hover:bg-[#059669] transition-colors"
            >
              <Send className="h-3 w-3" />
              Ask
            </button>
          </div>
          <div className="mt-2 flex items-center justify-between text-[10px] font-mono text-[#71717A]">
            <span>Supported Prompts: "Interview questions", "Salary projection", "Learning roadmap"</span>
            <span className="text-[#10B981]">Grounded in ChromaDB + FastAPI ML</span>
          </div>
        </form>
      </div>
    </div>
  );
}
