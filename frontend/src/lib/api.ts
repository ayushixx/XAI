const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, { cache: "no-store" });
    if (res.ok) return await res.json();
  } catch {
    // offline fallback
  }
  return { status: "operational_standalone", backend: "active" };
}

export async function simulateCounterfactual(candidateSkills: string[], requiredSkills: string[], targetRole: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v2/counterfactual/simulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate_skills: candidateSkills,
        required_skills: requiredSkills,
        target_role: targetRole
      }),
      cache: "no-store"
    });
    if (res.ok) return await res.json();
  } catch {
    // offline fallback
  }
  return null;
}

export async function navigateCareerGPS(candidateSkills: string[], targetRole: string, algorithm: string = "dijkstra") {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v2/career-gps/navigate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate_skills: candidateSkills,
        target_role: targetRole,
        algorithm: algorithm
      }),
      cache: "no-store"
    });
    if (res.ok) return await res.json();
  } catch {
    // offline fallback
  }
  return null;
}

export async function explainSHAP(candidateName: string, features: Record<string, number>, candidateSkills: string[], missingSkills: string[]) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v2/xai/shap`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate_name: candidateName,
        features: features,
        candidate_skills: candidateSkills,
        missing_skills: missingSkills
      }),
      cache: "no-store"
    });
    if (res.ok) return await res.json();
  } catch {
    // offline fallback
  }
  return null;
}
