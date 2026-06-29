"""ZENITH API — the HACD naming layer.

A small, well-documented FastAPI service over the naming engine. Read-only,
no custody, no signing. CORS is open so a Lovable frontend can call it directly.

Run locally:
    uvicorn app.main:app --reload --port 8000
Docs:
    http://localhost:8000/docs
"""
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import __version__, engine, gating

app = FastAPI(
    title="ZENITH — HACD Naming Layer",
    version=__version__,
    description=(
        "The naming intelligence layer for HACD. Scores any 6-letter HACD name, "
        "surfaces premium dictionary-word / palindrome / pattern names, and gates "
        "premium surfaces behind the ZEN Stack Token. Read-only — never asks for "
        "keys, seed phrases, or signatures."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
class BulkRequest(BaseModel):
    names: list[str] = Field(..., max_length=200, description="Up to 200 candidate names.")
    address: str = Field("", description="ZEN holder address (read-only, for gating).")


class AccessOut(BaseModel):
    address: str
    zen_balance: int
    tier: str
    source: str


# --------------------------------------------------------------------------- #
# Meta
# --------------------------------------------------------------------------- #
@app.get("/", tags=["meta"])
def root() -> dict:
    return {
        "name": "ZENITH",
        "tagline": "Every HACD is a word. ZENITH tells you which words are worth owning.",
        "version": __version__,
        "alphabet": engine.ALPHABET,
        "total_name_space": engine.TOTAL_NAME_SPACE,
        "endpoints": ["/health", "/meta", "/analyze", "/validate", "/search", "/leaderboard", "/bulk", "/access"],
        "docs": "/docs",
    }


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/meta", tags=["meta"])
def meta() -> dict:
    """Dataset statistics and the canonical HACD alphabet."""
    return engine.dataset_meta()


# --------------------------------------------------------------------------- #
# Free tier
# --------------------------------------------------------------------------- #
@app.get("/validate", tags=["free"])
def validate(name: str = Query(..., description="Candidate HACD name.")) -> dict:
    """Is this a structurally valid HACD name? (length + alphabet)"""
    ok, reason = engine.is_valid_hacd(name)
    return {"name": engine.normalize(name), "valid": ok, "reason": reason or "valid"}


@app.get("/analyze", tags=["free"])
def analyze(name: str = Query(..., description="Candidate HACD name to score.")) -> dict:
    """Full namescore (0-100), tier, tags, and reasons for one name."""
    return engine.analyze(name).to_dict()


# --------------------------------------------------------------------------- #
# Holder tier (gated)
# --------------------------------------------------------------------------- #
def _require(feature: str, address: str) -> gating.AccessResult:
    access = gating.check_access(feature, address)
    if not access.allowed:
        raise HTTPException(
            status_code=402,  # Payment Required — you need more ZEN
            detail={
                "error": "insufficient_zen",
                "message": f"'{feature}' requires the '{access.required_tier}' tier.",
                "your_tier": access.tier,
                "your_zen_balance": access.zen_balance,
                "required_tier": access.required_tier,
                "how_to_unlock": "Stack ZEN via the HACD Launchpad to raise your tier.",
            },
        )
    return access


@app.get("/search", tags=["holder"])
def search(
    contains: str = Query("", description="Substring the name must contain."),
    starts_with: str = "",
    ends_with: str = "",
    only_words: bool = True,
    min_score: int = Query(0, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
    address: str = Query("", description="ZEN holder address (read-only)."),
) -> dict:
    """Search premium HACD names. Requires the `holder` tier (>= 1,000 ZEN)."""
    access = _require("search", address)
    results = engine.search(contains, starts_with, ends_with, only_words, min_score, limit)
    return {"count": len(results), "tier": access.tier, "results": results}


@app.get("/leaderboard", tags=["holder"])
def leaderboard(
    limit: int = Query(25, ge=1, le=200),
    address: str = Query("", description="ZEN holder address (read-only)."),
) -> dict:
    """The highest-scoring HACD names in existence. Requires `holder` tier."""
    access = _require("leaderboard", address)
    return {"tier": access.tier, "results": engine.leaderboard(limit)}


# --------------------------------------------------------------------------- #
# Pro tier (gated)
# --------------------------------------------------------------------------- #
@app.post("/bulk", tags=["pro"])
def bulk(req: BulkRequest) -> dict:
    """Score up to 200 names at once. Requires the `pro` tier (>= 10,000 ZEN)."""
    access = _require("bulk", req.address)
    results = [engine.analyze(n).to_dict() for n in req.names]
    results.sort(key=lambda r: -r["score"])
    return {"count": len(results), "tier": access.tier, "results": results}


# --------------------------------------------------------------------------- #
# Access introspection
# --------------------------------------------------------------------------- #
@app.get("/access", response_model=AccessOut, tags=["meta"])
def access(address: str = Query("", description="Address to check ZEN tier for (read-only).")) -> AccessOut:
    """Report the ZEN balance and access tier for an address. Never asks for keys."""
    a = gating.check_access("analyze", address)
    return AccessOut(address=a.address, zen_balance=a.zen_balance, tier=a.tier, source=a.source)
