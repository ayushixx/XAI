import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple
import numpy as np
import pandas as pd
import joblib

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

from src.config.settings import ADVANCED_MODELS_DIR, MODELS_DIR, CLEANED_DIR
from src.config.hwef_config import load_weights, DEFAULT_WEIGHTS
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Standard model feature definitions
DEFAULT_JDS_FEATURES = [
    'big_data_skills',
    'maths-stats_skills',
    'coding_skills',
    'ai_and_ml_skills',
    'dashboard_and_storytelling_skills'
]

# Aliases to resolve candidate input dictionaries to model features
FEATURE_ALIASES = {
    'big_data': 'big_data_skills',
    'big_data_skills': 'big_data_skills',
    'maths': 'maths-stats_skills',
    'maths_stats': 'maths-stats_skills',
    'maths-stats_skills': 'maths-stats_skills',
    'coding': 'coding_skills',
    'coding_skills': 'coding_skills',
    'programming': 'coding_skills',
    'ai_ml': 'ai_and_ml_skills',
    'ai_and_ml': 'ai_and_ml_skills',
    'ai_and_ml_skills': 'ai_and_ml_skills',
    'ml': 'ai_and_ml_skills',
    'dashboard': 'dashboard_and_storytelling_skills',
    'dashboard_storytelling': 'dashboard_and_storytelling_skills',
    'dashboard_and_storytelling_skills': 'dashboard_and_storytelling_skills',
    'storytelling': 'dashboard_and_storytelling_skills',
    'bi_skills': 'dashboard_and_storytelling_skills'
}

class XAIService:
    """
    Explainable AI (XAI) Service integrating SHAP (SHapley Additive exPlanations)
    with TreeExplainer for gradient boosted models (XGBoost, LightGBM, CatBoost)
    and Hybrid Weighted Evaluation Fusion (HWEF) signal attribution.
    """
    _instance = None
    _explainer = None
    _model = None
    _expected_features = DEFAULT_JDS_FEATURES

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(XAIService, cls).__new__(cls)
            cls._instance._initialize_explainer()
        return cls._instance

    def _initialize_explainer(self):
        """Initializes global SHAP TreeExplainer by loading the primary gradient boosting model."""
        if not SHAP_AVAILABLE:
            logger.warning("SHAP library is not installed. Fallback rule-based XAI will be used.")
            return

        model_candidates = [
            ADVANCED_MODELS_DIR / 'jds' / 'xgboost.pkl',
            ADVANCED_MODELS_DIR / 'jds' / 'lightgbm.pkl',
            ADVANCED_MODELS_DIR / 'jds' / 'catboost.pkl',
            MODELS_DIR / 'jds' / 'random_forest.pkl'
        ]

        loaded_model = None
        for path in model_candidates:
            if path.exists():
                try:
                    loaded_model = joblib.load(path)
                    logger.info(f"XAI Service loaded model from {path}")
                    break
                except Exception as e:
                    logger.warning(f"Could not load model at {path}: {e}")

        if loaded_model is not None:
            self._model = loaded_model
            try:
                # Initialize TreeExplainer
                self._explainer = shap.TreeExplainer(self._model)
                logger.info("SHAP TreeExplainer initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize shap.TreeExplainer: {e}. Fallback enabled.")
                self._explainer = None

    def _align_features(self, input_features: Dict[str, Any]) -> pd.DataFrame:
        """
        Aligns the arbitrary input features dictionary to the exact columns and order
        expected by the trained ML model, applying alias mapping and default imputations.
        """
        aligned_dict = {}
        
        # Normalize input keys
        normalized_input = {}
        for k, v in input_features.items():
            clean_k = str(k).lower().strip()
            # Try float conversion
            try:
                val = float(v)
            except (ValueError, TypeError):
                val = 1.0 if bool(v) else 0.0
            normalized_input[clean_k] = val

        for target_col in self._expected_features:
            col_val = 0.0
            if target_col in normalized_input:
                col_val = normalized_input[target_col]
            else:
                # Check aliases
                found = False
                for alias_k, mapped_col in FEATURE_ALIASES.items():
                    if mapped_col == target_col and alias_k in normalized_input:
                        col_val = normalized_input[alias_k]
                        found = True
                        break
                if not found:
                    # Provide sensible normalized domain default (e.g. 5.0 on 0-10 scale or 0.5 on 0-1 scale)
                    col_val = 5.0

            aligned_dict[target_col] = [col_val]

        return pd.DataFrame(aligned_dict)

    def explain_candidate_score(
        self,
        candidate_features: Dict[str, Any],
        candidate_id: str = "candidate_001",
        candidate_name: str = "Candidate Evaluation",
        target_role: str = "Machine Learning Engineer",
        hwef_scores: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Computes SHAP values using TreeExplainer and creates a decoupled, UI-ready payload
        isolating base_value, final_prediction, feature_attributions, radar_chart, and waterfall.
        """
        try:
            # 1. Align features for ML model
            df_features = self._align_features(candidate_features)
            
            # 2. Check if SHAP explainer is active
            if self._explainer is not None and self._model is not None:
                shap_values_raw = self._explainer.shap_values(df_features)
                
                # Handle binary classification output formats (single array vs [class0, class1])
                if isinstance(shap_values_raw, list):
                    shap_vals = shap_values_raw[1][0] if len(shap_values_raw) > 1 else shap_values_raw[0][0]
                elif len(shap_values_raw.shape) == 3:
                    shap_vals = shap_values_raw[0, :, 1]
                elif len(shap_values_raw.shape) == 2:
                    shap_vals = shap_values_raw[0]
                else:
                    shap_vals = np.array(shap_values_raw).flatten()

                # Base expected value
                expected_val = self._explainer.expected_value
                if isinstance(expected_val, (list, np.ndarray)):
                    base_val = float(expected_val[1] if len(expected_val) > 1 else expected_val[0])
                else:
                    base_val = float(expected_val)

                # Raw model prediction probability
                if hasattr(self._model, 'predict_proba'):
                    prob = self._model.predict_proba(df_features)[0]
                    final_pred_prob = float(prob[1] if len(prob) > 1 else prob[0])
                else:
                    pred = self._model.predict(df_features)[0]
                    final_pred_prob = float(pred)

                # Format ML feature attributions
                ml_attributions = []
                total_abs_shap = sum(abs(float(v)) for v in shap_vals) or 1.0

                for col_name, raw_val, s_val in zip(self._expected_features, df_features.iloc[0], shap_vals):
                    s_float = float(s_val)
                    direction = "positive" if s_float > 0.005 else ("negative" if s_float < -0.005 else "neutral")
                    impact_pct = float(round((abs(s_float) / total_abs_shap) * 100.0, 2))
                    
                    human_label = col_name.replace('_', ' ').replace('-', ' / ').title()
                    ml_attributions.append({
                        "feature_name": human_label,
                        "raw_column": str(col_name),
                        "feature_value": float(round(raw_val, 2)),
                        "shap_value": float(round(s_float, 4)),
                        "impact_pct": impact_pct,
                        "direction": direction,
                        "description": f"{human_label} contributed {'+' if s_float >= 0 else ''}{round(s_float * 100, 1)}% to score"
                    })

                # Sort by absolute SHAP impact descending
                ml_attributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

            else:
                # Fallback to model-less SHAP estimation based on feature distance
                base_val, final_pred_prob, ml_attributions = self._compute_heuristic_shap(df_features)

            # 3. Integrate Multi-Modal HWEF Signal Attribution Layer
            weights = load_weights()
            hwef_attributions = self._build_hwef_attributions(candidate_features, weights, final_pred_prob)

            # Final Candidate Ranking Score (0-100 scale)
            final_ranking_score = float(round(hwef_attributions["overall_fit_score"], 2))

            # 4. Construct Radar Chart Payload
            radar_payload = {
                "categories": [attr["feature_name"] for attr in ml_attributions],
                "candidate_scores": [float(min(100.0, max(0.0, attr["feature_value"] * 10.0 if attr["feature_value"] <= 10.0 else attr["feature_value"]))) for attr in ml_attributions],
                "baseline_benchmark": [75.0] * len(ml_attributions),
                "shap_impacts": [attr["shap_value"] for attr in ml_attributions]
            }

            # 5. Construct Waterfall Chart Payload
            waterfall_steps = []
            running_val = base_val * 100.0
            waterfall_steps.append({
                "name": "Base Prior (E[f(x)])",
                "value": float(round(running_val, 2)),
                "running_total": float(round(running_val, 2)),
                "is_base": True
            })

            for item in ml_attributions:
                delta = float(item["shap_value"] * 100.0)
                running_val += delta
                waterfall_steps.append({
                    "name": item["feature_name"],
                    "value": float(round(delta, 2)),
                    "running_total": float(round(running_val, 2)),
                    "is_positive": delta >= 0
                })

            waterfall_payload = {
                "base_value": float(round(base_val * 100.0, 2)),
                "final_prediction": float(round(final_pred_prob * 100.0, 2)),
                "steps": waterfall_steps
            }

            # 6. Assemble Final Clean JSON Response
            response_payload = {
                "status": "success",
                "candidate_id": str(candidate_id),
                "candidate_name": str(candidate_name),
                "target_role": str(target_role),
                "base_value": float(round(base_val, 4)),
                "final_prediction": final_ranking_score,
                "ml_model_probability": float(round(final_pred_prob, 4)),
                "feature_attributions": {
                    item["raw_column"]: float(item["shap_value"]) for item in ml_attributions
                },
                "feature_attributions_detailed": ml_attributions,
                "hwef_multimodal_attribution": hwef_attributions,
                "radar_chart_payload": radar_payload,
                "waterfall_payload": waterfall_payload,
                "explainer_engine": "TreeExplainer" if self._explainer is not None else "HWEF-Calibrated-Fallback"
            }
            return response_payload

        except Exception as e:
            logger.error(f"XAI calculation error: {e}. Executing defensive fallback.", exc_info=True)
            return self._build_safe_fallback_response(candidate_id, candidate_name, target_role, candidate_features)

    def _compute_heuristic_shap(self, df_features: pd.DataFrame) -> Tuple[float, float, List[Dict[str, Any]]]:
        """Defensive fallback calculating calibrated additive attributions when SHAP model is absent."""
        base_val = 0.50
        row = df_features.iloc[0]
        attributions = []
        total_delta = 0.0

        for col in self._expected_features:
            val = float(row[col])
            norm_val = (val / 10.0) if val > 1.0 else val
            delta = float((norm_val - 0.5) * 0.20)
            total_delta += delta

            attributions.append({
                "feature_name": col.replace('_', ' ').replace('-', ' / ').title(),
                "raw_column": str(col),
                "feature_value": float(round(val, 2)),
                "shap_value": float(round(delta, 4)),
                "impact_pct": float(round(abs(delta) * 100.0, 2)),
                "direction": "positive" if delta > 0 else ("negative" if delta < 0 else "neutral"),
                "description": f"{col.title()} contribution: {'+' if delta >= 0 else ''}{round(delta * 100, 1)}%"
            })

        final_prob = float(min(1.0, max(0.0, base_val + total_delta)))
        return base_val, final_prob, attributions

    def _build_hwef_attributions(
        self,
        candidate_features: Dict[str, Any],
        weights: Dict[str, float],
        ml_prob: float
    ) -> Dict[str, Any]:
        """Constructs HWEF 5-signal explainability breakdown."""
        w_skill = float(weights.get("skill_match", 0.40))
        w_exp = float(weights.get("experience", 0.25))
        w_proj = float(weights.get("projects", 0.15))
        w_cert = float(weights.get("certifications", 0.10))
        w_ml = float(weights.get("ml_prediction", 0.10))

        s_skill = float(candidate_features.get("skill_match_score", candidate_features.get("skill_match", 78.0)))
        s_exp = float(candidate_features.get("experience_score", candidate_features.get("experience", 80.0)))
        s_proj = float(candidate_features.get("project_score", candidate_features.get("projects", 75.0)))
        s_cert = float(candidate_features.get("certification_score", candidate_features.get("certifications", 70.0)))
        s_ml = float(ml_prob * 100.0 if ml_prob <= 1.0 else ml_prob)

        overall_score = (
            (s_skill * w_skill) +
            (s_exp * w_exp) +
            (s_proj * w_proj) +
            (s_cert * w_cert) +
            (s_ml * w_ml)
        )

        signals = [
            {"signal": "Semantic Skill Match", "weight": w_skill, "score": s_skill, "contribution": round(s_skill * w_skill, 2)},
            {"signal": "Experience Alignment", "weight": w_exp, "score": s_exp, "contribution": round(s_exp * w_exp, 2)},
            {"signal": "Project Portfolio", "weight": w_proj, "score": s_proj, "contribution": round(s_proj * w_proj, 2)},
            {"signal": "Accredited Certifications", "weight": w_cert, "score": s_cert, "contribution": round(s_cert * w_cert, 2)},
            {"signal": "ML Classifier Prior", "weight": w_ml, "score": round(s_ml, 2), "contribution": round(s_ml * w_ml, 2)}
        ]

        return {
            "overall_fit_score": round(overall_score, 2),
            "signal_breakdown": signals
        }

    def _build_safe_fallback_response(
        self,
        candidate_id: str,
        candidate_name: str,
        target_role: str,
        candidate_features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ultimate fallback response preventing dashboard downtime."""
        weights = DEFAULT_WEIGHTS
        fallback_attrs = []
        for feat in DEFAULT_JDS_FEATURES:
            fallback_attrs.append({
                "feature_name": feat.replace('_', ' ').title(),
                "raw_column": str(feat),
                "feature_value": float(candidate_features.get(feat, 5.0)),
                "shap_value": 0.05,
                "impact_pct": 20.0,
                "direction": "positive",
                "description": f"Standard baseline weight for {feat}"
            })

        return {
            "status": "fallback",
            "candidate_id": str(candidate_id),
            "candidate_name": str(candidate_name),
            "target_role": str(target_role),
            "base_value": 0.50,
            "final_prediction": 75.0,
            "ml_model_probability": 0.75,
            "feature_attributions": {feat: 0.05 for feat in DEFAULT_JDS_FEATURES},
            "feature_attributions_detailed": fallback_attrs,
            "hwef_multimodal_attribution": {
                "overall_fit_score": 75.0,
                "signal_breakdown": [
                    {"signal": k, "weight": v, "score": 75.0, "contribution": round(75.0 * v, 2)}
                    for k, v in weights.items()
                ]
            },
            "radar_chart_payload": {
                "categories": [f.replace('_', ' ').title() for f in DEFAULT_JDS_FEATURES],
                "candidate_scores": [75.0] * len(DEFAULT_JDS_FEATURES),
                "baseline_benchmark": [70.0] * len(DEFAULT_JDS_FEATURES)
            },
            "waterfall_payload": {
                "base_value": 50.0,
                "final_prediction": 75.0,
                "steps": [
                    {"name": "Base Prior", "value": 50.0, "running_total": 50.0, "is_base": True},
                    {"name": "General Competence", "value": 25.0, "running_total": 75.0, "is_positive": True}
                ]
            },
            "explainer_engine": "Defensive-Static-HWEF-Fallback"
        }

# Global singleton helper
_xai_service_instance = None

def get_xai_service() -> XAIService:
    global _xai_service_instance
    if _xai_service_instance is None:
        _xai_service_instance = XAIService()
    return _xai_service_instance
