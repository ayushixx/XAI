import numpy as np
from typing import Dict, Any, Optional, Tuple

import src.utils.env_setup
from src.evaluation.workforce_index import get_workforce_index_engine
from src.modeling.personality_autoencoder import get_personality_autoencoder
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PersonalityDigitalTwinEngine:
    """
    Personality Digital Twin & Behavioral What-If Simulation Engine.
    Simulates candidate behavioral evolution (e.g. +5 Conscientiousness, -5 Neuroticism),
    evaluates deep latent personality shifts, and predicts Future Workplace Success Probability.
    """
    def __init__(self):
        self.wri_engine = get_workforce_index_engine()
        self.autoencoder = get_personality_autoencoder()

    def simulate_digital_twin(
        self,
        candidate_name: str,
        current_traits: Dict[str, float],
        delta_conscientiousness: float = 5.0,
        delta_neuroticism: float = -5.0,
        delta_openness: float = 0.0,
        delta_extraversion: float = 0.0,
        delta_agreeableness: float = 0.0
    ) -> Dict[str, Any]:
        """
        Simulates current vs. future behavioral digital twin states:
        1. Current State: Baseline WRI score + 3D latent personality embedding.
        2. Intervention Simulation: +5 Conscientiousness, -5 Neuroticism (and optional deltas).
        3. Future State: Simulated WRI score + shifted 3D latent personality embedding.
        4. Predicts Future Success Probability and improvement delta.
        """
        # 1. Normalize current state traits (0-10 or 0-100 scale handling)
        c_traits = {
            "Conscientiousness": float(current_traits.get("Conscientiousness", current_traits.get("conscientiousness", 7.0))),
            "Openness": float(current_traits.get("Openness", current_traits.get("openness", 7.5))),
            "Extraversion": float(current_traits.get("Extraversion", current_traits.get("extraversion", 6.5))),
            "Agreeableness": float(current_traits.get("Agreeableness", current_traits.get("agreeableness", 7.0))),
            "Neuroticism": float(current_traits.get("Neuroticism", current_traits.get("neuroticism", 4.5)))
        }

        # Auto-detect scale (if on 0-10 scale, adapt delta from 0-10 or 0-100)
        is_ten_scale = max(c_traits.values()) <= 10.0
        delta_scale = 0.1 if is_ten_scale else 1.0

        # Current Evaluation
        curr_wri = self.wri_engine.compute_wri(
            conscientiousness=c_traits["Conscientiousness"],
            openness=c_traits["Openness"],
            extraversion=c_traits["Extraversion"],
            agreeableness=c_traits["Agreeableness"],
            neuroticism=c_traits["Neuroticism"]
        )

        curr_emb = self.autoencoder.encode_personality(
            candidate_id=f"{candidate_name}_current",
            traits=c_traits
        )

        # Baseline Success Probability calculation via sigmoid on normalized WRI
        # P(Success) = 1 / (1 + exp(- (WRI - 50) / 15))
        base_success_prob = round(1.0 / (1.0 + np.exp(-(curr_wri["workforce_readiness_score"] - 50.0) / 15.0)), 4)

        # 2. Simulate Future State with Interventions
        # (+5 Conscientiousness, -5 Neuroticism)
        max_bound = 10.0 if is_ten_scale else 100.0
        min_bound = 0.0

        f_traits = {
            "Conscientiousness": float(np.clip(c_traits["Conscientiousness"] + (delta_conscientiousness * delta_scale), min_bound, max_bound)),
            "Openness": float(np.clip(c_traits["Openness"] + (delta_openness * delta_scale), min_bound, max_bound)),
            "Extraversion": float(np.clip(c_traits["Extraversion"] + (delta_extraversion * delta_scale), min_bound, max_bound)),
            "Agreeableness": float(np.clip(c_traits["Agreeableness"] + (delta_agreeableness * delta_scale), min_bound, max_bound)),
            "Neuroticism": float(np.clip(c_traits["Neuroticism"] + (delta_neuroticism * delta_scale), min_bound, max_bound))
        }

        # Future Evaluation
        future_wri = self.wri_engine.compute_wri(
            conscientiousness=f_traits["Conscientiousness"],
            openness=f_traits["Openness"],
            extraversion=f_traits["Extraversion"],
            agreeableness=f_traits["Agreeableness"],
            neuroticism=f_traits["Neuroticism"]
        )

        future_emb = self.autoencoder.encode_personality(
            candidate_id=f"{candidate_name}_future",
            traits=f_traits
        )

        future_success_prob = round(1.0 / (1.0 + np.exp(-(future_wri["workforce_readiness_score"] - 50.0) / 15.0)), 4)

        # Score Improvement & Probability Gain
        score_diff = round(future_wri["workforce_readiness_score"] - curr_wri["workforce_readiness_score"], 2)
        prob_diff = round((future_success_prob - base_success_prob) * 100.0, 2)

        return {
            "candidate_name": candidate_name,
            "simulation_parameters": {
                "delta_conscientiousness": f"+{delta_conscientiousness}",
                "delta_neuroticism": f"{delta_neuroticism}"
            },
            "current_state": {
                "personality_traits": {k: round(v, 2) for k, v in c_traits.items()},
                "current_score": curr_wri["workforce_readiness_score"],
                "readiness_tier": curr_wri["readiness_tier"],
                "latent_personality_vector": curr_emb["latent_personality_vector"],
                "baseline_success_probability": round(base_success_prob * 100.0, 2)
            },
            "future_state": {
                "personality_traits": {k: round(v, 2) for k, v in f_traits.items()},
                "future_score": future_wri["workforce_readiness_score"],
                "readiness_tier": future_wri["readiness_tier"],
                "latent_personality_vector": future_emb["latent_personality_vector"],
                "future_success_probability": round(future_success_prob * 100.0, 2)
            },
            "improvement": {
                "score_improvement": f"+{score_diff}%" if score_diff >= 0 else f"{score_diff}%",
                "score_delta_numeric": score_diff,
                "success_probability_gain": f"+{prob_diff}%" if prob_diff >= 0 else f"{prob_diff}%",
                "behavioral_summary": (
                    f"Strengthening Conscientiousness (+{delta_conscientiousness}) and reducing Neuroticism/Stress Sensitivity ({delta_neuroticism}) "
                    f"boosts Workforce Readiness by +{score_diff} points and increases career success probability by +{prob_diff}%."
                )
            }
        }

# Global Singleton
_DIGITAL_TWIN_ENGINE = None

def get_digital_twin_engine() -> PersonalityDigitalTwinEngine:
    global _DIGITAL_TWIN_ENGINE
    if _DIGITAL_TWIN_ENGINE is None:
        _DIGITAL_TWIN_ENGINE = PersonalityDigitalTwinEngine()
    return _DIGITAL_TWIN_ENGINE
