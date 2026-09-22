"""
Lazy model loader — models are only loaded on the first inference call,
NOT at server startup. This keeps Render's 512 MB free-tier alive:
  • SpaCy en_core_web_md  ≈  50 MB
  • all-MiniLM-L6-v2     ≈  90 MB model + PyTorch overhead

Loading both at boot would exceed 512 MB before the first request arrives.
With lazy loading the first resume analysis is slower (~5 s), but the server
stays within memory limits.
"""
import logging
from functools import lru_cache

from backend.core.config import (
    SPACY_MODEL_PRIMARY,
    SPACY_MODEL_SECONDARY,
    SENTENCE_TRANSFORMER_MODEL,
)

logger = logging.getLogger("ats_resume_scorer")


@lru_cache(maxsize=1)
def get_nlp():
    """Return the SpaCy NLP model, loading it on the first call."""
    import spacy

    try:
        logger.info(f"[lazy] Loading spaCy model: {SPACY_MODEL_PRIMARY}")
        nlp = spacy.load(SPACY_MODEL_PRIMARY)
        logger.info(f"[lazy] spaCy {SPACY_MODEL_PRIMARY} ready")
        return nlp
    except OSError:
        logger.warning(f"[lazy] {SPACY_MODEL_PRIMARY} not found — falling back to {SPACY_MODEL_SECONDARY}")
        nlp = spacy.load(SPACY_MODEL_SECONDARY)
        logger.info(f"[lazy] spaCy {SPACY_MODEL_SECONDARY} (fallback) ready")
        return nlp


@lru_cache(maxsize=1)
def get_embedder():
    """Return the SentenceTransformer embedder, loading it on the first call."""
    from sentence_transformers import SentenceTransformer

    logger.info(f"[lazy] Loading SentenceTransformer: {SENTENCE_TRANSFORMER_MODEL}")
    embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    logger.info(f"[lazy] SentenceTransformer {SENTENCE_TRANSFORMER_MODEL} ready")
    return embedder
