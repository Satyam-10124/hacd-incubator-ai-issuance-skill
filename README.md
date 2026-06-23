# HACD Incubator AI Issuance Skill

> **Bitcoin proved PoW for money. HACD brings PoW to assets.**

An AI-assisted issuance workflow for the HACD Labs Incubator Cohort 2 campaign.  
Turn a raw project idea into a complete, validated HACD Stack Token launch package — in one AI session, no coding required.

**Apply:** https://hacd.it/incubator  
**Launchpad:** https://hacd.it/launchpad  
**Campaign rules + $500 reward pool:** see `CAMPAIGN.md`

---

## What this is

This repo is an AI skill — a set of structured prompts and templates you load into Claude or ChatGPT. Once loaded, the AI becomes a HACD Stack issuance expert that knows the full Hacash ecosystem, the correct terminology, the supply math rules, and every safety check required before a project can go live on the Launchpad.

It generates 8 documents per project. It validates the math. It self-reviews for unsafe claims. It scores submissions so HACD Labs can rank them objectively.

```
You give it:  a project idea + 9 Google Form answers
It gives you: 8 complete launch documents, validated and review-ready
Time:         under 10 minutes
```

---

## Live example projects

Two complete working packages are included in this repo. Both pass the validator with no errors.

| Project | Ticker | Type | Lots | Supply | Stack Cost | Folder |
|---------|--------|------|------|--------|------------|--------|
| StackFire | SFR | FT | 100 | 1,000,000 | 50 HAC | `examples/example_community_token/` |
| HacashBuilders | BUILD | HYBRID | 500 | 10,000,000 | 50 HAC | `hacashbuilders/` |

These are not mockups. Each folder contains all 8 required documents. Run the validator on either one:

```bash
python3 scripts/validate_launch_spec.py examples/example_community_token/launch_spec.json
python3 scripts/validate_launch_spec.py hacashbuilders/launch_spec.json
```

---

## Incubator Cohort 2 — $500 reward pool

Campaign open: 20 June 2026  
Campaign close: 27 June 2026  
Winners announced: 29 June 2026

Top 3 projects that launch on hacd.it/launchpad win from the prize pool:

| Place | Reward |
|-------|--------|
| 1st | $250 |
| 2nd | $150 |
| 3rd | $100 |

See `CAMPAIGN.md` for full rules, judging criteria, and submission format.

---

## Fast start — 10 minutes

Full guide in `QUICKSTART.md`. Short version:

**Step 1 — Load the skill**
Open claude.ai or chatgpt.com. Paste the contents of `SKILL.md` as your first message.

**Step 2 — Expand your application**
Paste `prompts/google_form_to_intake.md` + your 9 Google Form answers. The AI expands them into a full 40-field intake form automatically.

**Step 3 — Generate all 8 documents**
Tell the AI: *"Generate all 8 documents using this intake form."*

**Step 4 — Validate**
```bash
python3 scripts/validate_launch_spec.py your_project/launch_spec.json
```

**Step 5 — Self-review**
Paste `prompts/roast_mode.md` + all 8 documents. Fix every issue it finds.

**Step 6 — Submit**
Send your complete package to HACD Labs via hacd.it/incubator.

---

## Use with Claude Code (ccr)

If you have Claude Code Router installed:

```bash
ccr start
ccr code "Load the system prompt from prompts/acp_agent_system_prompt.md and help me design a Stack Token for [your project name] with [N] lots"
```

The ACP agent system prompt at `prompts/acp_agent_system_prompt.md` contains full Hacash ecosystem knowledge including live reference data from Carat Protocol, HAC market links, wallet and explorer links, and real stack cost benchmarks.

---

## Prompts reference — 13 prompts total

| Prompt | What it does |
|--------|-------------|
| `acp_agent_system_prompt.md` | Full ACP / Claude Code agent system prompt with live Hacash ecosystem knowledge |
| `web_research.md` | **Research Mode** — live web search with source citations and VERIFIED/REPORTED/ASSUMPTION tagging |
| `google_form_to_intake.md` | Expands 9 Google Form answers into the full 40-field intake form |
| `project_scorer.md` | Scores any submission 1–10 across 5 weighted dimensions |
| `roast_mode.md` | Brutal pre-submission review — finds every blocker and warning |
| `x_thread_generator.md` | Generates 7-tweet launch thread + teaser + one-liner + 3 hooks |
| `hac_cost_calculator.md` | Participation cost table at every lot level + FAQ additions |
| `issuer_intake.md` | Guided intake conversation for initial project capture |
| `project_fit_review.md` | Standalone incubator fit review |
| `stack_token_design.md` | Standalone Stack Token design and supply math |
| `risk_review.md` | Standalone copy safety and risk disclosure review |
| `launchpad_page_copy.md` | Standalone Launchpad page copy generator |
| `x_announcement.md` | Standalone X announcement drafts |

## Key reference docs

| File | What it is |
|------|-----------|
| `ECOSYSTEM.md` | **Single source of truth** for every Hacash fact, link, benchmark, and campaign number. Change facts here first. |
| `LAUNCH_WALKTHROUGH.md` | Step-by-step on-chain guide: wallet → get HAC → get HACD → submit → Stack → verify |
| `schema/launch_spec.schema.json` | JSON Schema for `launch_spec.json` (editor + CI validation) |

## Validator — now does more than math

`scripts/validate_launch_spec.py` checks structure, enums, the supply equation, the phase-lot
sum, **cross-document consistency** (numbers in the `.md` files must match the spec), and runs a
**negation-aware copy-safety linter** that flags unsafe promo language without false-flagging
risk disclosures.

```bash
python3 scripts/validate_launch_spec.py your_project/launch_spec.json            # draft check
python3 scripts/validate_launch_spec.py your_project/launch_spec.json --strict   # final / CI check
python3 scripts/validate_launch_spec.py your_project/launch_spec.json --no-docs  # JSON only
```

Every `launch_spec.json` in the repo is validated automatically by GitHub Actions on push and PR
(`.github/workflows/validate.yml`).

---

## Repo structure

```txt
hacd-incubator-ai-issuance-skill/
├── README.md
├── ECOSYSTEM.md             ← single source of truth: facts, links, benchmarks, campaign
├── CAMPAIGN.md              ← campaign rules, reward pool, timeline
├── QUICKSTART.md            ← 10-minute document-generation guide
├── LAUNCH_WALKTHROUGH.md    ← on-chain guide: wallet → HAC → HACD → Stack → verify
├── SKILL.md                 ← core AI operating instructions
├── LICENSE                  ← MIT
├── prompts/                 ← 13 prompts incl. web_research.md (see table above)
├── templates/               ← blank document templates
├── schema/
│   └── launch_spec.schema.json   ← JSON Schema for launch_spec.json
├── examples/
│   ├── example_community_token/   ← StackFire (SFR) — FT reference
│   └── example_stack_spec.json
├── hacashbuilders/          ← HacashBuilders (BUILD) — FT+NFT reference
├── lovable-prompt-builder/  ← companion skill: idea → executive Lovable demo prompt
│   ├── SKILL.md
│   ├── prompts/             ← idea_board, pow_fit_check, sprint_plan
│   ├── templates/           ← lovable_prompt_template
│   └── examples/proofpress/ ← worked example (PRSS)
├── hacashbuilders/          ← HacashBuilders (BUILD) — HYBRID reference
├── scripts/
│   └── validate_launch_spec.py    ← structure + math + cross-doc + copy-safety linter
└── .github/
    └── workflows/validate.yml     ← CI: validates every spec on push/PR
```

---

## Companion skill — Lovable Prompt Builder

The issuance skill produces your launch *documents*. The companion
[`lovable-prompt-builder/`](lovable-prompt-builder/) skill produces your demo
*app*: it turns the same idea into an executive-grade
[Lovable](https://lovable.dev) build prompt you paste into Lovable (or hand to
Claude) to ship a working demo a reviewer can watch run in under a minute.

```txt
Project idea ─▶ lovable-prompt-builder ─▶ executive Lovable prompt ─▶ working demo app
                                                                   └─▶ pairs with the 8-doc issuance package
```

It ships the full Cohort 2 idea board (20 vetted Stack Asset concepts), a
PoW-fit check, a sprint plan keyed to `CAMPAIGN.md`, the fill-in prompt scaffold,
and a complete worked example (ProofPress). Load
[`lovable-prompt-builder/SKILL.md`](lovable-prompt-builder/SKILL.md) the same way
you load the root `SKILL.md`, then give it your idea or an idea-board ticker.

---

## Hacash ecosystem links

| Resource | Link |
|----------|------|
| Launchpad | hacd.it/launchpad |
| Incubator | hacd.it/incubator |
| Wallet | wallet.hacash.org |
| Explorer | explorer.hacash.org |
| Buy HACD | hacash.org/get |
| Mine HACD | hacash.org/mining-HACD |
| HACD Marketplace | sea.hacash.diamonds |
| HAC on CoinEx | coinex.com/en/info/HAC |
| White Paper | hacd.it/hacash_diamond.pdf |
| Lite Paper | hacd.it/bring_pow_to_everything.pdf |
| HACD Labs Twitter | x.com/hacdlabs |
| HACD Labs Discord | discord.gg/PZEEm6Jtgd |
| Community forum | hacashtalk.com |

---

## What the Skill does not do

- Does not ask for private keys, seed phrases, or wallet passwords
- Does not sign transactions
- Does not guarantee Launchpad approval
- Does not provide legal, financial, or investment advice
- Does not promise price appreciation, yield, or profits

---

## License

MIT — see `LICENSE`. Fork it, adapt it, build with it.
