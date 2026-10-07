"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Briefcase,
  Target,
  Layers,
  GraduationCap,
  Zap,
  Cpu
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { ThemeToggle } from "@/components/ThemeToggle";

const ROLES_LIST = [
  "Data Analyst",
  "Junior ML Engineer",
  "Software Engineer",
  "Data Scientist",
  "DevOps Engineer",
  "Business Intelligence Developer",
  "CS Graduate Student"
];

const TARGET_ROLES_LIST = [
  "AI & Generative AI Architect",
  "Senior MLOps & Production AI Lead",
  "Staff Data Scientist",
  "Big Data Solutions Architect",
  "Principal AI Research Scientist"
];

const SKILLS_LIBRARY = [
  "Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Docker", "Kubernetes",
  "FastAPI", "PyTorch", "TensorFlow", "MLOps", "Transformers", "RAG Architectures",
  "ChromaDB", "Tableau", "Power BI", "Snowflake", "Databricks", "Git", "CI/CD"
];

export default function OnboardingPage() {
  const router = useRouter();
  const { updateProfile } = useAuth();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  // Form State
  const [currentRole, setCurrentRole] = useState("Data Analyst");
  const [targetRole, setTargetRole] = useState("AI & Generative AI Architect");
  const [selectedSkills, setSelectedSkills] = useState<string[]>(["Python", "SQL", "Pandas", "Scikit-Learn"]);
  const [yearsExperience, setYearsExperience] = useState(3.5);
  const [education, setEducation] = useState("B.S. Computer Science & Statistics");

  const toggleSkill = (skill: string) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter((s) => s !== skill));
    } else {
      setSelectedSkills([...selectedSkills, skill]);
    }
  };

  const handleFinishOnboarding = () => {
    setIsGenerating(true);
    updateProfile({
      currentRole,
      targetRole,
      skills: selectedSkills,
      yearsExperience
    });

    setTimeout(() => {
      router.push("/dashboard");
    }, 2000);
  };

  return (
    <div className="flex min-h-screen flex-col bg-[#FFFFFF] dark:bg-[#0A0A0A] text-[#111111] dark:text-[#FFFFFF] transition-colors">
      {/* Top Bar */}
      <header className="flex h-14 items-center justify-between border-b border-[#E5E7EB] dark:border-[#262626] px-6">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#00C26E] font-mono text-sm font-black text-black">
            8B
          </div>
          <span className="font-mono text-sm font-bold">8BIT Onboarding</span>
        </div>

        <div className="flex items-center gap-3">
          <span className="font-mono text-xs text-[#71717A] dark:text-[#8E8E93]">
            Step {step} of 5
          </span>
          <ThemeToggle />
        </div>
      </header>

      {/* Main Container */}
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center px-6 py-12">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between font-mono text-xs font-semibold text-[#71717A] dark:text-[#8E8E93] mb-2">
            <span>{step === 1 ? "Current Role" : step === 2 ? "Target Goal" : step === 3 ? "Skills Profile" : step === 4 ? "Experience" : "Profile Generation"}</span>
            <span>{Math.round((step / 5) * 100)}% Completed</span>
          </div>
          <div className="h-2 w-full rounded-full bg-[#E5E7EB] dark:bg-[#262626] overflow-hidden">
            <motion.div
              className="h-full bg-[#00C26E]"
              initial={{ width: "20%" }}
              animate={{ width: `${(step / 5) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="rounded-2xl border border-[#E5E7EB] dark:border-[#262626] bg-[#FFFFFF] dark:bg-[#141414] p-8 shadow-lg">
          <AnimatePresence mode="wait">
            {/* Step 1: Current Role */}
            {step === 1 && (
              <motion.div
                key="step-1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div>
                  <div className="inline-flex items-center gap-1.5 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[11px] font-bold text-[#00C26E]">
                    <Briefcase className="h-3 w-3" /> Step 1 of 5
                  </div>
                  <h2 className="text-2xl font-bold tracking-tight mt-1">What is your current role?</h2>
                  <p className="text-xs text-[#71717A] dark:text-[#8E8E93] mt-1">
                    This provides the baseline anchor for knowledge graph distance calculations.
                  </p>
                </div>

                <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
                  {ROLES_LIST.map((role) => (
                    <button
                      key={role}
                      type="button"
                      onClick={() => setCurrentRole(role)}
                      className={`flex items-center justify-between rounded-xl border p-3.5 text-left font-mono text-xs font-semibold transition-all ${
                        currentRole === role
                          ? "border-[#00C26E] bg-[#00C26E]/10 text-[#111111] dark:text-[#FFFFFF] shadow-sm shadow-[#00C26E]/10"
                          : "border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] text-[#71717A] dark:text-[#8E8E93] hover:border-[#00C26E]"
                      }`}
                    >
                      <span>{role}</span>
                      {currentRole === role && <CheckCircle2 className="h-4 w-4 text-[#00C26E]" />}
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Step 2: Target Career */}
            {step === 2 && (
              <motion.div
                key="step-2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div>
                  <div className="inline-flex items-center gap-1.5 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[11px] font-bold text-[#00C26E]">
                    <Target className="h-3 w-3" /> Step 2 of 5
                  </div>
                  <h2 className="text-2xl font-bold tracking-tight mt-1">What is your target destination?</h2>
                  <p className="text-xs text-[#71717A] dark:text-[#8E8E93] mt-1">
                    The Career GPS Dijkstra engine will chart the shortest upskilling path to this role.
                  </p>
                </div>

                <div className="space-y-2.5">
                  {TARGET_ROLES_LIST.map((role) => (
                    <button
                      key={role}
                      type="button"
                      onClick={() => setTargetRole(role)}
                      className={`flex w-full items-center justify-between rounded-xl border p-3.5 text-left font-mono text-xs font-semibold transition-all ${
                        targetRole === role
                          ? "border-[#00C26E] bg-[#00C26E]/10 text-[#111111] dark:text-[#FFFFFF] shadow-sm shadow-[#00C26E]/10"
                          : "border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] text-[#71717A] dark:text-[#8E8E93] hover:border-[#00C26E]"
                      }`}
                    >
                      <span>{role}</span>
                      {targetRole === role && <CheckCircle2 className="h-4 w-4 text-[#00C26E]" />}
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Step 3: Skills Inventory */}
            {step === 3 && (
              <motion.div
                key="step-3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div>
                  <div className="inline-flex items-center gap-1.5 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[11px] font-bold text-[#00C26E]">
                    <Layers className="h-3 w-3" /> Step 3 of 5
                  </div>
                  <h2 className="text-2xl font-bold tracking-tight mt-1">Select your verified skills</h2>
                  <p className="text-xs text-[#71717A] dark:text-[#8E8E93] mt-1">
                    Sentence-BERT embeds your skill cluster to detect semantic equivalencies and skill gaps.
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {SKILLS_LIBRARY.map((skill) => {
                    const isSelected = selectedSkills.includes(skill);
                    return (
                      <button
                        key={skill}
                        type="button"
                        onClick={() => toggleSkill(skill)}
                        className={`rounded-lg border px-3 py-1.5 font-mono text-xs font-semibold transition-all ${
                          isSelected
                            ? "border-[#00C26E] bg-[#00C26E] text-black shadow-sm"
                            : "border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] text-[#71717A] dark:text-[#8E8E93] hover:border-[#00C26E]"
                        }`}
                      >
                        {skill} {isSelected ? "✓" : "+"}
                      </button>
                    );
                  })}
                </div>
                <div className="text-[11px] text-[#00C26E] font-mono">
                  {selectedSkills.length} skills selected for profile vector embedding.
                </div>
              </motion.div>
            )}

            {/* Step 4: Experience */}
            {step === 4 && (
              <motion.div
                key="step-4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-6"
              >
                <div>
                  <div className="inline-flex items-center gap-1.5 rounded bg-[#00C26E]/10 px-2 py-0.5 font-mono text-[11px] font-bold text-[#00C26E]">
                    <GraduationCap className="h-3 w-3" /> Step 4 of 5
                  </div>
                  <h2 className="text-2xl font-bold tracking-tight mt-1">Experience & Background</h2>
                  <p className="text-xs text-[#71717A] dark:text-[#8E8E93] mt-1">
                    Harmonic Weighted Employability (HWEF) factors experience ratios into the final score.
                  </p>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between font-mono text-xs">
                      <span>Years of Relevant Industry Experience</span>
                      <span className="font-bold text-[#00C26E]">{yearsExperience} Years</span>
                    </div>
                    <input
                      type="range"
                      min="0.5"
                      max="15.0"
                      step="0.5"
                      value={yearsExperience}
                      onChange={(e) => setYearsExperience(parseFloat(e.target.value))}
                      className="mt-2 w-full accent-[#00C26E]"
                    />
                  </div>

                  <div>
                    <label className="block font-mono text-xs font-semibold">Highest Education Level</label>
                    <input
                      type="text"
                      value={education}
                      onChange={(e) => setEducation(e.target.value)}
                      className="mt-1.5 w-full rounded-lg border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] p-2.5 font-mono text-xs focus:border-[#00C26E] focus:outline-none"
                    />
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 5: Profile Generation */}
            {step === 5 && (
              <motion.div
                key="step-5"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-6 text-center py-4"
              >
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[#00C26E]/15 text-[#00C26E]">
                  <Cpu className={`h-8 w-8 ${isGenerating ? "animate-spin" : ""}`} />
                </div>

                <div>
                  <h2 className="text-2xl font-bold tracking-tight">Ready to Generate Workforce Profile</h2>
                  <p className="text-xs text-[#71717A] dark:text-[#8E8E93] mt-1 max-w-md mx-auto">
                    The platform will calculate Sentence-BERT embeddings, HWEF scores, SHAP TreeExplainer attributions, and Dijkstra career navigation.
                  </p>
                </div>

                <div className="rounded-xl border border-[#E5E7EB] dark:border-[#262626] bg-[#F7F7F7] dark:bg-[#1A1A1A] p-4 text-left font-mono text-xs space-y-1.5">
                  <div className="flex justify-between">
                    <span className="text-[#71717A]">Target Role:</span>
                    <span className="font-bold text-[#00C26E]">{targetRole}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#71717A]">Skills Count:</span>
                    <span className="font-bold">{selectedSkills.length} Verified</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#71717A]">Experience Ratio:</span>
                    <span className="font-bold">{yearsExperience} Years</span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Stepper Buttons */}
          <div className="mt-8 flex items-center justify-between border-t border-[#E5E7EB] dark:border-[#262626] pt-5">
            {step > 1 ? (
              <button
                type="button"
                onClick={() => setStep(step - 1)}
                className="flex items-center gap-1.5 rounded-lg border border-[#E5E7EB] dark:border-[#262626] px-4 py-2 font-mono text-xs font-semibold hover:border-[#71717A]"
              >
                <ArrowLeft className="h-3.5 w-3.5" /> Back
              </button>
            ) : (
              <div />
            )}

            {step < 5 ? (
              <button
                type="button"
                onClick={() => setStep(step + 1)}
                className="flex items-center gap-1.5 rounded-lg bg-[#00C26E] px-5 py-2 font-mono text-xs font-bold text-black hover:bg-[#00E887] shadow-sm transition-all"
              >
                Continue <ArrowRight className="h-3.5 w-3.5" />
              </button>
            ) : (
              <button
                type="button"
                disabled={isGenerating}
                onClick={handleFinishOnboarding}
                className="flex items-center gap-2 rounded-lg bg-[#00C26E] px-6 py-2.5 font-mono text-xs font-bold text-black hover:bg-[#00E887] shadow-md shadow-[#00C26E]/20 transition-all disabled:opacity-50"
              >
                {isGenerating ? "Synthesizing ML Profile..." : "Launch Workforce Dashboard"}
                <Sparkles className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
