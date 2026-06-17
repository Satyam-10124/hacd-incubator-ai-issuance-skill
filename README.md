# HACD Incubator AI Issuance Skill

An AI-assisted issuance workflow for HACD Labs Incubator Cohort 2.

Apply to the incubator: https://hacd.it/incubator
Launchpad: https://hacd.it/launchpad

This Skill helps applicants and HACD Labs operators turn a raw project idea into a complete HACD Stack issuance package in one AI session — no coding required.

- project fit review and objective scoring
- Stack Token design with math validation
- HACD formation logic and participant flow
- Launchpad page copy
- issuer FAQ
- X / community announcement drafts
- internal review checklist
- machine-readable launch spec

The goal is not to let AI "launch a token blindly". The goal is to make HACD issuance more structured, reviewable, repeatable, and safer for builders.

## Incubator Cohort 2 Campaign

HACD Labs is running a $500 reward pool campaign for the top 10 projects that complete a full Stack Token launch through this skill. See `CAMPAIGN.md` for rules, timeline, and reward split.

## Intended users

1. Project teams applying to HACD Labs Incubator Cohort 2
2. HACD Labs reviewers preparing projects for Launchpad
3. Community builders exploring PoW-backed Stack Assets on HACD
4. AI agents that need a structured issuance workflow

## What this Skill does

- Converts a project idea into a complete issuance brief
- Helps define supply, lots, stack cost, HACD requirements, holder logic, and launch rules
- Produces Launchpad-ready copy and FAQ
- Produces X announcement drafts in HACD Labs style
- Produces a `launch_spec.json` for review and validation
- Scores submissions objectively across 5 dimensions
- Runs a brutal pre-submission review to catch every problem before it reaches HACD Labs
- Checks for missing fields, unsafe claims, and unclear economic logic

## What this Skill does not do

- It does not ask for private keys, seed phrases, wallet files, or passwords
- It does not sign transactions
- It does not guarantee launch approval
- It does not provide legal, financial, or investment advice
- It does not promise price appreciation, yield, or profits

## Repo structure

```txt
hacd-incubator-ai-issuance-skill/
├── README.md
├── CAMPAIGN.md
├── QUICKSTART.md
├── SKILL.md
├── prompts/
│   ├── google_form_to_intake.md
│   ├── project_scorer.md
│   ├── roast_mode.md
│   ├── x_thread_generator.md
│   ├── hac_cost_calculator.md
│   ├── issuer_intake.md
│   ├── launchpad_page_copy.md
│   ├── project_fit_review.md
│   ├── risk_review.md
│   ├── stack_token_design.md
│   └── x_announcement.md
├── templates/
├── examples/
│   ├── example_community_token/
│   └── example_stack_spec.json
├── scripts/
└── .github/
```

## Fast start (10 minutes)

See `QUICKSTART.md` for the full step-by-step guide. Short version:

1. Open Claude (claude.ai) or ChatGPT (chatgpt.com)
2. Load `SKILL.md` as the AI's operating instruction
3. Use `prompts/google_form_to_intake.md` to expand your application answers into a full intake form
4. Ask the AI to generate all 8 documents
5. Run the validator:

```bash
python3 scripts/validate_launch_spec.py path/to/your/launch_spec.json
```

6. Run `prompts/roast_mode.md` to catch every problem before submitting
7. Submit your package to HACD Labs

## Prompts reference

| Prompt | What it does |
|--------|-------------|
| `google_form_to_intake.md` | Expands 9 Google Form answers into the full 40-field intake form |
| `project_scorer.md` | Scores any submission 1-10 across 5 dimensions objectively |
| `roast_mode.md` | Brutal pre-submission review — finds every blocker and warning |
| `x_thread_generator.md` | Generates full X launch thread + 5 hooks from launch_spec.json |
| `hac_cost_calculator.md` | Shows participants exactly what they need at every lot level |
| `issuer_intake.md` | Guides the initial intake conversation |
| `project_fit_review.md` | Standalone fit review prompt |
| `stack_token_design.md` | Standalone stack design prompt |
| `risk_review.md` | Standalone risk and copy safety review |
| `launchpad_page_copy.md` | Standalone launchpad copy prompt |
| `x_announcement.md` | Standalone announcement prompt |

## Reference example

See `examples/example_community_token/` for a complete valid submission using the StackFire (SFR) community token test project. This is exactly what a strong submission looks like — 8 documents, passing validator, complete review checklist.

## Recommended public positioning

> HACD Labs Incubator Cohort 2 uses AI to simplify PoW-backed asset issuance on HACD.
> Builders can turn an idea into a structured Stack launch proposal in 10 minutes, while HACD Labs keeps human review over formation logic, launch quality, and ecosystem fit.

## License

To be decided by HACD Labs.
