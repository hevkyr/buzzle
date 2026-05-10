"""
buzzle/tests/test_engine.py
Unit tests for the phrase generation engine.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from engine import generate_phrase, generate_multiple, _profoundness_score


class TestGeneratePhrase:
    def test_returns_dict(self):
        result = generate_phrase()
        assert isinstance(result, dict)

    def test_required_keys(self):
        result = generate_phrase()
        assert "phrase" in result
        assert "score" in result
        assert "category" in result
        assert "generated_at" in result

    def test_phrase_is_non_empty_string(self):
        result = generate_phrase()
        assert isinstance(result["phrase"], str)
        assert len(result["phrase"]) > 10

    def test_phrase_ends_with_punctuation(self):
        for _ in range(20):
            result = generate_phrase()
            assert result["phrase"][-1] in ".!?", (
                f"Phrase does not end with punctuation: {result['phrase']}"
            )

    def test_phrase_starts_uppercase(self):
        for _ in range(10):
            result = generate_phrase()
            assert result["phrase"][0].isupper()

    def test_score_is_integer_in_range(self):
        for _ in range(20):
            result = generate_phrase()
            assert isinstance(result["score"], int)
            assert 1 <= result["score"] <= 100

    def test_category_is_valid(self):
        valid = {"hustle", "tech", "mindset", "chaos", "enlightenment"}
        for _ in range(20):
            result = generate_phrase()
            assert result["category"] in valid

    def test_seed_reproducibility(self):
        r1 = generate_phrase(seed=42)
        r2 = generate_phrase(seed=42)
        assert r1["phrase"] == r2["phrase"]
        assert r1["score"] == r2["score"]

    def test_different_seeds_differ(self):
        phrases = {generate_phrase(seed=i)["phrase"] for i in range(10)}
        assert len(phrases) > 1

    def test_custom_noun(self):
        result = generate_phrase(noun="capybara")
        assert "capybara" in result["phrase"].lower()

    def test_custom_verb(self):
        result = generate_phrase(verb="deploys")
        # verb may be title-cased in some templates
        assert "deploys" in result["phrase"].lower() or "Deploys" in result["phrase"]

    def test_custom_adjective(self):
        result = generate_phrase(adjective="caffeinated")
        assert "caffeinated" in result["phrase"].lower()


class TestGenerateMultiple:
    def test_returns_list(self):
        results = generate_multiple(count=5)
        assert isinstance(results, list)

    def test_correct_count(self):
        results = generate_multiple(count=5)
        assert len(results) == 5

    def test_uniqueness(self):
        results = generate_multiple(count=10)
        phrases = [r["phrase"] for r in results]
        assert len(set(phrases)) == len(phrases), "Duplicate phrases detected"

    def test_count_clamped_at_max(self):
        results = generate_multiple(count=999)
        assert len(results) <= 20

    def test_count_minimum_is_one(self):
        results = generate_multiple(count=0)
        assert len(results) >= 1


class TestProfoundnessScore:
    def test_score_in_range(self):
        for phrase in [
            "The caffeinated cactus never deploys to gravity.",
            "A.",
            "In a world of spreadsheets, be the agile penguin.",
        ]:
            score = _profoundness_score(phrase)
            assert 1 <= score <= 100
