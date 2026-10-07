from typing import Dict, Any, Optional
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)

class WorkforceReadinessEngine:
    """
    Workforce Readiness Index (WRI) Calculation Engine.
    Formula:
        WRI = 0.30*Conscientiousness + 0.25*Openness + 0.20*Extraversion + 0.15*Agreeableness - 0.10*Neuroticism
    Normalized to standard 0 - 100 benchmark.
    """
    WEIGHTS = {
        "Conscientiousness": 0.30,
        "Openness": 0.25,
        "Extraversion": 0.20,
        "Agreeableness": 0.15,
        "Neuroticism": -0.10
    }

    def compute_wri(
        self,
        conscientiousness: float,
        openness: float,
        extraversion: float,
        agreeableness: float,
        neuroticism: float
    ) -> Dict[str, Any]:
        """
        Computes the Workforce Readiness Score from Big-Five personality traits.
        Assumes inputs on standard 0-10 or 0-100 scale; automatically normalizes to 0-100.
        """
        # If inputs are on 0-10 scale, scale to 0-100
        traits_raw = {
            "Conscientiousness": float(conscientiousness),
            "Openness": float(openness),
            "Extraversion": float(extraversion),
            "Agreeableness": float(agreeableness),
            "Neuroticism": float(neuroticism)
        }

        # Auto-detect if on 1-10 scale
        is_ten_scale = max(traits_raw.values()) <= 10.0
        traits_100 = {
            k: (v * 10.0 if is_ten_scale else v)
            for k, v in traits_raw.items()
        }

        # Apply standard WRI formula:
        # 0.30*C + 0.25*O + 0.20*E + 0.15*A - 0.10*N
        raw_wri = (
            (self.WEIGHTS["Conscientiousness"] * traits_100["Conscientiousness"]) +
            (self.WEIGHTS["Openness"] * traits_100["Openness"]) +
            (self.WEIGHTS["Extraversion"] * traits_100["Extraversion"]) +
            (self.WEIGHTS["Agreeableness"] * traits_100["Agreeableness"]) +
            (self.WEIGHTS["Neuroticism"] * traits_100["Neuroticism"])
        )

        # Theoretical min is -10 (if N=100 and others=0)
        # Theoretical max is +90 (if C=100, O=100, E=100, A=100, N=0)
        # Normalize strictly to 0 - 100 scale:
        # normalized = ((raw_wri - (-10)) / (90 - (-10))) * 100 = (raw_wri + 10)
        normalized_wri = float(np.clip(raw_wri + 10.0, 0.0, 100.0))
        final_score = round(normalized_wri, 2)

        # Readiness Tier Classification
        if final_score >= 80.0:
            tier = "Exceptional Workplace Readiness (Immediate Leadership / Autonomy)"
            status = "Ready"
        elif final_score >= 65.0:
            tier = "Solid Professional Readiness (Standard Team Deployment)"
            status = "Qualified"
        elif final_score >= 50.0:
            tier = "Developing Readiness (Mentorship & Structure Recommended)"
            status = "Developing"
        else:
            tier = "Foundational Readiness (Targeted Soft-Skills Coaching Required)"
            status = "Coaching Required"

        # Trait contributions breakdown
        contributions = {
            trait: round(self.WEIGHTS[trait] * traits_100[trait], 2)
            for trait in self.WEIGHTS
        }

        return {
            "workforce_readiness_score": final_score,
            "raw_wri_value": round(raw_wri, 2),
            "readiness_tier": tier,
            "readiness_status": status,
            "formula": "0.30*C + 0.25*O + 0.20*E + 0.15*A - 0.10*N",
            "trait_inputs_scaled_100": traits_100,
            "trait_weighted_contributions": contributions
        }

# Global Singleton
_WRI_ENGINE = None

def get_workforce_index_engine() -> WorkforceReadinessEngine:
    global _WRI_ENGINE
    if _WRI_ENGINE is None:
        _WRI_ENGINE = WorkforceReadinessEngine()
    return _WRI_ENGINE
