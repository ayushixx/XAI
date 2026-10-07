import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from src.hwef.hwef_engine import get_hwef_engine
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.semantic_matching.semantic_engine import get_semantic_matcher
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ExplainabilityEngine:
    """
    Dedicated Explainability & Visualization Engine
    Generates structured telemetry for Radar Charts, Heatmaps, Skill Distributions,
    Readiness Gauges, and Feature Importance decompositions.
    """
    def __init__(self):
        self.hwef = get_hwef_engine()
        self.kg = get_knowledge_graph()
        self.matcher = get_semantic_matcher()

    def generate_candidate_explainability(
        self,
        candidate_name: str,
        candidate_skills: List[str],
        required_skills: List[str],
        candidate_years_exp: float = 3.0,
        required_years_exp: float = 3.0,
        projects: Optional[List[Dict[str, Any]]] = None,
        certifications: Optional[List[str]] = None,
        target_role: str = "Data Scientist"
    ) -> Dict[str, Any]:
        """
        Produces complete Explainable AI package for a candidate evaluation.
        """
        eval_result = self.hwef.evaluate_candidate(
            candidate_skills=candidate_skills,
            required_skills=required_skills,
            candidate_years_exp=candidate_years_exp,
            required_years_exp=required_years_exp,
            candidate_projects=projects,
            certifications=certifications,
            target_role=target_role
        )

        signal_bd = eval_result["signal_breakdown"]
        
        # 1. Radar Chart Data (Multi-dimensional signal profile)
        radar_chart = {
            "categories": [
                "Semantic Skill Match",
                "Domain Experience",
                "Project Complexity",
                "Certifications Tier",
                "Model Predictive Signal",
                "Prerequisite Foundation"
            ],
            "candidate_scores": [
                signal_bd["skill_match"]["raw_score"],
                signal_bd["experience"]["raw_score"],
                signal_bd["projects"]["raw_score"],
                signal_bd["certifications"]["raw_score"],
                signal_bd["ml_prediction"]["raw_score"],
                max(20.0, 100.0 - (len(eval_result["hidden_skill_gaps"]) * 15.0))
            ],
            "target_benchmark": [85.0, 80.0, 75.0, 70.0, 80.0, 90.0]
        }

        # 2. Skill Gap Heatmap Matrix (Candidate vs Required skills with similarity gradient)
        heatmap_matrix = []
        for req in required_skills:
            row_items = []
            for cand in candidate_skills:
                sim = self.matcher.compute_similarity(req, cand)
                row_items.append({
                    "candidate_skill": cand,
                    "required_skill": req,
                    "similarity": round(sim, 3),
                    "is_direct_match": sim >= 0.70
                })
            heatmap_matrix.append({
                "required_skill": req,
                "matches": row_items,
                "max_similarity": max([r["similarity"] for r in row_items], default=0.0)
            })

        # 3. Readiness Gauge & Confidence Calibration
        readiness_gauge = {
            "score": eval_result["job_fit_score"],
            "max_score": 100.0,
            "gap_percentage": eval_result["skill_gap_percentage"],
            "ranking_score": eval_result["candidate_ranking_score"],
            "fit_tier": eval_result["fit_tier"],
            "confidence_level": eval_result["confidence"],
            "gauge_color": (
                "#10b981" if eval_result["job_fit_score"] >= 75 else 
                ("#f59e0b" if eval_result["job_fit_score"] >= 55 else "#ef4444")
            )
        }

        # 4. Feature Importance Attribution (Weighted SHAP-style breakdown)
        weights_used = eval_result["weights_used"]
        feature_attribution = [
            {
                "feature": "Skill Match",
                "importance_weight": weights_used.get("skill_match", 0.40),
                "raw_score": signal_bd["skill_match"]["raw_score"],
                "impact_contribution": signal_bd["skill_match"]["weighted_contribution"],
                "status": "Positive Asset" if signal_bd["skill_match"]["raw_score"] >= 65 else "Primary Gap"
            },
            {
                "feature": "Experience Alignment",
                "importance_weight": weights_used.get("experience", 0.25),
                "raw_score": signal_bd["experience"]["raw_score"],
                "impact_contribution": signal_bd["experience"]["weighted_contribution"],
                "status": "Meets Threshold" if signal_bd["experience"]["raw_score"] >= 70 else "Under Requirement"
            },
            {
                "feature": "Project Portfolio",
                "importance_weight": weights_used.get("projects", 0.15),
                "raw_score": signal_bd["projects"]["raw_score"],
                "impact_contribution": signal_bd["projects"]["weighted_contribution"],
                "status": "Strong Portfolio" if signal_bd["projects"]["raw_score"] >= 70 else "Moderate Portfolio"
            },
            {
                "feature": "Accredited Certifications",
                "importance_weight": weights_used.get("certifications", 0.10),
                "raw_score": signal_bd["certifications"]["raw_score"],
                "impact_contribution": signal_bd["certifications"]["weighted_contribution"],
                "status": "Verified Credentials" if signal_bd["certifications"]["raw_score"] >= 60 else "No Major Certs"
            },
            {
                "feature": "ML Classifier Prior",
                "importance_weight": weights_used.get("ml_prediction", 0.10),
                "raw_score": signal_bd["ml_prediction"]["raw_score"],
                "impact_contribution": signal_bd["ml_prediction"]["weighted_contribution"],
                "status": "High Likelihood" if signal_bd["ml_prediction"]["raw_score"] >= 65 else "Moderate Likelihood"
            }
        ]

        # 5. Top Matching & Missing Skills Summary
        top_matching = [
            {"skill": m["required_skill"], "matched_with": m["matched_candidate_skill"], "score": m["similarity_score"]}
            for m in eval_result["semantic_matching_details"]["matched_skills"]
        ]
        top_missing = [
            {"skill": m["skill"], "partial_match": m.get("best_partial_match"), "partial_score": m.get("partial_similarity", 0)}
            for m in eval_result["semantic_matching_details"]["missing_skills"]
        ]

        return {
            "candidate_name": candidate_name,
            "target_role": target_role,
            "readiness_gauge": readiness_gauge,
            "radar_chart": radar_chart,
            "heatmap_matrix": heatmap_matrix,
            "feature_attribution": feature_attribution,
            "top_matching_skills": top_matching,
            "top_missing_skills": top_missing,
            "hidden_root_gaps": eval_result["hidden_skill_gaps"],
            "raw_evaluation": eval_result
        }

# Global singleton
_exp_instance = None

def get_explainability_engine() -> ExplainabilityEngine:
    global _exp_instance
    if _exp_instance is None:
        _exp_instance = ExplainabilityEngine()
    return _exp_instance
