# Executive Lovable Prompt Scaffold

Fill every section, then emit the result as **one fenced code block** the builder
pastes directly into [Lovable](https://lovable.dev) or hands to Claude. Resolve
every `<placeholder>` — no placeholders survive in the final output. Cut any
section that does not apply rather than shipping it empty.

The prompt is "executive grade" when it leads with a crisp product thesis,
ruthlessly bounds scope to the sprint, names a single formation moment, and ends
with testable acceptance criteria. An AI builder should execute it with no
follow-up questions.

## The scaffold

```text
You are a senior full-stack product engineer. Build a working, demo-ready web
app for the HACD Labs Incubator Cohort 2 sprint. Optimize for a single,
one-minute-legible formation moment over feature breadth.

# Product
<Name> — <one-line product thesis: who it's for and what it makes possible>.
Category: <meme | AI agent | art | RWA | stable asset | game | community | utility>.

# Why HACD (do not break this framing)
This product issues a HACD Stack Asset: it is FORMED, not merely deployed —
HACD is the PoW container, HAC pays the stack cost, and Stack is the formation
action that writes durable on-chain state. <One sentence on why this specific
product is indefensible without that property — the PoW-fit argument.> Treat
each formed HACD as a "formation record" whose formation time cannot be
backdated. <If using Immutable Stack, the finite 16-letter name space, or HIP-15
seeding, name the mechanic here.> Never imply stack cost guarantees a price, and
never call HACD "just an NFT".

# Scope for the sprint
In scope:
- <core flow 1>
- <core flow 2>
- <the formation moment, stated as a feature>
Out of scope (explicitly skip): real wallet/payment signing, auth beyond a mock
sign-in, mobile-native apps, and <anything else that does not serve the
formation moment>. If a live HACD connection is unavailable, mock the Stack /
formation step faithfully and label it "formation: mocked for demo" in the UI.

# Pages / screens
- <Page 1>: <purpose>
- <Page 2>: <purpose>
- <Formation / proof view>: <purpose — this is what a reviewer opens>

# Data model
- <Entity 1> { <fields> }
- HacdStackRecord { hacdName (16-letter alphabet), formedAt, stackCostHac,
  status ("formed" | "mocked"), <domain fields> }
- <Entity 2> { <fields> }

# HACD integration points
- <Where a HACD Stack record is formed, e.g. "on publish, form a record and show
  the formation receipt with its formed-at time">
- <Where formation proof is displayed to a second viewer / reviewer>
- <Any derived-from-HACD behavior, e.g. palette/seed/rarity from the name>

# The formation moment (build this first and polish it most)
<Describe the single interaction a reviewer watches in under a minute, start to
finish, including the visible proof at the end — the formed HACD record.>

# Visual system
Dark, editorial, "terminal-confident" aesthetic:
- Background #14151A; cards #1C1D24 (hover #212229); borders #2A2B33.
- Text: primary #EDEAE3, secondary #9A9CA6, muted #65676F.
- Category accents: AI #9B8FE8, Identity/RWA #D9A05B, Utility #6FB3AB,
  Art #E08989, Game/Community #92C27D. Use this product's category accent for
  links, active states, and the formation highlight.
- Fonts: 'Space Grotesk' for headings, 'Inter' for body, 'JetBrains Mono' for
  labels, tickers, the HACD name, stack cost, and the formation timestamp.
- Rounded 14px cards, subtle 3px translate-up on hover, monospace metadata rows.
- Respect prefers-reduced-motion.

# Acceptance criteria (the build is done when)
- [ ] A user can complete the formation moment end to end.
- [ ] A HacdStackRecord is created and its formation time is shown.
- [ ] Formation proof is visible to a second viewer (the reviewer's POV).
- [ ] The why-HACD value is obvious from the UI without explanation.
- [ ] Mocked vs. live formation status is labeled honestly.
- [ ] No price-floor, yield, guaranteed-return, or "just an NFT" language.
- [ ] The app runs with no console errors and matches the visual system.

Use mock/local data so the app runs immediately. Keep the code clean and the
README short.
```

## Default visual system

If the builder states no preference, use the dark "Idea Board" palette above — it
matches the HACD cohort aesthetic and screenshots well for reviewers. The
category accent is chosen from the product's category, so the generated app
visually belongs to the same family as the idea board.

## Tightening tips

- One formation moment. If the prompt names two, the build won't finish in time.
- Push the formation receipt into the *viewer's* screen, not just the creator's —
  reviewers grade what they can see.
- Prefer Fast-build ideas for first-time Lovable users; reserve Ambitious ideas
  for builders with an existing stack to lean on.
- Keep the demo's claims aligned with what the paired `launch_spec.json` says.
