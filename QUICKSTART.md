# HACD Incubator AI Skill — 10-Minute Quickstart

This guide shows you how to generate your complete 8-document launch package using any AI assistant. No coding required.

## What You Will Produce

By the end of this guide you will have:
- A complete HACD Stack issuance package ready to submit to HACD Labs
- A validated launch_spec.json with no math errors
- Launchpad-ready copy, FAQ, X announcements, and a review checklist

## Before You Start

You need:
1. Your completed Google Form answers (from hacd.it/incubator)
2. Access to Claude (claude.ai) or ChatGPT (chatgpt.com) — free accounts work
3. This repo open so you can copy file contents

---

## Step 1 — Load the Skill into Your AI (2 minutes)

Open Claude or ChatGPT and start a new conversation.

Copy the entire contents of `SKILL.md` from this repo.

Paste it into the chat with this message at the top:

```
You are the HACD Incubator AI Issuance Assistant. The following are your operating instructions. Read them fully before I give you my project details.

[paste SKILL.md contents here]

Confirm you have read and understood these instructions before I continue.
```

Wait for the AI to confirm. It should describe its role back to you.

---

## Step 2 — Give It Your Project Details (2 minutes)

Copy your Google Form answers. Then use the google_form_to_intake prompt:

Open `prompts/google_form_to_intake.md`, copy its contents, and paste it into the chat followed by your Google Form answers.

The AI will output a completed `issuer_intake_form.md` for your project.

Review it. Correct anything that is wrong or missing. Add any details the form did not cover.

---

## Step 3 — Generate All 8 Documents (3 minutes)

Once the intake form looks right, send this message:

```
Now generate the complete issuance package for this project in order:
1. incubator_fit_review.md
2. project_profile.md
3. stack_design.md
4. launch_spec.json
5. launchpad_copy.md
6. issuer_faq.md
7. x_announcement.md
8. review_checklist.md

Follow the SKILL.md templates exactly. Mark any assumptions as "Needs issuer confirmation".
```

The AI will output all 8 documents one by one. Copy each into its own file.

---

## Optional — Research Mode for live data (2 minutes)

The skill ships with a live web-research prompt. If your assistant has web search, paste
`prompts/web_research.md` and ask for current data instead of guessing:

```
Research Mode: give me a live HAC market snapshot, convert my formation cost to USD as of today,
and tell me whether my project name and ticker are already taken on the Launchpad or X.
```

It returns sourced findings tagged VERIFIED / REPORTED / ASSUMPTION. Use this for anything
time-sensitive: price, network fee, comparable projects, name availability.

## Step 4 — Validate the launch_spec.json (1 minute)

Save the `launch_spec.json` the AI generated, in the same folder as your 8 documents (the
validator cross-checks the numbers in the `.md` files against the spec).

If you have Python installed, run:

```bash
python3 scripts/validate_launch_spec.py path/to/your/launch_spec.json
```

The validator now also lints your copy for unsafe language and checks that the supply numbers in
`stack_design.md` and `launchpad_copy.md` match the spec. For your final submission, use strict
mode (warnings become failures):

```bash
python3 scripts/validate_launch_spec.py path/to/your/launch_spec.json --strict
```

You should see:

```
OK: launch spec passed basic validation
Formation cost reference: XXXX HAC + network fees
```

Two warnings about issuer_confirmed and hacd_labs_reviewed being false are expected and fine. Any ERROR means something needs fixing — the error message will tell you exactly what.

If you do not have Python, paste the launch_spec.json back into the AI and ask:

```
Check this launch_spec.json against these validation rules: 
total_supply must equal total_hacd_lots multiplied by units_per_hacd_lot. 
All required fields must be present and non-null. 
Report any errors.
```

---

## Step 5 — Run Roast Mode (1 minute)

Before you submit, get a brutal review of your package. Open `prompts/roast_mode.md`, copy it, and paste into the AI chat followed by your launch_spec.json.

Fix everything it flags. Then rerun the validator.

---

## Step 6 — Package and Submit

Create a folder named after your project ticker. Put all 8 documents plus the launch_spec.json inside. ZIP it or push it to a GitHub repo.

Submit to HACD Labs as instructed in `CAMPAIGN.md`.

## Step 7 — Actually launch on-chain

Generating documents is half the job. When your package is approved, follow
`LAUNCH_WALKTHROUGH.md` to set up a wallet, get HAC and HACD, perform the Stack on
hacd.it/launchpad, and verify formation on explorer.hacash.org.

---

## Tips

- If the AI makes up numbers you did not provide, correct them and regenerate
- If supply math does not match, tell the AI: "Fix the supply: total_supply must equal total_hacd_lots times units_per_hacd_lot"
- If the copy contains unsafe language the validator cannot catch, run roast_mode.md first
- See `/examples/example_community_token/` for a complete working example to compare against

## Reference Example

The StackFire (SFR) project in `/examples/example_community_token/` was generated using this exact workflow. Compare your output to it to check quality.

---

*10 minutes. 8 documents. One validated launch package. Good luck.*
