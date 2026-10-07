import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercent(val: number, decimals: number = 1): string {
  return `${val >= 0 ? "+" : ""}${val.toFixed(decimals)}%`;
}

export function formatNumber(val: number): string {
  return new Intl.NumberFormat("en-US").format(val);
}

// Calculate Harmonic Weighted Employability Function (HWEF)
export function calculateHWEF(techScore: number, softScore: number, expRatio: number): number {
  const eps = 1e-5;
  const wTech = 0.5;
  const wSoft = 0.3;
  const wExp = 0.2;
  const denom = (wTech / (techScore + eps)) + (wSoft / (softScore + eps)) + (wExp / (expRatio + eps));
  return Math.min(100, Math.max(0, (wTech + wSoft + wExp) / denom));
}

// Calculate Workforce Readiness Index (WRI)
export function calculateWRI(
  c: number,
  o: number,
  e: number,
  a: number,
  n: number
): { score: number; tier: string } {
  // 0.30*C + 0.25*O + 0.20*E + 0.15*A - 0.10*N
  const raw = (0.30 * c * 10) + (0.25 * o * 10) + (0.20 * e * 10) + (0.15 * a * 10) - (0.10 * n * 10);
  const normalized = Math.min(100, Math.max(0, raw + 10));

  let tier = "Exceptional Readiness";
  if (normalized < 50) tier = "Coaching Required";
  else if (normalized < 65) tier = "Developing Readiness";
  else if (normalized < 80) tier = "Solid Professional";

  return { score: Number(normalized.toFixed(1)), tier };
}

// Cosine Similarity between two numeric vectors
export function cosineSimilarity(vecA: number[], vecB: number[]): number {
  if (vecA.length !== vecB.length || vecA.length === 0) return 0;
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
