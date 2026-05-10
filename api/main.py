"""
buzzle/api/main.py
FastAPI REST API for the buzzle phrase generator.
"""

import time
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engine import generate_phrase, generate_multiple

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="buzzle API",
    description="The world's most over-engineered motivational phrase generator.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── State ─────────────────────────────────────────────────────────────────────

START_TIME = time.time()
_stats = {"total": 0, "noun_counter": {}}


# ── Models ────────────────────────────────────────────────────────────────────

class CustomPhraseRequest(BaseModel):
    noun: Optional[str] = None
    verb: Optional[str] = None
    adjective: Optional[str] = None
    seed: Optional[int] = None


class PhraseResponse(BaseModel):
    phrase: str
    score: int
    category: str
    generated_at: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _track(phrase_data: dict):
    _stats["total"] += 1
    # Extract noun (first word after "The" or second word)
    words = phrase_data["phrase"].split()
    noun = words[1] if len(words) > 1 else words[0]
    _stats["noun_counter"][noun] = _stats["noun_counter"].get(noun, 0) + 1


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["root"])
def root():
    """Buzzle is alive."""
    return {
        "service": "buzzle",
        "version": "1.0.0",
        "motto": "Generating profundity since 2026.",
        "endpoints": ["/phrase", "/phrase/rated", "/stats", "/phrase/custom"],
    }


@app.get("/phrase", response_model=list[PhraseResponse] | PhraseResponse, tags=["phrases"])
def get_phrase(
    count: int = Query(default=1, ge=1, le=20, description="Number of phrases (max 20)"),
    seed: Optional[int] = Query(default=None, description="RNG seed for reproducibility"),
):
    """
    Generate one or more motivational phrases.
    Use `count` to get multiple. Use `seed` for reproducibility.
    """
    if count == 1:
        result = generate_phrase(seed=seed)
        _track(result)
        return result
    results = generate_multiple(count=count, seed=seed)
    for r in results:
        _track(r)
    return results


@app.get("/phrase/rated", response_model=PhraseResponse, tags=["phrases"])
def get_rated_phrase(seed: Optional[int] = Query(default=None)):
    """Get a phrase with its completely fabricated profoundness score."""
    result = generate_phrase(seed=seed)
    _track(result)
    return result


@app.post("/phrase/custom", response_model=PhraseResponse, tags=["phrases"])
def custom_phrase(body: CustomPhraseRequest):
    """Build a phrase using your own words. Missing fields are randomized."""
    result = generate_phrase(
        seed=body.seed,
        noun=body.noun,
        verb=body.verb,
        adjective=body.adjective,
    )
    _track(result)
    return result


@app.get("/stats", tags=["meta"])
def get_stats():
    """Return API usage statistics."""
    most_used = (
        max(_stats["noun_counter"], key=_stats["noun_counter"].get)
        if _stats["noun_counter"]
        else "none yet"
    )
    return {
        "total_phrases_generated": _stats["total"],
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "most_used_noun": most_used,
        "engine_version": "1.0.0",
    }


@app.get("/health", tags=["meta"])
def health():
    """Liveness probe."""
    return {"status": "ok"}
