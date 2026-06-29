# ZENITH Backend — the HACD Naming Layer

> Every HACD is a 6-letter word. ZENITH tells you which words are worth owning.

A small, dependency-light FastAPI service that scores HACD names, surfaces the
premium ones, and gates its heavier endpoints behind the **ZEN** Stack Token.
Read-only — it never asks for a private key, seed phrase, or signature.

## Why this exists

HACD names are exactly **6 letters** drawn from a **16-letter alphabet**
(`A B E H I K M N S T U V W X Y Z` — the letters `C D F G J L O P Q R` are not
valid). That makes the entire HACD namespace finite: **16⁶ = 16,777,216** names.

Inside that space sits a tiny, ownable subset of *premium* names:

| Category | Count |
|----------|-------|
| Real English dictionary words | **1,219** |
| Palindrome words | 3 |
| Solid (one letter ×6) | 16 |
| Namespace palindromes | 4,096 |

ZENITH indexes and scores that subset. Carat Protocol scores HACD *market
rarity* (HIP-5/8/9); ZENITH scores what a name *says* — they're complementary.

## Quick start

```bash
cd zenith/backend
python3 build_dataset.py                 # regenerate data/dataset.json (already committed)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
open http://localhost:8000/docs          # interactive API docs
```

Run the tests (no network, no extra services):

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/ -q
```

## The namescore (0–100)

`app/engine.py` is pure and deterministic. Each name earns points for:

- **word** (45) — it's a real dictionary word
- **palindrome** (22) — reads the same both ways
- **repetition** (5–30) — doubles, triples, solids, mirror-halves
- **rarity** (0–18) — built from letters that are rare in the word corpus
- **structure** (0–14) — small alphabet, `ABEABE`-style mirror halves

Tiers: `common · uncommon · rare · legendary · mythic`.

## Token gating (usage-first)

ZEN is the access key, not a speculation chip. `app/gating.py` maps a public
address's ZEN balance to a tier:

| Tier | ZEN held | Unlocks |
|------|----------|---------|
| free | 0 | `/analyze`, `/validate` |
| holder | ≥ 1,000 | `/search`, `/leaderboard` |
| pro | ≥ 10,000 | `/bulk`, exports |

Gated endpoints return **HTTP 402** with a clear "how to unlock" message when
the caller's tier is too low.

### Live chain integration (one seam)

Balance lookup runs in **offline-sim** mode by default so the product is fully
demoable with zero chain access — it derives a deterministic pseudo-balance
from the address so reviewers can hit all three tiers. Set the environment
variable `ZENITH_EXPLORER_API` to point at a real Hacash explorer endpoint and
the same code path queries the live ZEN Stack Asset balance instead. No other
code changes required.

## API surface

| Method | Path | Tier | Purpose |
|--------|------|------|---------|
| GET | `/` | – | service banner |
| GET | `/health` | – | liveness |
| GET | `/meta` | – | dataset stats + alphabet |
| GET | `/validate?name=` | free | length + alphabet check |
| GET | `/analyze?name=` | free | full namescore |
| GET | `/access?address=` | – | report ZEN tier (read-only) |
| GET | `/search?contains=&starts_with=&ends_with=&min_score=` | holder | find premium names |
| GET | `/leaderboard?limit=` | holder | top names in existence |
| POST | `/bulk` | pro | score up to 200 names |

## Safety

- Never requests keys, seeds, passwords, or signatures.
- Read-only: it observes public balances, it does not move funds.
- No price, profit, or floor language anywhere in responses.
- ZEN utility described is live at launch (the engine works today).
