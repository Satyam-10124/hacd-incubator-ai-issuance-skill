# ZENITH — the naming layer for HACD

> **Every HACD is a word. ZENITH tells you which words are worth owning.**

A complete HACD Labs Incubator Cohort 2 submission: a *usage-first* Stack Token
(**ZEN**) that gates a live engine for scoring and discovering premium HACD names.

ZENITH is built around HACD's defining constraint — every HACD name is **6
letters** from a **16-letter alphabet** (`A B E H I K M N S T U V W X Y Z`),
making exactly **16,777,216** possible names. Inside that space sit **1,219**
real English dictionary words, a few palindromes, and 16 solid names. ZENITH
indexes and scores them. The ZEN token is the key to the engine.

It is deliberately *not* a Carat clone: **Carat scores what a HACD is worth
(market rarity, HIP-5/8/9); ZENITH scores what it says (language).** Complementary.

## What's in here

```
zenith/
├── README.md              ← you are here
├── LOVABLE_PROMPT.md       ← paste-ready, pro-grade frontend build prompt
├── backend/                ← FastAPI naming engine (built, tested, runnable)
│   ├── app/                  engine.py · gating.py · main.py
│   ├── data/dataset.json     1,219 dictionary-word HACDs, generated offline
│   ├── build_dataset.py      regenerates the dataset from a system wordlist
│   ├── tests/                16 passing tests, no network needed
│   ├── requirements.txt · Dockerfile · README.md
└── submission/             ← the 9 incubator submission documents
    ├── issuer_intake_form.md
    ├── incubator_fit_review.md
    ├── project_profile.md
    ├── stack_design.md
    ├── launch_spec.json      ← passes the validator with 0 errors
    ├── launchpad_copy.md
    ├── issuer_faq.md
    ├── x_announcement.md
    └── review_checklist.md
```

## Run the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
open http://localhost:8000/docs
# tests:
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/ -q
```

## Validate the submission

From the repo root:

```bash
python3 scripts/validate_launch_spec.py zenith/submission/launch_spec.json
```

Output: `OK: launch spec passed validation` (two draft warnings are expected and
correct — `issuer_confirmed` / `hacd_labs_reviewed` must stay false until a human
and HACD Labs actually sign off).

## The supply math (deliberately thematic)

| Field | Value |
|-------|-------|
| Total supply | 16,777,216 ZEN = 16⁶ = every possible HACD name |
| HACD lots | 256 = 16² |
| Units per lot | 65,536 = 16⁴ |
| Genesis | 32 reserved → 224 public (reserved-first, like the live benchmark) |
| Stack cost | 50 HAC per HACD (12,800 HAC total formation reference) |

`256 × 65,536 = 16,777,216` ✓  ·  `32 + 224 = 256` ✓

## Access tiers (usage-first)

| Tier | ZEN held | Unlocks |
|------|----------|---------|
| free | 0 | analyze any single name |
| holder | ≥ 1,000 | premium search + namescore leaderboard |
| pro | ≥ 10,000 | bulk scoring + exports |

Read-only gating. ZENITH never asks for a key, seed phrase, or signature.

## Safety

No price/profit/floor language anywhere. The namescore is a linguistic opinion,
not a valuation. ZEN is a utility access token, not an investment. Not financial
advice. Final Launchpad parameters must be verified by HACD Labs.
