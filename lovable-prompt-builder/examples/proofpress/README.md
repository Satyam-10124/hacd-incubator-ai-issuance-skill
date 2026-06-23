# Worked Example — ProofPress (PRSS)

A complete worked output of the HACD Lovable Prompt Builder skill for one
idea-board concept: **ProofPress (`PRSS`)** — immutable authorship timestamps for
articles, research notes, and citizen journalism.

It shows what the skill produces end to end, so a builder can see the target
before generating their own.

## Inputs used

- **Concept / ticker:** `PRSS` (ProofPress), resolved from
  [`../../prompts/idea_board.md`](../../prompts/idea_board.md).
- **Category:** utility.
- **Why HACD:** authorship disputes need an unfakeable "published first"; HACD's
  formation time is exactly that proof and cannot be backdated.
- **Formation moment:** an author hits Publish, a HACD Stack record is formed
  with a timestamp and content hash, and a *second* viewer opens the public proof
  page and sees the unfakeable "formed at" time.

## Scope summary

ProofPress lets writers stamp a piece of writing with a HACD formation record the
moment they publish, so authorship and "published first" are provable later by
anyone. Category: utility. PoW-fit read: **Strong** — a plain database timestamp
can be edited or backdated; a PoW-formed record cannot, which is the entire
product. The formation moment is one minute: publish → receipt → independent
verification.

## Files

- [`lovable-prompt.md`](lovable-prompt.md) — the executive Lovable prompt this
  skill generated. Paste it into Lovable or hand it to Claude to build the app.
- [`sprint-plan.md`](sprint-plan.md) — the build mapped to the `CAMPAIGN.md`
  window.

## How to reuse

1. Load `../../SKILL.md` into Claude or ChatGPT (or run it via Claude Code).
2. Give it your own concept or an idea-board ticker.
3. Take the generated prompt block and paste it into Lovable.
4. Follow the sprint plan, then pair the demo with the 8-document issuance
   package from the root `SKILL.md` and validate `launch_spec.json`.

> This example is illustrative. Replace ProofPress with your real project, and
> keep every claim honest — no invented metrics, payouts, or price language.
