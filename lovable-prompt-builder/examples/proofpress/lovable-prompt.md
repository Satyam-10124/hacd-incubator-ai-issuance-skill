# ProofPress — Generated Executive Lovable Prompt

Paste the block below directly into [Lovable](https://lovable.dev), or hand it to
Claude, to build the ProofPress demo.

```text
You are a senior full-stack product engineer. Build a working, demo-ready web
app for the HACD Labs Incubator Cohort 2 sprint. Optimize for a single,
one-minute-legible formation moment over feature breadth.

# Product
ProofPress — a publishing tool for writers, researchers, and citizen
journalists that stamps every piece with an unfakeable "published first" proof
the moment it goes live.
Category: utility.

# Why HACD (do not break this framing)
ProofPress issues a HACD Stack Asset: each proof is FORMED, not merely deployed —
HACD is the PoW container, HAC pays the stack cost, and Stack is the formation
action that writes durable on-chain state. Authorship disputes hinge on who
published first, and a normal database timestamp can be edited or backdated at
will, so it proves nothing. A HACD formation record is mined and Stacked, so its
formation time cannot be backdated and the proof cannot be silently altered. That
non-repudiable formation time is the entire product; without it, ProofPress is
just another CMS. Never imply stack cost guarantees a price, and never call HACD
"just an NFT".

# Scope for the sprint
In scope:
- Write/paste an article in a simple editor.
- Publish: form a HACD Stack record with a formation timestamp and a content hash.
- A public, shareable proof page anyone can open to verify "formed at".
Out of scope (explicitly skip): real wallet/payment signing, auth beyond a mock
sign-in, comments, rich media uploads, and mobile-native apps. If a live HACD
connection is unavailable, mock the Stack / formation step faithfully and label
it "formation: mocked for demo" in the UI.

# Pages / screens
- Editor: title + body fields and a single Publish button.
- Library: the author's published pieces, each showing its HACD name and
  formation time.
- Proof page (public): the canonical authorship receipt for one piece — content
  hash, HACD name, formation timestamp, and a "verify" affordance. This is the
  page a reviewer opens.

# Data model
- Article { id, title, body, contentHash, authorHandle }
- HacdStackRecord { hacdName (16-letter alphabet), formedAt, stackCostHac,
  status ("formed" | "mocked"), contentHash, articleId }

# HACD integration points
- On Publish, compute a content hash and form a HacdStackRecord; show the
  formation receipt inline immediately after publishing.
- The public proof page renders the formation receipt for any viewer, not just
  the author — this is where "published first" becomes provable.
- Re-publishing edited content forms a NEW record, making edits visible rather
  than silent (reinforcing tamper-evidence).

# The formation moment (build this first and polish it most)
An author types a headline, clicks Publish, and instantly sees a formation
receipt with a monospace HACD name and a "formed at" timestamp. They copy the
public proof link, open it in a fresh tab (the reviewer's point of view), and the
same unfakeable formation time and content hash appear — proving authorship to
someone who was not the author. The whole flow takes under a minute.

# Visual system
Dark, editorial, "terminal-confident" aesthetic:
- Background #14151A; cards #1C1D24 (hover #212229); borders #2A2B33.
- Text: primary #EDEAE3, secondary #9A9CA6, muted #65676F.
- Utility category accent #6FB3AB for links, active states, and the formation
  highlight.
- Fonts: 'Space Grotesk' for headings, 'Inter' for body, 'JetBrains Mono' for
  labels, the HACD name, the content hash, and the formation timestamp.
- Rounded 14px cards, subtle 3px translate-up on hover, monospace metadata rows.
- Respect prefers-reduced-motion.

# Acceptance criteria (the build is done when)
- [ ] An author can write, publish, and get a formation receipt in one flow.
- [ ] A HacdStackRecord is created with a formation timestamp and content hash.
- [ ] The public proof page shows the same receipt to a second viewer.
- [ ] Editing then re-publishing forms a new, visible formation record.
- [ ] The why-HACD value ("can't be backdated") is obvious from the proof page.
- [ ] Mocked vs. live formation status is labeled honestly in the UI.
- [ ] No price-floor, yield, guaranteed-return, or "just an NFT" language.
- [ ] The app runs with no console errors and matches the visual system.

Use mock/local data so the app runs immediately. Keep the code clean and the
README short.
```
