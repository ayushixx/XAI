export interface CandidateProfile {
  id: string;
  name: string;
  currentRole: string;
  targetRole: string;
  yearsExperience: number;
  skills: string[];
  personalityTraits: {
    neuroticism: number; // 0 - 10 scale
    extraversion: number;
    openness: number;
    agreeableness: number;
    conscientiousness: number;
  };
  metrics: {
    workforceReadinessScore: number;
    jobFitScore: number;
    skillGapPercentage: number;
    careerAlignmentScore: number;
    successProbability: number;
  };
}

export interface SkillNode {
  id: string;
  label: string;
  category: "Languages" | "Data & ML" | "Cloud & DevOps" | "AI & GenAI" | "Databases";
  pageRank: number;
  degreeCentrality: number;
  difficulty: "Foundational" | "Intermediate" | "Advanced" | "Expert";
  estimatedWeeks: number;
  prerequisites: string[];
  historicalGrowthCAGR: number;
}

export interface CareerRouteStep {
  step: number;
  skill: string;
  learningWeeks: number;
  milestoneRole: string;
  salaryMultiplier: string;
  difficultyScore: number;
  rationale: string;
}

export interface CounterfactualRec {
  skill: string;
  marginalGain: number; // e.g. +13.0%
  counterfactualScore: number; // e.g. 87.0%
  learningTimeWeeks: number;
  roiIndex: number;
  whyRecommended: string;
  difficulty: string;
}

export interface SHAPContribution {
  feature: string;
  featureValue: number;
  shapValue: number;
  direction: "positive" | "negative";
}

export interface FutureSkillDemand {
  skill: string;
  domain: string;
  status: "Hyper-Growth" | "High Growth" | "Stable" | "Declining";
  growthCAGR: number;
  actualDemand2024: number;
  projectedDemand2025: number;
  projectedDemand2026: number;
  projectedDemand2029: number;
}

export interface AlgorithmCard {
  id: string;
  name: string;
  category: "Semantic NLP" | "Graph Theory" | "Machine Learning" | "Explainability" | "Optimization" | "GenAI & RAG";
  purpose: string;
  formula: string;
  formulaExplanation: string;
  inputs: string[];
  outputs: string[];
  keyMetric: string;
  codeSnippet: string;
}
