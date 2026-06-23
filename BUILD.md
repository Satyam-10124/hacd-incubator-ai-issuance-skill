# BUILD — one prompt, full package

This is the fastest way to use the skill. One copy-paste prompt takes you from a
raw idea to all 8 launch documents, self-reviewed, in a single AI turn. Use this
instead of running the six QUICKSTART steps by hand.

> Prefer the step-by-step version, or want to run one stage in isolation? See
> `QUICKSTART.md` and the individual prompts in `prompts/`.

---

## How to run it

1. Open Claude (claude.ai) or ChatGPT. Start a new chat.
2. Paste the entire contents of **`SKILL.md`** as your first message.
   *(In Claude Code / claude.ai with skills, you can instead invoke the
   `hacd-issuance` skill and skip this paste.)*
3. Paste the **mega-prompt below**, then fill in the `>>> YOUR PROJECT <<<` block
   with whatever you know. Unknown fields are fine — write "unsure" and the AI
   will draft a sensible default and mark it `Needs issuer confirmation`.
4. Copy each document the AI returns into its own file. To scaffold the folder and
   filenames automatically first, run:

   ```bash
   python3 scripts/new_project.py --name "Your Project" --ticker TKR \
       --type FT --lots 100 --units 10000 --cost 50
   ```

5. Validate:

   ```bash
   python3 scripts/validate_launch_spec.py project_tkr/launch_spec.json --strict
   ```

---

## The mega-prompt

```text
You are the HACD Incubator AI Issuance Assistant, operating under the SKILL.md
instructions already loaded in this conversation. Run the FULL pipeline in one
pass and return everything in a single response.

>>> YOUR PROJECT <<<
- Project name:
- Ticker (guess if unsure):
- One-sentence description:
- Category (meme / AI agent / art / RWA / stable asset / game / community / utility):
- Why does PoW / HACD make sense for this, in your own words:
- Asset type (FT / NFT / SFT / HYBRID / unsure):
- Rough supply idea (total supply, or # of HACD lots, or "unsure"):
- Stack cost per HACD in HAC (or "unsure" — Carat sits at 100; 10–50 maximizes onboarding):
- What holders can do AT LAUNCH (be honest; "nothing yet" is allowed):
- What is only planned for later:
- Founder / team / contact:
- Links (website, X) if any:
>>> END <<<

DO THIS, IN ORDER, IN ONE RESPONSE:

1. INTAKE: Expand the block above into a complete issuer_intake_form.md using the
   template structure. Use my answers as the source of truth. Never invent supply
   numbers, stack costs, or links I did not give. For anything missing, write
   "Needs issuer confirmation — [what is needed]".

2. RESOLVE SUPPLY MATH: Pick consistent numbers so that
   total_supply = total_hacd_lots × units_per_hacd_lot, and
   first_phase_hacd_lots + public_phase_hacd_lots = total_hacd_lots.
   If I gave only some of these, derive the rest and SHOW the arithmetic. If I gave
   none, propose a clean default and label it an assumption.

3. GENERATE ALL 8 DOCUMENTS, each in its own fenced code block titled with its
   filename, following the SKILL.md templates exactly:
     1) incubator_fit_review.md
     2) project_profile.md
     3) stack_design.md
     4) launch_spec.json
     5) launchpad_copy.md
     6) issuer_faq.md
     7) x_announcement.md
     8) review_checklist.md
   Rules:
   - The supply numbers in stack_design.md and launchpad_copy.md MUST match
     launch_spec.json verbatim (the validator cross-checks this).
   - launch_spec.json must follow templates/stack_launch_spec.json and pass the
     supply equation and phase-lot sum.
   - No banned language anywhere in public copy: no "guarantee(d)", "floor price",
     "risk-free", "moon", "ROI", "yield", "profit", "Nx returns", "backed value".
     Describe stack cost as a "formation cost reference", never a price floor.
   - Include "not financial advice" and a risk disclosure in the public docs.
   - Present launch utility honestly; mark future utility as planned, never current.

4. SELF-ROAST: After the 8 documents, run a brutal pre-submission review of your
   own output (math, unsafe copy, utility honesty, missing fields, terminology).
   List every issue as PROBLEM / LOCATION / FIX, then APPLY each fix inline by
   reprinting only the corrected documents. End with TOTAL ISSUES FOUND and a
   confirmation that no blockers remain.

5. CLOSE with exactly:
   "This is a draft issuance package for review. Final parameters must be confirmed
   by the issuer and HACD Labs before Launchpad publication."
```

---

## After the AI finishes

- Save each block to its filename (or into the folder `new_project.py` scaffolded).
- Run the validator in `--strict` mode. Any `ERROR` tells you exactly what to fix;
  paste the error back to the AI and ask it to correct that document.
- The two warnings about `issuer_confirmed` / `hacd_labs_reviewed` being `false`
  are expected for a draft — flip them only once those reviews actually happen.
- Then follow `LAUNCH_WALKTHROUGH.md` to take it on-chain, and submit per
  `CAMPAIGN.md`.
