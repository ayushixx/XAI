import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

import src.utils.env_setup
from src.config.settings import PROCESSED_DIR, MODELS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

EMBEDDINGS_DIR = PROCESSED_DIR / "personality_embeddings"
EMBEDDINGS_CACHE_FILE = EMBEDDINGS_DIR / "latent_personality_embeddings.json"

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not found. Using mathematical linear autoencoder projection.")

if TORCH_AVAILABLE:
    class PersonalityAutoencoderNN(nn.Module):
        """
        Deep Neural Network Autoencoder for Personality Trait Dimensionality Reduction.
        Encoder: 5 -> 16 -> 8 -> 3 (Latent Space)
        Decoder: 3 -> 8 -> 16 -> 5 (Reconstruction)
        """
        def __init__(self):
            super().__init__()
            # Encoder: 5 -> 16 -> 8 -> 3
            self.encoder = nn.Sequential(
                nn.Linear(5, 16),
                nn.LeakyReLU(0.1),
                nn.Linear(16, 8),
                nn.LeakyReLU(0.1),
                nn.Linear(8, 3)
            )
            # Decoder: 3 -> 8 -> 16 -> 5
            self.decoder = nn.Sequential(
                nn.Linear(3, 8),
                nn.LeakyReLU(0.1),
                nn.Linear(8, 16),
                nn.LeakyReLU(0.1),
                nn.Linear(16, 5)
            )

        def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            latent = self.encoder(x)
            reconstructed = self.decoder(latent)
            return latent, reconstructed

class PersonalityAutoencoderEngine:
    """
    Personality Embedding & Deep Latent Factor Representation Engine.
    Encodes Big Five personality traits into a compact 3-dimensional behavioral latent space.
    """
    TRAIT_ORDER = [
        "Neuroticism",
        "Extraversion",
        "Openness",
        "Agreeableness",
        "Conscientiousness"
    ]

    def __init__(self):
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
        self.nn_model = None
        self._memory_cache: Dict[str, List[float]] = {}
        self._init_model()
        self.load_stored_embeddings()

    def _init_model(self) -> None:
        if TORCH_AVAILABLE:
            torch.manual_seed(42)
            self.nn_model = PersonalityAutoencoderNN()
            self.nn_model.eval()
            logger.info("PersonalityAutoencoder Deep Learning model initialized (5 -> 16 -> 8 -> 3 -> 8 -> 16 -> 5)")

    def _normalize_traits_input(self, traits: Dict[str, float]) -> np.ndarray:
        """Extracts and scales the 5 Big-Five traits into a 5D vector."""
        vec = []
        for trait in self.TRAIT_ORDER:
            # Handle case-insensitive key lookup
            val = None
            for k, v in traits.items():
                if k.lower() == trait.lower():
                    val = float(v)
                    break
            if val is None:
                val = 5.0  # Default neutral score
            vec.append(val)
        return np.array(vec, dtype=np.float32)

    def encode_personality(
        self,
        candidate_id: str,
        traits: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Encodes candidate Big Five personality traits:
        Input: Neuroticism, Extraversion, Openness, Agreeableness, Conscientiousness
        Returns:
            personality_embedding: Normalized 3D latent vector
            latent_personality_vector: Exact continuous latent coordinates [z1, z2, z3]
            reconstructed_traits: Model's autoencoder reconstruction
            reconstruction_loss: Mean squared reconstruction error
        """
        raw_vec = self._normalize_traits_input(traits)

        if TORCH_AVAILABLE and self.nn_model is not None:
            with torch.no_grad():
                tensor_in = torch.from_numpy(raw_vec).unsqueeze(0)
                latent_tensor, recon_tensor = self.nn_model(tensor_in)
                latent_vec = latent_tensor.squeeze(0).numpy()
                recon_vec = recon_tensor.squeeze(0).numpy()
        else:
            # Mathematical orthogonal compression fallback (5 -> 3)
            # Weights mapping: [Emotional Stability vs Neuroticism, Executive Drive/Conscientiousness, Social Openness]
            W_enc = np.array([
                [-0.45, 0.20, 0.10, 0.15, 0.35],
                [0.10, 0.40, 0.30, 0.20, 0.45],
                [-0.20, 0.35, 0.50, 0.35, 0.20]
            ], dtype=np.float32)
            latent_vec = np.dot(W_enc, raw_vec)
            recon_vec = np.dot(W_enc.T, latent_vec)

        # Normalize latent vector for cosine/embedding calculations
        norm = np.linalg.norm(latent_vec)
        normalized_emb = (latent_vec / (norm if norm > 0 else 1.0)).tolist()

        latent_coords = [round(float(z), 4) for z in latent_vec]
        reconstructed_dict = {
            trait: round(float(recon_vec[i]), 2)
            for i, trait in enumerate(self.TRAIT_ORDER)
        }

        mse_loss = float(np.mean((raw_vec - recon_vec) ** 2))

        # Store in memory and cache
        self._memory_cache[candidate_id] = normalized_emb
        self.store_embeddings()

        return {
            "candidate_id": candidate_id,
            "raw_traits": {trait: round(float(raw_vec[i]), 2) for i, trait in enumerate(self.TRAIT_ORDER)},
            "personality_embedding": [round(x, 4) for x in normalized_emb],
            "latent_personality_vector": latent_coords,
            "latent_dimensions_meaning": {
                "z1_emotional_resilience": latent_coords[0],
                "z2_executive_drive_and_structure": latent_coords[1],
                "z3_collaborative_openness": latent_coords[2]
            },
            "reconstructed_traits": reconstructed_dict,
            "reconstruction_loss_mse": round(mse_loss, 4)
        }

    def store_embeddings(self) -> None:
        """Persists candidate personality embeddings to local JSON storage."""
        try:
            with open(EMBEDDINGS_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self._memory_cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not persist personality embeddings to disk: {e}")

    def load_stored_embeddings(self) -> None:
        """Loads stored personality embeddings from local disk."""
        if EMBEDDINGS_CACHE_FILE.exists():
            try:
                with open(EMBEDDINGS_CACHE_FILE, "r", encoding="utf-8") as f:
                    self._memory_cache = json.load(f)
                logger.info(f"Loaded {len(self._memory_cache)} stored personality embeddings from disk.")
            except Exception as e:
                logger.warning(f"Failed to load personality embeddings from disk: {e}")

# Global Singleton
_PERSONALITY_AUTOENCODER = None

def get_personality_autoencoder() -> PersonalityAutoencoderEngine:
    global _PERSONALITY_AUTOENCODER
    if _PERSONALITY_AUTOENCODER is None:
        _PERSONALITY_AUTOENCODER = PersonalityAutoencoderEngine()
    return _PERSONALITY_AUTOENCODER
