# Prompt: PoW-Fit Check

Use this before generating a Lovable prompt. It answers one question:

> Could a plain token contract — or a normal database row — power this whole
> demo with no real loss? Or does it genuinely need a PoW-mined, costly-to-fake
> HACD underneath it?

## How to score

Read the project's why-HACD claim, then assign a fit tier and justify it in one
or two sentences. Be honest — a weak fit told plainly helps the builder more than
flattery.

- **Exceptional** — the project is meaningless without HACD's tamper-evidence.
  Removing HACD removes the product. (e.g. AI agent reputation that must not
  silently reset; security-device service history.)
- **Strong** — HACD's finite 16-letter name space or Immutable Stack is the core
  mechanic. (e.g. name-space settlement game; post-publication-locked fiction.)
- **Good** — HACD adds real, defensible value, but a determined team could fake a
  weaker version elsewhere. (e.g. authorship receipts; attendance stamps.)
- **Niche** — it works, but the PoW-fit argument is thin. Only pick it if the
  formation moment is exceptionally clear and visual.

## What strong PoW-fit looks like

At least one of these is true and *visible in the demo*:

- Needs credible asset origin / costly-to-fake formation.
- Benefits from scarce HACD containers or the finite name space.
- Benefits from visible on-chain formation progress.
- Benefits from a durable, non-repudiable formation history / timestamp.
- Benefits from community participation around Stack lots.
- Benefits from immutability after formation (Immutable Stack).

## What weak PoW-fit looks like

- No reason to use HACD beyond "it's on-chain".
- Pure price speculation; utility depends only on future promises.
- The "formation" step is invisible to the reviewer.
- A plain ERC-20-style deploy would do the same job.

## If the fit is weak

Do one of:

1. Sharpen the angle so a HACD property becomes load-bearing (e.g. make the
   formation timestamp the actual proof users rely on).
2. Suggest a stronger-fit idea-board concept in the same category from
   `idea_board.md`.
3. Tell the builder plainly that the demo will be hard to defend on PoW-fit, and
   that the formation moment must carry it.

## Output

Return: the fit tier, a one-sentence justification, and — if weak — the sharper
angle or alternative. Then proceed to pick the single formation moment for the
Lovable prompt.
