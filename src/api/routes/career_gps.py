from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from src.career_gps.career_gps_engine import get_career_gps_engine
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v2/career-gps",
    tags=["Career GPS & Shortest Path Navigation"]
)

class CareerGPSNavigateRequest(BaseModel):
    current_skills: List[str] = Field(
        default=["Python", "SQL"],
        description="Candidate current skills"
    )
    target_role: str = Field(
        default="AI Engineer",
        description="Target destination career role"
    )
    algorithm: str = Field(
        default="dijkstra",
        description="Optimization algorithm: 'dijkstra' or 'astar'"
    )

@router.post("/navigate")
def navigate_career_gps_endpoint(req: CareerGPSNavigateRequest):
    """
    Computes optimal shortest path traversal through the Knowledge Graph
    minimizing learning friction, difficulty, and time while maximizing salary boost.
    """
    gps = get_career_gps_engine()
    result = gps.navigate_career_path(
        current_skills=req.current_skills,
        target_role=req.target_role,
        algorithm=req.algorithm
    )
    return result

@router.get("/roles")
def get_available_career_roles():
    """Lists standard target career roles with compensation profiles."""
    from src.career_gps.career_gps_engine import CAREER_TARGET_PROFILES
    return {"roles": CAREER_TARGET_PROFILES}
