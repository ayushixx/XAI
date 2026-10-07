"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { CandidateProfile } from "./types";
import { DEFAULT_CANDIDATE } from "./data";

export interface DemoRoleProfile {
  id: string;
  roleType: "student" | "analyst" | "recruiter";
  name: string;
  title: string;
  avatar: string;
  companyOrSchool: string;
  profile: CandidateProfile;
}

export const DEMO_PROFILES: Record<string, DemoRoleProfile> = {
  student: {
    id: "DEMO-STU-01",
    roleType: "student",
    name: "Alex Chen",
    title: "CS Graduate & Aspiring ML Engineer",
    avatar: "AC",
    companyOrSchool: "Stanford CS",
    profile: {
      id: "STU-8BIT-01",
      name: "Alex Chen",
      currentRole: "CS Student / Junior ML Enthusiast",
      targetRole: "AI & Deep Learning Engineer",
      yearsExperience: 1.0,
      skills: ["Python", "NumPy", "Pandas", "Scikit-Learn", "Git"],
      personalityTraits: {
        conscientiousness: 8.4,
        openness: 9.0,
        extraversion: 6.8,
        agreeableness: 7.5,
        neuroticism: 3.4
      },
      metrics: {
        workforceReadinessScore: 82.4,
        jobFitScore: 68.5,
        skillGapPercentage: 31.5,
        careerAlignmentScore: 84.0,
        successProbability: 81.5
      }
    }
  },
  analyst: {
    id: "DEMO-ANA-02",
    roleType: "analyst",
    name: "Sarah Miller",
    title: "Senior Business & Data Analyst",
    avatar: "SM",
    companyOrSchool: "FinTech ScaleUp",
    profile: {
      id: "ANA-8BIT-02",
      name: "Sarah Miller",
      currentRole: "Senior Data Analyst",
      targetRole: "AI & Generative AI Architect",
      yearsExperience: 4.5,
      skills: ["SQL", "Python", "Pandas", "Tableau", "Power BI", "Scikit-Learn", "Docker"],
      personalityTraits: {
        conscientiousness: 8.8,
        openness: 8.2,
        extraversion: 7.4,
        agreeableness: 8.0,
        neuroticism: 2.8
      },
      metrics: {
        workforceReadinessScore: 88.6,
        jobFitScore: 78.0,
        skillGapPercentage: 22.0,
        careerAlignmentScore: 91.0,
        successProbability: 89.4
      }
    }
  },
  recruiter: {
    id: "DEMO-REC-03",
    roleType: "recruiter",
    name: "David Vance",
    title: "VP of Enterprise Talent & Workforce Strategy",
    avatar: "DV",
    companyOrSchool: "Apex Global Tech",
    profile: {
      id: "REC-8BIT-03",
      name: "David Vance (Talent Audit View)",
      currentRole: "Enterprise Talent Strategy Lead",
      targetRole: "Strategic AI Workforce Director",
      yearsExperience: 10.0,
      skills: ["Workforce Analytics", "Python", "SQL", "Team Leadership", "Talent Intelligence"],
      personalityTraits: {
        conscientiousness: 9.2,
        openness: 8.5,
        extraversion: 8.6,
        agreeableness: 8.4,
        neuroticism: 2.2
      },
      metrics: {
        workforceReadinessScore: 94.2,
        jobFitScore: 89.0,
        skillGapPercentage: 11.0,
        careerAlignmentScore: 96.0,
        successProbability: 95.0
      }
    }
  }
};

interface AuthContextType {
  activeProfile: CandidateProfile;
  currentRoleType: "student" | "analyst" | "recruiter";
  isAuthenticated: boolean;
  loginAs: (role: "student" | "analyst" | "recruiter") => void;
  logout: () => void;
  updateProfile: (updated: Partial<CandidateProfile>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [activeProfile, setActiveProfile] = useState<CandidateProfile>(DEFAULT_CANDIDATE);
  const [currentRoleType, setCurrentRoleType] = useState<"student" | "analyst" | "recruiter">("analyst");
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(true);

  useEffect(() => {
    const savedRole = localStorage.getItem("workforce_demo_role") as "student" | "analyst" | "recruiter" | null;
    if (savedRole && DEMO_PROFILES[savedRole]) {
      setCurrentRoleType(savedRole);
      setActiveProfile(DEMO_PROFILES[savedRole].profile);
    }
  }, []);

  const loginAs = (role: "student" | "analyst" | "recruiter") => {
    const target = DEMO_PROFILES[role];
    if (target) {
      setCurrentRoleType(role);
      setActiveProfile(target.profile);
      setIsAuthenticated(true);
      localStorage.setItem("workforce_demo_role", role);
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
  };

  const updateProfile = (updated: Partial<CandidateProfile>) => {
    setActiveProfile((prev) => ({ ...prev, ...updated }));
  };

  return (
    <AuthContext.Provider
      value={{
        activeProfile,
        currentRoleType,
        isAuthenticated,
        loginAs,
        logout,
        updateProfile
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
