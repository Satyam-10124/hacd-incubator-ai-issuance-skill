"""ZENITH naming engine.

Pure, dependency-free analysis of HACD names. Everything here is deterministic
and offline: given a 6-letter candidate over the 16-letter HACD alphabet, it
produces a structured *namescore* (0-100) plus the human-readable reasons behind
it, and it can search the pre-computed dataset for premium names.

This module is the heart of the product. The API in `main.py` is a thin shell
over it; the token-gating logic in `gating.py` decides who may call the
heavier endpoints.

ZENITH deliberately scores names on *linguistic and structural* properties
(words, palindromes, repetition, letter rarity) — NOT on market rarity / HIP
rank, which is Carat Protocol's domain. The two are complementary: Carat tells
you what a HACD is worth on the market; ZENITH tells you what it *says*.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field, asdict
from functools import lru_cache
from pathlib import Path

ALPHABET = "ABEHIKMNSTUVWXYZ"
ALPHA_SET = set(ALPHABET)
NAME_LEN = 6
TOTAL_NAME_SPACE = len(ALPHABET) ** NAME_LEN  # 16,777,216

DATA_PATH = Path(__file__).parent.parent / "data" / "dataset.json"

# Per-letter frequency weight. Letters that are RARER in real English words
# (computed offline from the dictionary subset) score higher, because a name
# built from rare letters is visually distinctive. Hand-tuned, stable ordering.
# Lower number = more common in the valid-word corpus = less distinctive.
LETTER_RARITY = {
    "A": 1, "E": 1, "I": 2, "S": 2, "T": 2, "N": 2, "M": 3, "H": 3,
    "U": 3, "B": 4, "K": 4, "Y": 4, "V": 5, "W": 5, "X": 6, "Z": 6,
}


@dataclass
class ScoreBreakdown:
    word: int = 0
    palindrome: int = 0
    repetition: int = 0
    rarity: int = 0
    structure: int = 0

    def total(self) -> int:
        return min(100, self.word + self.palindrome + self.repetition + self.rarity + self.structure)


@dataclass
class NameAnalysis:
    name: str
    valid: bool
    score: int
    tier: str
    breakdown: dict
    tags: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    is_dictionary_word: bool = False
    is_palindrome: bool = False
    repeat_signature: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@lru_cache(maxsize=1)
def _dataset() -> dict:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"dataset.json missing at {DATA_PATH}. Run `python3 build_dataset.py` first."
        )
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _word_set() -> frozenset[str]:
    return frozenset(_dataset()["dictionary_words"])


def dataset_meta() -> dict:
    d = _dataset()
    return {**d["meta"], **d["stats"]}


def normalize(name: str) -> str:
    return (name or "").strip().upper()


def is_valid_hacd(name: str) -> tuple[bool, str]:
    """Return (valid, reason_if_invalid)."""
    name = normalize(name)
    if len(name) != NAME_LEN:
        return False, f"A HACD name must be exactly {NAME_LEN} letters (got {len(name)})."
    bad = sorted(set(name) - ALPHA_SET)
    if bad:
        return False, f"Letters not in the HACD alphabet: {', '.join(bad)}. Valid letters: {ALPHABET}."
    return True, ""


def _repeat_signature(name: str) -> str:
    counts = sorted(Counter(name).values(), reverse=True)
    return "".join(str(c) for c in counts)


def analyze(name: str) -> NameAnalysis:
    """Score a single candidate HACD name. Always returns a structured result."""
    name = normalize(name)
    valid, reason = is_valid_hacd(name)
    if not valid:
        return NameAnalysis(
            name=name, valid=False, score=0, tier="invalid",
            breakdown=ScoreBreakdown().__dict__, reasons=[reason],
        )

    b = ScoreBreakdown()
    tags: list[str] = []
    reasons: list[str] = []

    is_word = name in _word_set()
    is_pal = name == name[::-1]
    sig = _repeat_signature(name)
    counts = Counter(name)
    distinct = len(counts)
    max_run = max(counts.values())

    # --- word ---
    if is_word:
        b.word = 45
        tags.append("dictionary-word")
        reasons.append("Real English dictionary word — only 1,219 of 16,777,216 names qualify.")

    # --- palindrome ---
    if is_pal:
        b.palindrome = 22
        tags.append("palindrome")
        reasons.append("Reads the same forwards and backwards (1 in 4,096 names).")

    # --- repetition / pattern ---
    if distinct == 1:
        b.repetition = 30
        tags.append("solid")
        reasons.append("Solid name — a single letter repeated six times (only 16 exist).")
    elif sig == "33" or sig == "42" or sig == "51":
        b.repetition = 16
        tags.append("heavy-repeat")
        reasons.append(f"Strong repetition pattern ({sig}).")
    elif max_run >= 3:
        b.repetition = 10
        tags.append("triple")
        reasons.append("Contains a letter repeated three or more times.")
    elif max_run == 2:
        b.repetition = 5
        if name[0] == name[1]:
            tags.append("double-start")
            reasons.append("Opens with a doubled letter.")

    # --- letter rarity ---
    rarity_pts = sum(LETTER_RARITY[c] for c in counts) / max(1, distinct)
    rarity_norm = int(min(18, (rarity_pts - 1) * 4))
    b.rarity = max(0, rarity_norm)
    rare_letters = [c for c in counts if LETTER_RARITY[c] >= 5]
    if rare_letters:
        tags.append("rare-letters")
        reasons.append(f"Uses rare letters: {', '.join(sorted(set(rare_letters)))}.")

    # --- structure niceties ---
    if distinct <= 3 and not is_word:
        b.structure = 6
        tags.append("low-alphabet")
        reasons.append("Built from a small set of letters — visually clean.")
    if name[:3] == name[3:]:
        b.structure += 8
        tags.append("mirror-half")
        reasons.append("First three letters repeat as the last three (e.g. ABEABE).")

    score = b.total()
    tier = (
        "mythic" if score >= 80 else
        "legendary" if score >= 60 else
        "rare" if score >= 40 else
        "uncommon" if score >= 20 else
        "common"
    )
    if not reasons:
        reasons.append("Valid HACD name with no premium pattern detected.")

    return NameAnalysis(
        name=name, valid=True, score=score, tier=tier,
        breakdown=b.__dict__, tags=tags, reasons=reasons,
        is_dictionary_word=is_word, is_palindrome=is_pal, repeat_signature=sig,
    )


def search(
    contains: str = "",
    starts_with: str = "",
    ends_with: str = "",
    only_words: bool = True,
    min_score: int = 0,
    limit: int = 50,
) -> list[dict]:
    """Search the premium dataset (dictionary words by default).

    Falls back to scanning generated patterns only when a non-word filter is
    used; the dataset is small enough that this is instant.
    """
    contains = normalize(contains)
    starts_with = normalize(starts_with)
    ends_with = normalize(ends_with)

    if only_words:
        pool = sorted(_word_set())
    else:
        extended = set(_word_set())
        d = _dataset()
        extended.update(d.get("solid_letter_names", []))
        extended.update(d.get("palindromes", []))
        pool = sorted(extended)
    results: list[dict] = []
    for w in pool:
        if contains and contains not in w:
            continue
        if starts_with and not w.startswith(starts_with):
            continue
        if ends_with and not w.endswith(ends_with):
            continue
        a = analyze(w)
        if a.score < min_score:
            continue
        results.append(a.to_dict())

    results.sort(key=lambda r: (-r["score"], r["name"]))
    return results[:limit]


def leaderboard(limit: int = 25) -> list[dict]:
    """Highest-scoring premium names across the whole dataset."""
    scored = [analyze(w).to_dict() for w in _word_set()]
    # fold in the solid names, which aren't dictionary words
    for solid in _dataset()["solid_letter_names"]:
        scored.append(analyze(solid).to_dict())
    scored.sort(key=lambda r: (-r["score"], r["name"]))
    return scored[:limit]
