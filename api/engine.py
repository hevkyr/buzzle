"""
buzzle/api/engine.py
Core phrase generation engine.
"""

import random
import string
from datetime import datetime, timezone
from typing import Optional

from words import NOUNS, VERBS, ADJECTIVES, PREPOSITIONS, TEMPLATES

CATEGORIES = ["hustle", "tech", "mindset", "chaos", "enlightenment"]


def _syllable_count(word: str) -> int:
    """Approximate syllable count (good enough for fake scoring)."""
    word = word.lower().strip(string.punctuation)
    count = 0
    vowels = "aeiouy"
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    return max(1, count)


def _profoundness_score(phrase: str) -> int:
    """
    Compute a completely fake but internally consistent profoundness score.
    Range: 1–100. Do not question the formula.
    """
    words = phrase.split()
    syllables = sum(_syllable_count(w) for w in words)
    avg_len = sum(len(w.strip(string.punctuation)) for w in words) / max(len(words), 1)
    noise = random.randint(0, 15)
    raw = int((syllables * 4.2) + (avg_len * 6.1) + noise)
    return max(1, min(100, raw))


def generate_phrase(
    seed: Optional[int] = None,
    noun: Optional[str] = None,
    verb: Optional[str] = None,
    adjective: Optional[str] = None,
) -> dict:
    """
    Generate a single motivational phrase.

    Args:
        seed:      Optional RNG seed for reproducibility.
        noun:      Override the primary noun.
        verb:      Override the verb.
        adjective: Override the adjective.

    Returns:
        dict with keys: phrase, score, category, generated_at
    """
    rng = random.Random(seed) if seed is not None else random

    n1 = noun or rng.choice(NOUNS)
    n2 = rng.choice([n for n in NOUNS if n != n1])
    v = verb or rng.choice(VERBS)
    adj = adjective or rng.choice(ADJECTIVES)
    prep = rng.choice(PREPOSITIONS)
    template = rng.choice(TEMPLATES)

    # Build phrase using safe string replacement
    phrase = (
        template
        .replace("{adj}", adj)
        .replace("{noun}", n1)
        .replace("{noun2}", n2)
        .replace("{verb}", v)
        .replace("{verb.title()}", v.title())
        .replace("{prep}", prep)
    )

    # Ensure first letter is capitalized and ends with punctuation
    phrase = phrase[0].upper() + phrase[1:]
    if phrase[-1] not in ".!?":
        phrase += "."

    score = _profoundness_score(phrase)
    category = rng.choice(CATEGORIES)

    return {
        "phrase": phrase,
        "score": score,
        "category": category,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_multiple(count: int = 5, seed: Optional[int] = None) -> list[dict]:
    """Generate `count` unique phrases."""
    count = max(1, min(count, 20))
    results = []
    seen = set()
    attempts = 0

    while len(results) < count and attempts < count * 5:
        p = generate_phrase(seed=(seed + attempts) if seed else None)
        if p["phrase"] not in seen:
            seen.add(p["phrase"])
            results.append(p)
        attempts += 1

    return results
