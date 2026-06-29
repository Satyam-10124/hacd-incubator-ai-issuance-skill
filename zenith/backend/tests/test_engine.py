"""Tests for the ZENITH naming engine and gating. Run: pytest -q"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import engine, gating  # noqa: E402


# --- validity ---------------------------------------------------------------
def test_alphabet_is_16_letters():
    assert len(engine.ALPHABET) == 16
    assert set(engine.ALPHABET) == set("ABEHIKMNSTUVWXYZ")


def test_total_name_space():
    assert engine.TOTAL_NAME_SPACE == 16 ** 6 == 16_777_216


def test_invalid_wrong_length():
    ok, reason = engine.is_valid_hacd("ABC")
    assert not ok and "6 letters" in reason


def test_invalid_bad_letter():
    # C, D, O are NOT in the HACD alphabet.
    ok, reason = engine.is_valid_hacd("CODECO")
    assert not ok and "not in the HACD alphabet" in reason


def test_valid_name():
    ok, _ = engine.is_valid_hacd("ZENITH")
    assert ok


# --- scoring ----------------------------------------------------------------
def test_project_name_zenith_is_a_word():
    a = engine.analyze("ZENITH")
    assert a.valid
    assert a.is_dictionary_word
    assert a.score >= 45
    assert "dictionary-word" in a.tags


def test_solid_name_scores_high():
    a = engine.analyze("AAAAAA")
    assert "solid" in a.tags
    assert a.tier in ("legendary", "mythic")


def test_invalid_name_scores_zero():
    a = engine.analyze("ZZZ")
    assert not a.valid and a.score == 0


def test_tiers_are_ordered():
    order = ["common", "uncommon", "rare", "legendary", "mythic"]
    # a plain valid non-word should not beat a dictionary word
    plain = engine.analyze("BHKMVW")  # unlikely to be a word
    word = engine.analyze("ZENITH")
    assert word.score > plain.score


# --- search -----------------------------------------------------------------
def test_search_returns_words_only_by_default():
    res = engine.search(contains="AB", limit=10)
    assert all(r["is_dictionary_word"] for r in res)
    assert len(res) <= 10


def test_search_starts_with():
    res = engine.search(starts_with="ZE", limit=50)
    assert all(r["name"].startswith("ZE") for r in res)


def test_search_non_word_includes_solid_names():
    res = engine.search(only_words=False, min_score=30, limit=50)
    solid_found = any(r.get("tags") and "solid" in r["tags"] for r in res)
    assert solid_found, "Non-word search must surface solid names (the dead-else bug)"


def test_leaderboard_sorted_desc():
    lb = engine.leaderboard(limit=20)
    scores = [r["score"] for r in lb]
    assert scores == sorted(scores, reverse=True)


# --- gating -----------------------------------------------------------------
def test_free_feature_always_allowed():
    a = gating.check_access("analyze", "anyaddress")
    assert a.allowed


def test_offline_balance_is_deterministic():
    b1, src = gating.lookup_balance("HX_TEST_ADDRESS")
    b2, _ = gating.lookup_balance("HX_TEST_ADDRESS")
    assert b1 == b2
    assert src == "offline-sim"


def test_tier_thresholds():
    assert gating.tier_for_balance(0) == gating.FREE_TIER
    assert gating.tier_for_balance(1_000) == gating.HOLDER_TIER
    assert gating.tier_for_balance(10_000) == gating.PRO_TIER


def test_pro_feature_blocked_for_low_balance(monkeypatch):
    monkeypatch.setattr(gating, "lookup_balance", lambda a: (0, "offline-sim"))
    a = gating.check_access("bulk", "broke")
    assert not a.allowed and a.required_tier == gating.PRO_TIER
