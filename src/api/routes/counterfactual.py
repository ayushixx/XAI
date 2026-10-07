from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from src.counterfactual.counterfactual_engine import get_counterfactual_engine
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v2/counterfactual",
    tags=["Counterfactual Skill Recommendations"]
)

class CounterfactualSimulateRequest(BaseModel):
    candidate_skills: List[str] = Field(
        default=["Python", "SQL", "Pandas", "Scikit-Learn"],
        description="Candidate current skill set"
    )
    required_skills: Optional[List[str]] = Field(
        default=["Python", "SQL", "TensorFlow", "Docker", "MLOps", "FastAPI"],
        description="Job role required skill set"
    )
    candidate_years_exp: float = 3.0
    required_years_exp: float = 3.0
    target_role: str = "Senior Machine Learning Engineer"
    max_combo_size: int = 2

@router.post("/simulate")
def simulate_counterfactuals_endpoint(req: CounterfactualSimulateRequest):
    """
    Executes counterfactual simulation:
    ΔScore = f(X') - f(X)
    Returns single skill marginal gains, synergistic multi-skill combinations,
    optimal minimal bundle, and why-recommended explainability rationales.
    """
    engine = get_counterfactual_engine()
    result = engine.simulate_counterfactuals(
        candidate_skills=req.candidate_skills,
        required_skills=req.required_skills or ["Python", "SQL", "TensorFlow", "Docker", "MLOps"],
        candidate_years_exp=req.candidate_years_exp,
        required_years_exp=req.required_years_exp,
        target_role=req.target_role,
        max_combo_size=req.max_combo_size
    )
    return result
