from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Path as FastPath, Body, HTTPException
from pydantic import BaseModel, Field

from src.services.xai_service import get_xai_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v2/xai",
    tags=["Explainable AI (SHAP)"]
)

# Request Models
class CandidateXAIRequest(BaseModel):
    candidate_name: Optional[str] = "Alex Chen"
    target_role: Optional[str] = "Senior Machine Learning Engineer"
    candidate_features: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {
            "coding_skills": 8.5,
            "ai_and_ml_skills": 9.0,
            "maths-stats_skills": 7.8,
            "big_data_skills": 7.0,
            "dashboard_and_storytelling_skills": 6.5,
            "skill_match_score": 88.0,
            "experience_score": 82.0,
            "project_score": 85.0,
            "certification_score": 75.0
        }
    )

class CandidateXAIResponse(BaseModel):
    status: str
    candidate_id: str
    candidate_name: str
    target_role: str
    base_value: float
    final_prediction: float
    ml_model_probability: float
    feature_attributions: Dict[str, float]
    feature_attributions_detailed: List[Dict[str, Any]]
    hwef_multimodal_attribution: Dict[str, Any]
    radar_chart_payload: Dict[str, Any]
    waterfall_payload: Dict[str, Any]
    explainer_engine: str

# Sample candidate repository for quick GET lookups
SAMPLE_CANDIDATES = {
    "candidate_001": {
        "candidate_name": "Alex Chen",
        "target_role": "Senior Machine Learning Engineer",
        "features": {
            "coding_skills": 8.5,
            "ai_and_ml_skills": 9.2,
            "maths-stats_skills": 8.0,
            "big_data_skills": 7.5,
            "dashboard_and_storytelling_skills": 6.8,
            "skill_match_score": 90.0,
            "experience_score": 85.0,
            "project_score": 88.0,
            "certification_score": 80.0
        }
    },
    "candidate_002": {
        "candidate_name": "Sarah Jenkins",
        "target_role": "Data Scientist",
        "features": {
            "coding_skills": 7.5,
            "ai_and_ml_skills": 7.0,
            "maths-stats_skills": 8.8,
            "big_data_skills": 6.0,
            "dashboard_and_storytelling_skills": 8.5,
            "skill_match_score": 80.0,
            "experience_score": 78.0,
            "project_score": 75.0,
            "certification_score": 70.0
        }
    },
    "candidate_003": {
        "candidate_name": "Vikram Mehta",
        "target_role": "MLOps Platform Engineer",
        "features": {
            "coding_skills": 9.0,
            "ai_and_ml_skills": 7.8,
            "maths-stats_skills": 6.5,
            "big_data_skills": 8.8,
            "dashboard_and_storytelling_skills": 6.0,
            "skill_match_score": 84.0,
            "experience_score": 82.0,
            "project_score": 86.0,
            "certification_score": 85.0
        }
    }
}

@router.get("/candidate/{candidate_id}", response_model=CandidateXAIResponse)
def get_candidate_xai(candidate_id: str = FastPath(..., description="Unique Candidate Identifier")):
    """
    Computes and returns SHAP TreeExplainer attributions and HWEF multimodal explainability
    for the specified candidate ID.
    """
    xai = get_xai_service()
    cand_info = SAMPLE_CANDIDATES.get(candidate_id, {
        "candidate_name": f"Candidate {candidate_id}",
        "target_role": "Data Science Specialist",
        "features": {
            "coding_skills": 7.0,
            "ai_and_ml_skills": 7.0,
            "maths-stats_skills": 7.0,
            "big_data_skills": 6.5,
            "dashboard_and_storytelling_skills": 7.0
        }
    })

    result = xai.explain_candidate_score(
        candidate_features=cand_info["features"],
        candidate_id=candidate_id,
        candidate_name=cand_info["candidate_name"],
        target_role=cand_info["target_role"]
    )
    return result

@router.post("/candidate/{candidate_id}", response_model=CandidateXAIResponse)
def post_candidate_xai(
    candidate_id: str = FastPath(..., description="Unique Candidate Identifier"),
    payload: CandidateXAIRequest = Body(...)
):
    """
    Computes custom SHAP TreeExplainer values and XAI radar/waterfall payloads
    for dynamically supplied candidate features.
    """
    xai = get_xai_service()
    features = payload.candidate_features or {}
    
    result = xai.explain_candidate_score(
        candidate_features=features,
        candidate_id=candidate_id,
        candidate_name=payload.candidate_name or f"Candidate {candidate_id}",
        target_role=payload.target_role or "AI Specialist"
    )
    return result
