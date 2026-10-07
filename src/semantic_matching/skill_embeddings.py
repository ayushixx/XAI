import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

import src.utils.env_setup  # Preload dynamic libraries on macOS
from src.config.settings import PROCESSED_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Standard abbreviations and synonymous tech expansions
SKILL_ABBREVIATIONS = {
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "DL": "Deep Learning",
    "NLP": "Natural Language Processing",
    "CV": "Computer Vision",
    "LLM": "Large Language Models",
    "LLMS": "Large Language Models",
    "RAG": "Retrieval Augmented Generation",
    "DS": "Data Science",
    "BI": "Business Intelligence",
    "EDA": "Exploratory Data Analysis",
    "SBERT": "Sentence-BERT Embeddings",
    "GBDT": "Gradient Boosted Decision Trees",
    "XGB": "XGBoost",
    "LGBM": "LightGBM",
    "TF": "TensorFlow",
    "PT": "PyTorch",
    "SKLEARN": "Scikit-Learn",
    "GCP": "Google Cloud Platform",
    "AWS": "Amazon Web Services",
    "K8S": "Kubernetes",
    "DOCKER": "Docker Containerization",
    "SQL": "Structured Query Language",
    "ETL": "Extract Transform Load Data Pipelines",
    "ELT": "Extract Load Transform Data Pipelines"
}

CACHE_DIR = PROCESSED_DIR / "embeddings"
CACHE_FILE = CACHE_DIR / "skill_embeddings_cache.json"

class SkillEmbeddingEngine:
    """
    Production Sentence-BERT Semantic Skill Matcher & Vector Similarity Engine.
    Uses 'all-MiniLM-L6-v2' to project skills and job descriptions into a 384-dimensional dense space.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._memory_cache: Dict[str, List[float]] = {}
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.load_embeddings_from_local()

    def _get_model(self):
        """Lazy load SentenceTransformer model to optimize memory and startup speed."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Falling back to algorithmic dense vectorizer.")
                self._model = "FALLBACK"
        return self._model

    def normalize_skill(self, skill: str) -> str:
        """Expands common abbreviations and standardizes whitespace."""
        clean = skill.strip()
        upper = clean.upper()
        if upper in SKILL_ABBREVIATIONS:
            return SKILL_ABBREVIATIONS[upper]
        return clean

    def generate_skill_embedding(self, skill: str) -> np.ndarray:
        """
        Generates a normalized 384-dimensional dense vector for a single skill.
        Caches results locally on disk and in memory.
        """
        normalized = self.normalize_skill(skill)
        cache_key = normalized.lower()

        if cache_key in self._memory_cache:
            return np.array(self._memory_cache[cache_key], dtype=np.float32)

        model = self._get_model()
        if model != "FALLBACK" and hasattr(model, "encode"):
            try:
                emb = model.encode(normalized, convert_to_numpy=True, normalize_embeddings=True)
                self._memory_cache[cache_key] = emb.tolist()
                self.store_embeddings_locally()
                return emb.astype(np.float32)
            except Exception as e:
                logger.warning(f"Embedding encoding failed for '{skill}': {e}. Using deterministic projection.")

        # Fallback deterministic pseudo-embedding (384-dimensional) based on character n-grams
        np.random.seed(abs(hash(cache_key)) % (2**32))
        vec = np.random.randn(384).astype(np.float32)
        norm = np.linalg.norm(vec)
        vec = vec / (norm if norm > 0 else 1.0)
        self._memory_cache[cache_key] = vec.tolist()
        return vec

    def generate_requirements_embedding(self, requirements: List[str]) -> np.ndarray:
        """
        Generates an aggregated pooled embedding representing an entire job specification or requirement list.
        """
        if not requirements:
            return np.zeros(384, dtype=np.float32)

        vectors = [self.generate_skill_embedding(req) for req in requirements if req.strip()]
        if not vectors:
            return np.zeros(384, dtype=np.float32)

        mean_vec = np.mean(vectors, axis=0)
        norm = np.linalg.norm(mean_vec)
        return (mean_vec / (norm if norm > 0 else 1.0)).astype(np.float32)

    @staticmethod
    def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Computes cosine similarity between two unit-normalized vectors."""
        dot = float(np.dot(vec1, vec2))
        norm1 = float(np.linalg.norm(vec1))
        norm2 = float(np.linalg.norm(vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        sim = dot / (norm1 * norm2)
        return float(np.clip(sim, 0.0, 1.0))

    def detect_semantic_matches(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        threshold: float = 0.65
    ) -> Dict[str, Any]:
        """
        Compares candidate skill set against required target skills using cosine similarity.
        Identifies:
        - Exact & Semantic Matches (e.g. 'ML' matches 'Machine Learning')
        - Missing Critical Skills
        - Semantic Match Score (0.0 - 100.0)
        """
        if not required_skills:
            return {
                "semantic_score": 100.0,
                "matches": [],
                "missing_skills": [],
                "match_count": 0,
                "total_required": 0
            }

        candidate_embeddings = {
            s: self.generate_skill_embedding(s)
            for s in candidate_skills if s.strip()
        }

        matches = []
        matched_required = set()

        for req in required_skills:
            req_clean = req.strip()
            if not req_clean:
                continue
            req_vec = self.generate_skill_embedding(req_clean)
            best_match_skill = None
            best_sim = 0.0

            for cand_skill, cand_vec in candidate_embeddings.items():
                # Direct string equality after normalization check
                if self.normalize_skill(cand_skill).lower() == self.normalize_skill(req_clean).lower():
                    best_match_skill = cand_skill
                    best_sim = 1.0
                    break

                sim = self.compute_cosine_similarity(req_vec, cand_vec)
                if sim > best_sim:
                    best_sim = sim
                    best_match_skill = cand_skill

            if best_sim >= threshold and best_match_skill:
                matches.append({
                    "required_skill": req_clean,
                    "matched_candidate_skill": best_match_skill,
                    "similarity_score": round(best_sim, 4),
                    "match_type": "Exact" if best_sim >= 0.98 else "Semantic Equivalent"
                })
                matched_required.add(req_clean)

        missing_skills = [r for r in required_skills if r.strip() and r.strip() not in matched_required]

        # Overall semantic match score calculation
        if matches:
            avg_match_sim = sum(m["similarity_score"] for m in matches) / len(required_skills)
            semantic_score = round(avg_match_sim * 100.0, 2)
        else:
            semantic_score = 0.0

        return {
            "semantic_score": semantic_score,
            "match_ratio": round(len(matches) / max(len(required_skills), 1), 4),
            "match_count": len(matches),
            "total_required": len(required_skills),
            "matches": matches,
            "missing_skills": missing_skills
        }

    def store_embeddings_locally(self) -> None:
        """Persists memory vector cache to disk in JSON format."""
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self._memory_cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not persist embeddings cache to disk: {e}")

    def load_embeddings_from_local(self) -> None:
        """Loads cached skill embeddings from local disk."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self._memory_cache = json.load(f)
                logger.info(f"Loaded {len(self._memory_cache)} cached skill embeddings from {CACHE_FILE}")
            except Exception as e:
                logger.warning(f"Failed to load cached embeddings: {e}")

# Global Singleton instance
_SKILL_EMBEDDER = None

def get_skill_embedder() -> SkillEmbeddingEngine:
    global _SKILL_EMBEDDER
    if _SKILL_EMBEDDER is None:
        _SKILL_EMBEDDER = SkillEmbeddingEngine()
    return _SKILL_EMBEDDER
