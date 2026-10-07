import json
from pathlib import Path
from typing import Dict
from src.config.settings import CONFIG_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

WEIGHTS_FILE = CONFIG_DIR / 'weights.json'

DEFAULT_WEIGHTS: Dict[str, float] = {
    "skill_match": 0.40,
    "experience": 0.25,
    "projects": 0.15,
    "certifications": 0.10,
    "ml_prediction": 0.10
}

def load_weights() -> Dict[str, float]:
    """Load HWEF fusion weights from config file or initialize with defaults."""
    if not WEIGHTS_FILE.exists():
        save_weights(DEFAULT_WEIGHTS)
        return DEFAULT_WEIGHTS.copy()
    try:
        with open(WEIGHTS_FILE, 'r', encoding='utf-8') as f:
            weights = json.load(f)
            # Ensure all keys exist
            for k, v in DEFAULT_WEIGHTS.items():
                if k not in weights:
                    weights[k] = v
            return weights
    except Exception as e:
        logger.warning(f"Error loading weights file, using defaults: {e}")
        return DEFAULT_WEIGHTS.copy()

def save_weights(weights: Dict[str, float]) -> bool:
    """Save HWEF fusion weights to json config file after normalization/validation."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        # Validate keys
        clean_weights = {}
        for k in DEFAULT_WEIGHTS.keys():
            val = float(weights.get(k, DEFAULT_WEIGHTS[k]))
            clean_weights[k] = max(0.0, min(1.0, val))
        
        # Normalize sum to 1.0 if not 0
        total = sum(clean_weights.values())
        if total > 0:
            clean_weights = {k: round(v / total, 4) for k, v in clean_weights.items()}
        
        with open(WEIGHTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(clean_weights, f, indent=4)
        logger.info(f"Updated HWEF weights: {clean_weights}")
        return True
    except Exception as e:
        logger.error(f"Failed to save weights: {e}")
        return False
