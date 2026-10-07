import json
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

from src.config.hwef_config import load_weights, save_weights, DEFAULT_WEIGHTS
from src.hwef.hwef_engine import get_hwef_engine
from src.semantic_matching.semantic_engine import get_semantic_matcher
from src.knowledge_graph.graph_engine import get_knowledge_graph
from src.roadmap.roadmap_engine import get_roadmap_engine
from src.future_demand.future_demand_engine import get_demand_engine
from src.advanced_modeling.advanced_models import run_advanced_modeling
from src.evaluation.explainability_engine import get_explainability_engine
from src.config.settings import BASE_DIR, REPORTS_DIR
from src.utils.logger import get_logger

from src.api.routes.xai import router as xai_router

logger = get_logger(__name__)

app = FastAPI(
    title="8BIT Workforce Skill Gap Analysis & AI Talent Intelligence Suite",
    description="Enterprise-grade Skill Gap Discovery, Knowledge Graph, Semantic Matching, HWEF, and Learning Roadmap APIs.",
    version="2.0.0"
)

# Enable CORS for modern web dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Modular Feature Routers
app.include_router(xai_router)


# ----------------- Request Models -----------------

class WeightsUpdateRequest(BaseModel):
    skill_match: float = Field(0.40, ge=0.0, le=1.0)
    experience: float = Field(0.25, ge=0.0, le=1.0)
    projects: float = Field(0.15, ge=0.0, le=1.0)
    certifications: float = Field(0.10, ge=0.0, le=1.0)
    ml_prediction: float = Field(0.10, ge=0.0, le=1.0)

class CandidateEvalRequest(BaseModel):
    candidate_name: str = "Alex Chen"
    candidate_skills: List[str] = ["Python", "SQL", "Pandas", "Scikit-Learn", "Tableau", "Git"]
    required_skills: List[str] = ["Python", "SQL", "TensorFlow", "Docker", "MLOps", "FastAPI"]
    candidate_years_exp: float = 3.5
    required_years_exp: float = 4.0
    candidate_projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[str]] = ["AWS Certified Cloud Practitioner"]
    ml_prediction_score: Optional[float] = None
    target_role: str = "Senior Machine Learning Engineer"

class BatchRankRequest(BaseModel):
    candidates: List[CandidateEvalRequest]
    required_skills: List[str]
    target_role: str = "Data Scientist"
    required_years_exp: float = 3.0

class SemanticMatchRequest(BaseModel):
    candidate_skills: List[str]
    required_skills: List[str]
    threshold: Optional[float] = 0.65

class RoadmapRequest(BaseModel):
    candidate_skills: List[str]
    target_role: str
    target_role_skills: List[str]
    hours_per_week: int = 10

class CareerPathRequest(BaseModel):
    start_skill_or_role: str
    target_skill_or_role: str

class HiddenGapRequest(BaseModel):
    candidate_skills: List[str]
    target_skills: List[str]

# ----------------- API Endpoints -----------------

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "8BIT Skill Gap Analysis & AI Talent Intelligence Suite",
        "version": "2.0.0",
        "engines": {
            "hwef": "active",
            "semantic_nlp": "active",
            "knowledge_graph": "active",
            "roadmap_engine": "active",
            "future_demand_engine": "active",
            "advanced_models": "active"
        }
    }

# 1. HWEF Fusion & Weights
@app.get("/api/hwef/weights")
def get_fusion_weights():
    return {"weights": load_weights(), "defaults": DEFAULT_WEIGHTS}

@app.post("/api/hwef/weights")
def update_fusion_weights(req: WeightsUpdateRequest):
    success = save_weights(req.model_dump())
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save weights.")
    return {"message": "Weights updated successfully", "weights": load_weights()}

@app.post("/api/hwef/evaluate")
def evaluate_single_candidate(req: CandidateEvalRequest):
    hwef = get_hwef_engine()
    result = hwef.evaluate_candidate(
        candidate_skills=req.candidate_skills,
        required_skills=req.required_skills,
        candidate_years_exp=req.candidate_years_exp,
        required_years_exp=req.required_years_exp,
        candidate_projects=req.candidate_projects,
        certifications=req.certifications,
        ml_prediction_score=req.ml_prediction_score,
        target_role=req.target_role
    )
    return {"candidate_name": req.candidate_name, "evaluation": result}

@app.post("/api/candidates/rank")
def rank_candidates(req: BatchRankRequest):
    hwef = get_hwef_engine()
    ranked_list = []
    for cand in req.candidates:
        res = hwef.evaluate_candidate(
            candidate_skills=cand.candidate_skills,
            required_skills=req.required_skills,
            candidate_years_exp=cand.candidate_years_exp,
            required_years_exp=req.required_years_exp,
            candidate_projects=cand.candidate_projects,
            certifications=cand.certifications,
            ml_prediction_score=cand.ml_prediction_score,
            target_role=req.target_role
        )
        ranked_list.append({
            "candidate_name": cand.candidate_name,
            "job_fit_score": res["job_fit_score"],
            "skill_gap_percentage": res["skill_gap_percentage"],
            "candidate_ranking_score": res["candidate_ranking_score"],
            "fit_tier": res["fit_tier"],
            "confidence": res["confidence"],
            "years_experience": cand.candidate_years_exp,
            "matched_skills_count": len(res["semantic_matching_details"]["matched_skills"]),
            "missing_skills_count": len(res["semantic_matching_details"]["missing_skills"]),
            "hidden_gaps_count": len(res["hidden_skill_gaps"]),
            "full_evaluation": res
        })
    # Sort by candidate ranking score descending
    ranked_list.sort(key=lambda x: x["candidate_ranking_score"], reverse=True)
    for idx, item in enumerate(ranked_list):
        item["rank"] = idx + 1
    return {
        "target_role": req.target_role,
        "total_candidates": len(ranked_list),
        "rankings": ranked_list
    }

# 2. Semantic Matching
@app.post("/api/semantic/match")
def match_skills_endpoint(req: SemanticMatchRequest):
    matcher = get_semantic_matcher()
    result = matcher.match_skills(
        candidate_skills=req.candidate_skills,
        required_skills=req.required_skills,
        custom_threshold=req.threshold
    )
    return result

# 3. Knowledge Graph
@app.get("/api/knowledge-graph/data")
def get_kg_data():
    kg = get_knowledge_graph()
    return kg.to_dict()

@app.get("/api/knowledge-graph/dependencies/{skill}")
def get_skill_dependencies_endpoint(skill: str):
    kg = get_knowledge_graph()
    return kg.get_skill_dependencies(skill)

@app.post("/api/knowledge-graph/gaps")
def detect_hidden_gaps_endpoint(req: HiddenGapRequest):
    kg = get_knowledge_graph()
    gaps = kg.detect_hidden_skill_gaps(req.candidate_skills, req.target_skills)
    return {"hidden_skill_gaps": gaps, "total_blockers": len(gaps)}

@app.post("/api/knowledge-graph/path")
def discover_career_path_endpoint(req: CareerPathRequest):
    kg = get_knowledge_graph()
    return kg.discover_career_path(req.start_skill_or_role, req.target_skill_or_role)

@app.get("/api/knowledge-graph/recommendations")
def recommend_next_skills_endpoint(skills: str):
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    kg = get_knowledge_graph()
    return {"recommendations": kg.recommend_next_skills(skill_list)}

# 4. Learning Roadmap
@app.post("/api/roadmap/generate")
def generate_roadmap_endpoint(req: RoadmapRequest):
    rm = get_roadmap_engine()
    return rm.generate_roadmap(
        candidate_skills=req.candidate_skills,
        target_role=req.target_role,
        target_role_skills=req.target_role_skills,
        hours_per_week=req.hours_per_week
    )

# 5. Explainable AI
@app.post("/api/explainability/candidate")
def explain_candidate_endpoint(req: CandidateEvalRequest):
    exp = get_explainability_engine()
    return exp.generate_candidate_explainability(
        candidate_name=req.candidate_name,
        candidate_skills=req.candidate_skills,
        required_skills=req.required_skills,
        candidate_years_exp=req.candidate_years_exp,
        required_years_exp=req.required_years_exp,
        projects=req.candidate_projects,
        certifications=req.certifications,
        target_role=req.target_role
    )

# 6. Future Skill Demand
@app.get("/api/future-skills/forecast")
def get_future_skills_forecast():
    demand = get_demand_engine()
    return demand.generate_workforce_forecast()

# 7. Advanced Modeling Benchmark
@app.get("/api/models/benchmark")
def get_model_benchmark():
    comp_file_jds = REPORTS_DIR / 'models' / 'jds_advanced_model_comparison.csv'
    comp_file_sds = REPORTS_DIR / 'models' / 'sds_advanced_model_comparison.csv'
    
    if not comp_file_jds.exists() or not comp_file_sds.exists():
        # Trigger training if not yet created
        run_advanced_modeling()
        
    jds_df = pd.read_csv(comp_file_jds) if comp_file_jds.exists() else pd.DataFrame()
    sds_df = pd.read_csv(comp_file_sds) if comp_file_sds.exists() else pd.DataFrame()

    fi_file = REPORTS_DIR / 'models' / 'jds_advanced_feature_importance.csv'
    fi_df = pd.read_csv(fi_file) if fi_file.exists() else pd.DataFrame()

    return {
        "jds_models": jds_df.to_dict(orient="records"),
        "sds_models": sds_df.to_dict(orient="records"),
        "feature_importances": fi_df.to_dict(orient="records")
    }

# ----------------- Serve Web Dashboard -----------------
DASHBOARD_DIR = BASE_DIR / 'src' / 'dashboard'
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

if (DASHBOARD_DIR / 'static').exists():
    app.mount("/static", StaticFiles(directory=str(DASHBOARD_DIR / 'static')), name="static")

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    index_path = DASHBOARD_DIR / 'index.html'
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>8BIT Skill Gap Analysis Dashboard is starting...</h1>"
