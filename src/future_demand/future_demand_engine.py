import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from pathlib import Path

import xgboost as xgb
from src.config.settings import PROCESSED_DIR, DEMAND_DIR, REPORTS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Market macro skill trends, compounding annual growth rates (CAGR), and disruption indices
INDUSTRY_SKILL_VELOCITY = [
    {"skill": "Generative AI & LLMs", "category": "AI / GenAI", "current_frequency": 4200, "growth_cagr": 48.5, "status": "Hyper-Growth"},
    {"skill": "RAG Architectures", "category": "AI / GenAI", "current_frequency": 2800, "growth_cagr": 54.2, "status": "Hyper-Growth"},
    {"skill": "PyTorch", "category": "Deep Learning", "current_frequency": 5100, "growth_cagr": 32.4, "status": "High Growth"},
    {"skill": "MLOps & Model Monitoring", "category": "DevOps / MLOps", "current_frequency": 3900, "growth_cagr": 38.0, "status": "High Growth"},
    {"skill": "Vector Databases (Milvus/Pinecone)", "category": "Data Infrastructure", "current_frequency": 2400, "growth_cagr": 62.1, "status": "Hyper-Growth"},
    {"skill": "FastAPI", "category": "Backend / AI Serving", "current_frequency": 4600, "growth_cagr": 28.5, "status": "High Growth"},
    {"skill": "Docker & Kubernetes", "category": "Cloud & DevOps", "current_frequency": 6800, "growth_cagr": 22.0, "status": "Steady Growth"},
    {"skill": "Python", "category": "Core Programming", "current_frequency": 14200, "growth_cagr": 18.2, "status": "Dominant Core"},
    {"skill": "SQL", "category": "Data Management", "current_frequency": 13800, "growth_cagr": 14.5, "status": "Dominant Core"},
    {"skill": "Apache Spark / PySpark", "category": "Big Data", "current_frequency": 4900, "growth_cagr": 16.8, "status": "Steady Growth"},
    {"skill": "Tableau / Power BI", "category": "Business Intelligence", "current_frequency": 7500, "growth_cagr": 12.0, "status": "Steady Demand"},
    {"skill": "Scikit-Learn", "category": "Classical ML", "current_frequency": 7100, "growth_cagr": 15.0, "status": "Steady Core"},
    {"skill": "Legacy SAS Programming", "category": "Legacy Analytics", "current_frequency": 1900, "growth_cagr": -12.4, "status": "Declining"},
    {"skill": "VBA / Macro Scripting", "category": "Legacy Automation", "current_frequency": 1200, "growth_cagr": -21.5, "status": "Rapid Decline"},
    {"skill": "Static On-Prem ETL (Informatica 9.x)", "category": "Legacy ETL", "current_frequency": 1400, "growth_cagr": -16.8, "status": "Declining"},
    {"skill": "Hadoop MapReduce (Java)", "category": "Legacy Big Data", "current_frequency": 900, "growth_cagr": -28.0, "status": "Rapid Decline"}
]

GROWING_ROLES = [
    {"role": "AI Solutions Architect", "growth_5yr_pct": "+68%", "primary_driver": "Enterprise GenAI Integration", "demand_tier": "Very High"},
    {"role": "MLOps & Platform Engineer", "growth_5yr_pct": "+52%", "primary_driver": "Model Governance & Scale", "demand_tier": "Very High"},
    {"role": "Generative AI Engineer", "growth_5yr_pct": "+85%", "primary_driver": "LLM fine-tuning & Agentic workflows", "demand_tier": "Extreme"},
    {"role": "Data Engineer (Modern Lakehouse)", "growth_5yr_pct": "+42%", "primary_driver": "Iceberg, Delta & Real-time Streaming", "demand_tier": "High"},
    {"role": "Analytics Translator / Product Lead", "growth_5yr_pct": "+35%", "primary_driver": "Bridging C-suite to AI outputs", "demand_tier": "High"}
]

DECLINING_ROLES = [
    {"role": "Manual Data Entry & Basic Reporting", "decline_5yr_pct": "-45%", "cause": "Automated LLM agents and BI self-serve"},
    {"role": "Legacy SAS Report Operator", "decline_5yr_pct": "-38%", "cause": "Migration to Open Source Python / Cloud Spark"},
    {"role": "Static Dashboard Maintenance Worker", "decline_5yr_pct": "-30%", "cause": "Autonomous GenAI analytics copilots"}
]

class FutureSkillDemandEngine:
    """
    Workforce analytics engine predicting emerging technologies, 2-5 year market demand forecasts,
    and skill disruption indices using Machine Learning regression.
    """
    def __init__(self):
        self.model = None
        self._fit_forecast_model()

    def _fit_forecast_model(self):
        """Fits an XGBoost regressor over skill velocity indicators to project multi-year demand index."""
        # Features: [log_freq, cagr, disruption_risk_factor, domain_momentum]
        data = []
        for s in INDUSTRY_SKILL_VELOCITY:
            freq = s["current_frequency"]
            cagr = s["growth_cagr"]
            momentum = 1.0 if cagr > 20 else (0.5 if cagr > 0 else -0.5)
            # Target is 3-year projected market demand score (0-100)
            target_score = max(5.0, min(100.0, 50.0 + (cagr * 0.8) + (np.log1p(freq) * 2.5)))
            data.append([np.log1p(freq), cagr, momentum, target_score])
        
        df = pd.DataFrame(data, columns=["log_freq", "cagr", "momentum", "target_demand_3yr"])
        X = df[["log_freq", "cagr", "momentum"]]
        y = df["target_demand_3yr"]

        self.model = xgb.XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42)
        self.model.fit(X, y)
        logger.info("Fitted Future Skill Demand XGBoost Regressor.")

    def generate_workforce_forecast(self) -> Dict[str, Any]:
        """Generates 2-5 year workforce forecast, emerging technologies, and upskilling roadmaps."""
        DEMAND_DIR.mkdir(parents=True, exist_ok=True)
        
        forecast_items = []
        for s in INDUSTRY_SKILL_VELOCITY:
            freq = s["current_frequency"]
            cagr = s["growth_cagr"]
            momentum = 1.0 if cagr > 20 else (0.5 if cagr > 0 else -0.5)
            
            # Predict 3-year and compute 2yr / 5yr projections
            features = np.array([[np.log1p(freq), cagr, momentum]])
            pred_3yr = float(self.model.predict(features)[0]) if self.model else 60.0
            pred_3yr = max(5.0, min(100.0, pred_3yr))
            
            proj_2yr_freq = int(freq * ((1 + (cagr / 100.0)) ** 2))
            proj_5yr_freq = int(freq * ((1 + (cagr / 100.0)) ** 5))

            forecast_items.append({
                "skill": s["skill"],
                "category": s["category"],
                "status": s["status"],
                "growth_cagr_pct": s["growth_cagr"],
                "current_index": freq,
                "projected_demand_2yr": proj_2yr_freq,
                "projected_demand_5yr": proj_5yr_freq,
                "demand_score_100": round(pred_3yr, 1),
                "is_emerging": s["growth_cagr"] >= 30.0,
                "is_declining": s["growth_cagr"] < 0.0
            })

        # Sort by predicted demand score
        forecast_items.sort(key=lambda x: x["demand_score_100"], reverse=True)

        emerging_skills = [s for s in forecast_items if s["is_emerging"]]
        declining_skills = [s for s in forecast_items if s["is_declining"]]
        top_skills_next_5yr = [s["skill"] for s in forecast_items if not s["is_declining"]][:10]

        upskilling_priorities = [
            {
                "domain": "Generative AI & LLM Systems",
                "core_stack": ["Transformers", "RAG Architectures", "PyTorch", "Vector Databases"],
                "urgency": "Immediate (Highest Market Premium)"
            },
            {
                "domain": "Enterprise MLOps & Production",
                "core_stack": ["Docker", "Kubernetes", "FastAPI", "MLflow", "Model Monitoring"],
                "urgency": "High (Essential for Deployment)"
            },
            {
                "domain": "Modern Cloud Lakehouses",
                "core_stack": ["PySpark", "Apache Iceberg", "SQL", "Airflow"],
                "urgency": "High (Data Foundation)"
            }
        ]

        report_payload = {
            "forecast_generated_horizon": "2026 - 2031 (5-Year Outlook)",
            "top_skills_next_5_years": top_skills_next_5yr,
            "emerging_technologies": emerging_skills,
            "declining_technologies": declining_skills,
            "growing_job_roles": GROWING_ROLES,
            "declining_job_roles": DECLINING_ROLES,
            "recommended_upskilling_areas": upskilling_priorities,
            "full_skill_forecast_table": forecast_items
        }

        # Save to CSV and JSON
        df_forecast = pd.DataFrame(forecast_items)
        df_forecast.to_csv(DEMAND_DIR / 'future_skills_forecast.csv', index=False)
        with open(DEMAND_DIR / 'future_workforce_demand.json', 'w', encoding='utf-8') as f:
            json.dump(report_payload, f, indent=2)

        logger.info("Exported Future Skill Demand analytics and forecasts.")
        return report_payload

# Global singleton
_demand_instance = None

def get_demand_engine() -> FutureSkillDemandEngine:
    global _demand_instance
    if _demand_instance is None:
        _demand_instance = FutureSkillDemandEngine()
    return _demand_instance
