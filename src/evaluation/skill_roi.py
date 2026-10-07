from typing import List, Dict, Any, Optional
from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.knowledge_graph.skill_graph import get_skill_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Standard default learning duration in weeks per skill
DEFAULT_LEARNING_WEEKS = {
    "Python": 4,
    "SQL": 3,
    "NumPy": 2,
    "Pandas": 3,
    "Scikit-Learn": 4,
    "Machine Learning": 6,
    "TensorFlow": 6,
    "PyTorch": 6,
    "Docker": 3,
    "Kubernetes": 5,
    "FastAPI": 3,
    "MLflow": 3,
    "MLOps": 5,
    "Transformers": 5,
    "LLMs": 6,
    "RAG Architectures": 4,
    "Prompt Engineering": 2,
    "Deep Learning": 6,
    "Computer Vision": 5,
    "NLP": 5,
    "Tableau": 3,
    "Power BI": 3,
    "Executive Storytelling": 2,
    "PySpark": 5,
    "ETL Pipelines": 4,
    "Data Warehousing": 4
}

class SkillROIEngine:
    """
    Skill Return-on-Investment (ROI) Calculation Engine.
    Formula:
        ROI = ScoreGain / LearningTime (weeks)
    Measures the efficiency of skill acquisition per unit of learning investment.
    """
    def __init__(self):
        self.cf_engine = get_counterfactual_engine()
        self.kg = get_skill_graph()

    def compute_skill_roi(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        target_role: str = "Machine Learning Engineer",
        candidate_years_exp: float = 3.0,
        required_years_exp: float = 4.0
    ) -> Dict[str, Any]:
        """
        Calculates and ranks skill interventions by ROI = DeltaScore / LearningWeeks.
        """
        # 1. Run counterfactual delta simulation
        sim = self.cf_engine.simulate_counterfactuals(
            candidate_skills=candidate_skills,
            required_skills=required_skills,
            candidate_years_exp=candidate_years_exp,
            required_years_exp=required_years_exp,
            target_role=target_role
        )

        single_recs = sim.get("top_single_skill_recommendations", [])
        ranked_roi = []

        for rec in single_recs:
            skill_name = rec["skill"]
            marginal_gain = float(rec["marginal_gain"])
            
            # Lookup learning time from knowledge graph or defaults
            if skill_name in self.kg.graph:
                learning_weeks = float(self.kg.graph.nodes[skill_name].get("time_weeks", 4))
            else:
                learning_weeks = float(DEFAULT_LEARNING_WEEKS.get(skill_name, 4))

            # ROI = ScoreGain / LearningTime
            roi_value = round(marginal_gain / max(learning_weeks, 1.0), 2)

            ranked_roi.append({
                "skill": skill_name,
                "score_gain": round(marginal_gain, 2),
                "learning_time_weeks": learning_weeks,
                "learning_time_hours": int(learning_weeks * 10),
                "roi_index": roi_value,
                "baseline_fit": rec.get("baseline_score", 0.0),
                "counterfactual_fit": rec.get("counterfactual_score", 0.0),
                "roi_tier": "High Efficiency (Fast Win)" if roi_value >= 2.0 else ("Moderate Efficiency" if roi_value >= 1.0 else "Strategic Investment")
            })

        # Rank descending by ROI
        ranked_roi.sort(key=lambda x: x["roi_index"], reverse=True)

        return {
            "target_role": target_role,
            "baseline_job_fit_score": sim.get("current_state", {}).get("current_job_fit_score", 0.0),
            "total_evaluated_skills": len(ranked_roi),
            "ranked_skill_roi": ranked_roi
        }

# Global Singleton
_ROI_ENGINE = None

def get_skill_roi_engine() -> SkillROIEngine:
    global _ROI_ENGINE
    if _ROI_ENGINE is None:
        _ROI_ENGINE = SkillROIEngine()
    return _ROI_ENGINE
