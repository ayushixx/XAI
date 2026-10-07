from typing import Dict, Any, List, Optional
from src.config.hwef_config import load_weights
from src.semantic_matching.semantic_engine import get_semantic_matcher
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

class HWEFEngine:
    """
    Hybrid Weighted Evaluation Fusion (HWEF) Layer
    Merges multi-modal evaluation signals (semantic skills, experience, projects, certifications,
    and legacy ML classifier probability) into an explainable, calibrated Job Fit & Ranking Score.
    """
    def __init__(self):
        self.matcher = get_semantic_matcher()
        self.kg = get_knowledge_graph()

    def calculate_experience_score(self, candidate_years: float, required_years: float) -> float:
        """Calibrates experience match on a 0-100 scale with smooth non-linear saturation."""
        if required_years <= 0:
            return 100.0
        ratio = candidate_years / required_years
        if ratio >= 1.2:
            return 100.0
        elif ratio >= 1.0:
            return 95.0 + (ratio - 1.0) * 25.0
        elif ratio >= 0.75:
            return 80.0 + (ratio - 0.75) * 60.0
        elif ratio >= 0.50:
            return 60.0 + (ratio - 0.50) * 80.0
        else:
            return max(15.0, ratio * 100.0)

    def calculate_project_score(self, candidate_projects: List[Dict[str, Any]], target_role: str) -> float:
        """Scores project relevance based on domain alignment and technical depth."""
        if not candidate_projects:
            return 40.0  # baseline for zero reported projects
        
        total_score = 0.0
        for proj in candidate_projects:
            # Score each project based on tech stack relevance and complexity
            tech_stack = proj.get("tech_stack", [])
            stars_or_impact = proj.get("impact_score", 75)
            
            # Match project tech against target role domain
            match_res = self.matcher.match_skills(tech_stack, [target_role, "Machine Learning", "Data Engineering", "Analytics"])
            proj_relevance = match_res["semantic_similarity_score"] * 100.0
            
            combined_proj = (proj_relevance * 0.6) + (stars_or_impact * 0.4)
            total_score += combined_proj

        avg_score = total_score / len(candidate_projects)
        # Bonus for portfolio breadth (up to 15%)
        breadth_bonus = min(15.0, len(candidate_projects) * 4.0)
        return min(100.0, round(avg_score * 0.85 + breadth_bonus, 2))

    def calculate_certification_score(self, certifications: List[str]) -> float:
        """Scores industry certifications (AWS, GCP, Azure, TensorFlow, Databricks, etc.)."""
        if not certifications:
            return 35.0  # baseline
        
        tier1_keywords = ["professional", "specialty", "architect", "expert", "tensorflow", "databricks"]
        tier2_keywords = ["associate", "developer", "practitioner", "coursera", "udacity", "deeplearning.ai"]
        
        score = 40.0
        for cert in certifications:
            c_low = cert.lower()
            if any(k in c_low for k in tier1_keywords):
                score += 25.0
            elif any(k in c_low for k in tier2_keywords):
                score += 15.0
            else:
                score += 10.0
        
        return min(100.0, round(score, 2))

    def evaluate_candidate(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        candidate_years_exp: float = 3.0,
        required_years_exp: float = 3.0,
        candidate_projects: Optional[List[Dict[str, Any]]] = None,
        certifications: Optional[List[str]] = None,
        ml_prediction_score: Optional[float] = None,
        target_role: str = "Data Scientist",
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Executes complete HWEF Fusion pipeline.
        Returns:
            - job_fit_score: float (0 - 100)
            - skill_gap_percentage: float (0 - 100)
            - candidate_ranking_score: float (0 - 100)
            - signal_breakdown: Dict of component scores & weighted contributions
            - explainability: Clear human-readable attribution breakdown
        """
        weights = custom_weights if custom_weights else load_weights()

        # 1. Semantic Skill Match Score
        skill_match_res = self.matcher.match_skills(candidate_skills, required_skills)
        skill_match_score = skill_match_res["semantic_similarity_score"] * 100.0

        # 2. Experience Match Score
        exp_score = self.calculate_experience_score(candidate_years_exp, required_years_exp)

        # 3. Project Relevance Score
        proj_score = self.calculate_project_score(candidate_projects or [], target_role)

        # 4. Certification Score
        cert_score = self.calculate_certification_score(certifications or [])

        # 5. ML Prediction Score (from baseline trained classifier or calibrated default)
        if ml_prediction_score is None:
            # Calibrated ensemble prior from skill & experience
            ml_pred = min(100.0, (skill_match_score * 0.7) + (exp_score * 0.3))
        else:
            ml_pred = ml_prediction_score * 100.0 if ml_prediction_score <= 1.0 else ml_prediction_score

        # Check Hidden Skill Gaps via Knowledge Graph
        missing_skill_names = [m["skill"] for m in skill_match_res["missing_skills"]]
        hidden_gaps = self.kg.detect_hidden_skill_gaps(candidate_skills, missing_skill_names)

        # Compute Fusion Score
        w_skill = weights.get("skill_match", 0.40)
        w_exp = weights.get("experience", 0.25)
        w_proj = weights.get("projects", 0.15)
        w_cert = weights.get("certifications", 0.10)
        w_ml = weights.get("ml_prediction", 0.10)

        # Weighted calculation
        job_fit_score = (
            (skill_match_score * w_skill) +
            (exp_score * w_exp) +
            (proj_score * w_proj) +
            (cert_score * w_cert) +
            (ml_pred * w_ml)
        )
        job_fit_score = round(max(0.0, min(100.0, job_fit_score)), 2)

        # Skill Gap % (adjusted for hidden blocker penalties)
        base_gap = max(0.0, 100.0 - skill_match_score)
        gap_penalty = min(15.0, len(hidden_gaps) * 3.0)
        skill_gap_percentage = round(min(100.0, base_gap + gap_penalty), 2)

        # Candidate Ranking Score (harmonic booster prioritizing high skill + experience balance)
        ranking_score = round(
            (job_fit_score * 0.75) + 
            (min(100.0, skill_match_score) * 0.15) + 
            (min(100.0, exp_score) * 0.10), 
            2
        )

        signal_breakdown = {
            "skill_match": {
                "raw_score": round(skill_match_score, 2),
                "weight": w_skill,
                "weighted_contribution": round(skill_match_score * w_skill, 2)
            },
            "experience": {
                "raw_score": round(exp_score, 2),
                "weight": w_exp,
                "weighted_contribution": round(exp_score * w_exp, 2)
            },
            "projects": {
                "raw_score": round(proj_score, 2),
                "weight": w_proj,
                "weighted_contribution": round(proj_score * w_proj, 2)
            },
            "certifications": {
                "raw_score": round(cert_score, 2),
                "weight": w_cert,
                "weighted_contribution": round(cert_score * w_cert, 2)
            },
            "ml_prediction": {
                "raw_score": round(ml_pred, 2),
                "weight": w_ml,
                "weighted_contribution": round(ml_pred * w_ml, 2)
            }
        }

        # Confidence level
        if job_fit_score >= 80:
            fit_tier = "Excellent Fit (Ready for Immediate Hire)"
            confidence = "High"
        elif job_fit_score >= 65:
            fit_tier = "Strong Candidate (Fast-track Upskilling Recommended)"
            confidence = "High"
        elif job_fit_score >= 50:
            fit_tier = "Moderate Potential (Targeted Learning Required)"
            confidence = "Medium"
        else:
            fit_tier = "Significant Gap (Requires Foundational Training)"
            confidence = "Medium-High"

        return {
            "job_fit_score": job_fit_score,
            "skill_gap_percentage": skill_gap_percentage,
            "candidate_ranking_score": ranking_score,
            "fit_tier": fit_tier,
            "confidence": confidence,
            "weights_used": weights,
            "signal_breakdown": signal_breakdown,
            "semantic_matching_details": skill_match_res,
            "hidden_skill_gaps": hidden_gaps,
            "target_role": target_role
        }

# Global instance
_hwef_instance = None

def get_hwef_engine() -> HWEFEngine:
    global _hwef_instance
    if _hwef_instance is None:
        _hwef_instance = HWEFEngine()
    return _hwef_instance
