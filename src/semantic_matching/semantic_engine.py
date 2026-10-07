import os
import pickle
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
from src.config.settings import CACHE_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

EMBEDDINGS_CACHE_FILE = CACHE_DIR / 'skill_embeddings_cache.pkl'

# Known domain synonyms and mappings for rapid lookup and high-fidelity calibration
DOMAIN_SYNONYMS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "ai": "artificial intelligence",
    "tableau": "data visualization power bi",
    "power bi": "data visualization tableau",
    "powerbi": "data visualization power bi",
    "gcp": "google cloud platform",
    "aws": "amazon web services cloud computing",
    "azure": "microsoft azure cloud computing",
    "k8s": "kubernetes container orchestration",
    "docker": "containerization docker",
    "llm": "large language models generative ai",
    "genai": "generative artificial intelligence",
    "scikit-learn": "machine learning sklearn",
    "sklearn": "machine learning scikit-learn",
    "tf": "tensorflow deep learning",
    "neural networks": "deep learning neural networks"
}

class SemanticSkillMatcher:
    """
    Production-grade Semantic Skill Matching Engine using Sentence-Transformers (all-MiniLM-L6-v2)
    with embedding caching, cosine similarity matrix computation, and fuzzy semantic mapping.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", threshold: float = 0.65):
        self.model_name = model_name
        self.threshold = threshold
        self.model = None
        self._cache: Dict[str, np.ndarray] = {}
        self._load_cache()

    def _load_cache(self):
        """Loads cached embeddings from disk."""
        if EMBEDDINGS_CACHE_FILE.exists():
            try:
                with open(EMBEDDINGS_CACHE_FILE, 'rb') as f:
                    self._cache = pickle.load(f)
                logger.info(f"Loaded {len(self._cache)} cached skill embeddings.")
            except Exception as e:
                logger.warning(f"Failed to load embeddings cache: {e}")
                self._cache = {}

    def _save_cache(self):
        """Saves cached embeddings to disk."""
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            with open(EMBEDDINGS_CACHE_FILE, 'wb') as f:
                pickle.dump(self._cache, f)
        except Exception as e:
            logger.warning(f"Failed to save embeddings cache: {e}")

    def _get_model(self):
        """Lazy load SentenceTransformer model."""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading sentence-transformers model '{self.model_name}'...")
                self.model = SentenceTransformer(self.model_name)
                logger.info("SentenceTransformer loaded successfully.")
            except Exception as e:
                logger.warning(f"SentenceTransformer load fallback: {e}. Using deterministic tf-idf/n-gram encoder.")
                self.model = "FALLBACK"
        return self.model

    def encode(self, text: str) -> np.ndarray:
        """Encodes a skill string into a normalized dense vector."""
        clean_text = text.strip().lower()
        if not clean_text:
            return np.zeros(384)

        # Check in cache
        if clean_text in self._cache:
            return self._cache[clean_text]

        model = self._get_model()
        if model != "FALLBACK" and hasattr(model, 'encode'):
            try:
                # Augment synonym context if present
                augmented = clean_text
                if clean_text in DOMAIN_SYNONYMS:
                    augmented = f"{clean_text} ({DOMAIN_SYNONYMS[clean_text]})"
                vec = model.encode(augmented, convert_to_numpy=True, normalize_embeddings=True)
                self._cache[clean_text] = vec
                return vec
            except Exception as e:
                logger.warning(f"Error encoding with model: {e}")

        # High-dimensional deterministic feature hashing fallback
        vec = np.zeros(384)
        for i, char in enumerate(clean_text):
            vec[(ord(char) * 17 + i * 31) % 384] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        self._cache[clean_text] = vec
        return vec

    def compute_similarity(self, skill_a: str, skill_b: str) -> float:
        """Computes cosine similarity between two skill strings."""
        a_clean = skill_a.strip().lower()
        b_clean = skill_b.strip().lower()

        if a_clean == b_clean:
            return 1.0

        # Exact match in synonyms
        if DOMAIN_SYNONYMS.get(a_clean) == b_clean or DOMAIN_SYNONYMS.get(b_clean) == a_clean:
            return 0.95

        vec_a = self.encode(a_clean)
        vec_b = self.encode(b_clean)

        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    def match_skills(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        custom_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Performs bipartite semantic matching between candidate skills and job requirements.
        Returns:
            - semantic_similarity_score: float (0.0 to 1.0)
            - matched_skills: List of dicts with match details
            - missing_skills: List of required skills not met
            - related_skills: Candidate skills that offer adjacent synergy
        """
        threshold = custom_threshold if custom_threshold is not None else self.threshold

        clean_candidate = [s.strip() for s in candidate_skills if s and s.strip()]
        clean_required = [s.strip() for s in required_skills if s and s.strip()]

        if not clean_required:
            return {
                "semantic_similarity_score": 1.0,
                "matched_skills": [],
                "missing_skills": [],
                "related_skills": clean_candidate,
                "total_required": 0,
                "total_candidate": len(clean_candidate),
                "match_rate_pct": 100.0
            }

        if not clean_candidate:
            return {
                "semantic_similarity_score": 0.0,
                "matched_skills": [],
                "missing_skills": clean_required,
                "related_skills": [],
                "total_required": len(clean_required),
                "total_candidate": 0,
                "match_rate_pct": 0.0
            }

        # Compute similarity matrix
        sim_matrix = np.zeros((len(clean_required), len(clean_candidate)))
        for i, req in enumerate(clean_required):
            for j, cand in enumerate(clean_candidate):
                sim_matrix[i, j] = self.compute_similarity(req, cand)

        matched_skills = []
        missing_skills = []
        matched_candidate_indices = set()

        total_match_score = 0.0

        for i, req in enumerate(clean_required):
            best_cand_idx = int(np.argmax(sim_matrix[i]))
            best_score = float(sim_matrix[i, best_cand_idx])
            best_cand = clean_candidate[best_cand_idx]

            if best_score >= threshold:
                match_type = "Exact Match" if best_score >= 0.95 else ("High Semantic Match" if best_score >= 0.80 else "Moderate Match")
                matched_skills.append({
                    "required_skill": req,
                    "matched_candidate_skill": best_cand,
                    "similarity_score": round(best_score, 3),
                    "match_type": match_type
                })
                matched_candidate_indices.add(best_cand_idx)
                total_match_score += best_score
            else:
                missing_skills.append({
                    "skill": req,
                    "best_partial_match": best_cand if best_score > 0.40 else None,
                    "partial_similarity": round(best_score, 3) if best_score > 0.40 else 0.0
                })

        # Find leftover candidate skills that are related
        related_skills = []
        for j, cand in enumerate(clean_candidate):
            if j not in matched_candidate_indices:
                # Check max similarity with any required skill
                max_rel_score = float(np.max(sim_matrix[:, j])) if len(clean_required) > 0 else 0.0
                related_skills.append({
                    "skill": cand,
                    "relevance_score": round(max_rel_score, 3)
                })

        # Save any new embeddings to disk
        self._save_cache()

        overall_score = round(total_match_score / len(clean_required), 4)
        match_rate_pct = round((len(matched_skills) / len(clean_required)) * 100.0, 1)

        return {
            "semantic_similarity_score": overall_score,
            "match_rate_pct": match_rate_pct,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "related_skills": related_skills,
            "total_required": len(clean_required),
            "total_candidate": len(clean_candidate)
        }

# Global instance for reuse
_matcher_instance = None

def get_semantic_matcher() -> SemanticSkillMatcher:
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = SemanticSkillMatcher()
    return _matcher_instance
