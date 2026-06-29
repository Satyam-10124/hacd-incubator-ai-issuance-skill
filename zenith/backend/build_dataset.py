#!/usr/bin/env python3
"""Build the ZENITH naming dataset from a system dictionary.

HACD names are exactly 6 letters drawn from a 16-letter alphabet:
    A B E H I K M N S T U V W X Y Z
(the letters C D F G J L O P Q R are NOT valid).

Of the full 16^6 = 16,777,216 possible HACD names, only a tiny, finite,
ownable subset are real English words, repeated letters, palindromes, or
otherwise "premium" patterns. This script pre-computes that subset once so
the API can serve it instantly without scanning a dictionary at request time.

Output: data/dataset.json  (committed, deterministic, no network needed)

Usage:
    python3 build_dataset.py            # uses /usr/share/dict/words
    python3 build_dataset.py words.txt  # use a custom wordlist
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ALPHABET = "ABEHIKMNSTUVWXYZ"  # the canonical 16 HACD letters, sorted
ALPHA_SET = set(ALPHABET)
NAME_LEN = 6
TOTAL_NAME_SPACE = len(ALPHABET) ** NAME_LEN  # 16,777,216

DATA_DIR = Path(__file__).parent / "data"


def is_valid_hacd(name: str) -> bool:
    return len(name) == NAME_LEN and set(name) <= ALPHA_SET


def load_words(path: Path) -> list[str]:
    words: set[str] = set()
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        w = raw.strip().upper()
        if is_valid_hacd(w):
            words.add(w)
    return sorted(words)


def is_palindrome(name: str) -> bool:
    return name == name[::-1]


def repeat_signature(name: str) -> str:
    """e.g. AABBCC-style signature describing the multiplicity pattern."""
    counts = sorted(Counter(name).values(), reverse=True)
    return "".join(str(c) for c in counts)


def all_repeating(letter_runs: int) -> list[str]:
    """All names made of a single repeated letter, etc. Cheap to enumerate."""
    out = []
    if letter_runs == 1:  # AAAAAA
        out = [c * NAME_LEN for c in ALPHABET]
    return out


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/usr/share/dict/words")
    if not src.exists():
        print(f"ERROR: wordlist not found at {src}")
        sys.exit(1)

    words = load_words(src)

    # Categorize dictionary words.
    palindromes = [w for w in words if is_palindrome(w)]
    double_letter_start = [w for w in words if w[0] == w[1]]

    # Pattern catalog (computed over the full namespace, not the dictionary).
    solid = all_repeating(1)  # AAAAAA — 16 of them
    namespace_palindromes = len(ALPHABET) ** 3  # first 3 letters free, last 3 mirror

    dataset = {
        "meta": {
            "alphabet": ALPHABET,
            "alphabet_size": len(ALPHABET),
            "name_length": NAME_LEN,
            "total_name_space": TOTAL_NAME_SPACE,
            "excluded_letters": "".join(sorted(ALPHA_SET.symmetric_difference(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")))),
            "source_wordlist": str(src),
        },
        "stats": {
            "dictionary_word_names": len(words),
            "palindrome_words": len(palindromes),
            "solid_letter_names": len(solid),
            "namespace_palindromes": namespace_palindromes,
        },
        "dictionary_words": words,
        "palindrome_words": palindromes,
        "solid_letter_names": solid,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    print(f"OK: wrote {out}")
    print(f"  dictionary-word HACD names : {len(words):,}")
    print(f"  palindrome words           : {len(palindromes):,}")
    print(f"  solid-letter names         : {len(solid)}")
    print(f"  total name space           : {TOTAL_NAME_SPACE:,}")
    print(f"  sample words               : {', '.join(words[:12])}")


if __name__ == "__main__":
    main()
