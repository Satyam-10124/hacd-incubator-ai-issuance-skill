# ZENITH — Lovable Frontend Build Prompt

Paste everything inside the code fence below into Lovable as your build prompt.
It is written to produce a production-grade, aesthetic site wired to the ZENITH
backend API. After the first build, use the follow-up prompts at the bottom to
refine.

> Before you start: deploy the backend (see `backend/README.md`) and copy its
> public URL. Replace `https://YOUR-BACKEND-URL` everywhere below with it. For a
> first pass you can point at a local tunnel or paste the URL when Lovable asks
> for the API base.

---

```text
Build a production-grade, single-page web app called ZENITH — "the naming layer for HACD."

POSITIONING
ZENITH scores HACD blockchain names. A HACD name is exactly 6 letters drawn from a fixed 16-letter alphabet: A B E H I K M N S T U V W X Y Z (the letters C D F G J L O P Q R are NOT allowed). There are exactly 16,777,216 possible names. ZENITH gives any name a 0–100 "namescore" and surfaces the rare premium names. The tagline is: "Every HACD is a word. ZENITH tells you which words are worth owning."

This is a real product for a blockchain incubator competition. It must look like a top-tier crypto-infra product (think Linear, Vercel, Stripe, Phantom, Rainbow) — not a template. Restraint over decoration. It must feel fast, precise, and expensive.

TECH
- React + Vite + TypeScript + Tailwind CSS.
- shadcn/ui for primitives (button, input, card, badge, tooltip, tabs, skeleton, sonner toasts, dialog).
- framer-motion for tasteful micro-animations only (fades, slides ≤ 250ms, number count-ups, score ring fill). No bouncing, no parallax circus.
- lucide-react for icons.
- All API calls go to a single configurable base URL. Create src/lib/api.ts that reads VITE_API_BASE (default "https://YOUR-BACKEND-URL"). Centralize fetch logic with typed responses and graceful error handling (toast on failure, never a white screen).

VISUAL IDENTITY (this is the most important part — make it genuinely beautiful)
- Dark, premium, "deep observatory at night" theme. Background: near-black with a very subtle radial gradient from #0A0A0F to #07070A. Add an extremely faint dot-grid or noise texture at ~3% opacity. No pure black, no pure white.
- Accent: a luminous gem/cyan-violet system. Primary accent #7C5CFF (violet), secondary #22D3EE (cyan), with a soft glow. Use a subtle violet→cyan gradient ONLY on the wordmark, the score ring, and primary CTAs. Everywhere else stay monochrome + one accent.
- Typography: a refined geometric/grotesk sans for UI (Inter or General Sans), and a MONOSPACE font (JetBrains Mono or Geist Mono) for every HACD name, score number, and code-like value. HACD names must always render in mono, uppercase, letter-spaced — they should look like minted artifacts.
- Tier color system, used consistently for badges and the score ring:
  common = slate/gray, uncommon = green, rare = cyan, legendary = violet, mythic = gold/amber with a soft glow.
- Generous whitespace, 1px hairline borders at low opacity (#FFFFFF14), soft shadows, rounded-2xl cards. Subtle inner glow on the hero. Everything should feel calm and high-contrast where it matters.
- Fully responsive, mobile-first, accessible (focus rings, aria labels, prefers-reduced-motion respected).

PAGE STRUCTURE (single scroll, with a sticky minimal top nav: ZENITH wordmark left; links "Analyze / Search / Leaderboard / About"; a small "Connect address" pill on the right)

1) HERO
- Big wordmark "ZENITH" with the gradient, and beneath it the tagline.
- One-line subhead: "Score any HACD name. Discover the 1,219 that are real words — and the handful that are legendary."
- The centerpiece is a large, focused SEARCH/ANALYZE INPUT: a single 6-character field styled like a premium OTP / license-plate input — six individual mono character cells, uppercase, that only accept the 16 valid letters and visibly reject invalid ones (cell flashes red + a tiny tooltip "C is not a HACD letter"). A primary "Analyze" button with the gradient.
- Below the input, a live ticker line of small stats pulled from GET /meta: "16,777,216 possible names · 1,219 dictionary words · 16 solid names · 6-letter / 16-letter alphabet". Animate the big number counting up once on load.

2) ANALYZE RESULT (appears in place / scrolls into view after analyzing)
- Call GET /analyze?name=XXXXXX.
- Show a large circular SCORE RING (animated fill, 0–100) colored by tier, with the score number count-up in the center and the tier label (e.g. "LEGENDARY") beneath it.
- The name itself displayed huge in mono, uppercase, letter-spaced, with a subtle gem-shimmer if tier is mythic/legendary.
- A row of TAG BADGES (dictionary-word, palindrome, solid, rare-letters, mirror-half, etc.) each with an icon and tier-appropriate color.
- A "Why this score" panel listing the reasons[] array as clean bullet rows, each with a check/sparkle icon.
- A horizontal breakdown bar showing the 5 components (word / palindrome / repetition / rarity / structure) as a segmented stacked bar with labels and point values, animated on reveal.
- If the API returns valid=false, show a tasteful inline error card explaining the reason (e.g. wrong length / invalid letter) instead of a score — never a crash.
- A subtle "Share" button that copies a link.

3) SEARCH (HOLDER-GATED)
- A search panel with inputs: contains, starts with, ends with, min score (slider 0–100), and a results limit. Calls GET /search with those params + the connected address.
- Results render as a responsive grid of "name cards": mono name, small score ring or score pill, tier badge, top 1–2 tags. Hover lifts the card slightly with a soft glow. Clicking a card loads it into the Analyze view at the top.
- IMPORTANT GATING UX: if no address is connected OR the API returns HTTP 402, do NOT show an ugly error. Show a beautiful "locked" overlay state on the panel: a frosted-glass blur over sample results, a lock icon, and a message: "Search is a Holder feature. Stack ≥ 1,000 ZEN to unlock." with a button "How to get ZEN" linking to the HACD Launchpad. Read the 402 JSON body to display the user's current tier and balance ("You hold 240 ZEN · need 1,000").

4) LEADERBOARD (HOLDER-GATED, same gating UX)
- Calls GET /leaderboard?limit=25 with the address.
- A refined ranked table: rank, mono name, tier badge, score (with a tiny inline bar), tags. Top 3 rows get a subtle medal accent (gold/silver/bronze hairline). Smooth row stagger animation on load. Same frosted "locked" state if not a holder.

5) CONNECT ADDRESS (drawer/dialog triggered by the nav pill)
- A simple input for a public HACD/Hacash address (read-only — make this explicit). On submit, call GET /access?address=XXX and store the returned { zen_balance, tier, source } in app state (context or zustand).
- Show the resulting tier as a small colored pill in the nav ("PRO · 12,076 ZEN"). If source === "offline-sim", show a tiny muted "demo" tag with a tooltip: "Simulated balance for preview — live balances read from the Hacash explorer when configured."
- Display a permanent, reassuring micro-copy near the input: "Read-only. ZENITH never asks for your private key, seed phrase, or signature." This is a trust feature — make it visible, not hidden.

6) ABOUT / FOOTER
- A compact "How the namescore works" section: 5 small cards for the 5 scoring dimensions with a one-line explanation each.
- A "ZENITH vs Carat" one-liner: "Carat scores what a HACD is worth. ZENITH scores what it says." (Be respectful — they're complementary.)
- Honest disclosure block in muted text: "ZEN is a utility access token, not an investment. The namescore is a linguistic opinion, not a valuation or financial advice. Built for HACD Labs Incubator Cohort 2."
- Footer with the ZENITH wordmark and links to the HACD Launchpad, Explorer, and the project's X.

INTERACTION + POLISH REQUIREMENTS
- Every async state has a skeleton loader, never a layout shift.
- Number count-ups on score and stats (respecting prefers-reduced-motion).
- Keyboard: Enter in the hero input triggers Analyze; the 6-cell input auto-advances and supports paste of a full 6-letter name.
- Input only permits the 16 valid letters; typing an invalid letter gives instant inline feedback.
- All toasts via sonner. All errors are friendly and on-brand.
- Add real, tasteful empty states (e.g. "No premium names match — try a broader filter").
- Ship clean component structure: components/, lib/api.ts, hooks/, and a types.ts mirroring the API responses below.

API CONTRACT (build typed clients for these — base URL = VITE_API_BASE)
- GET /meta -> { alphabet, alphabet_size, name_length, total_name_space, dictionary_word_names, palindrome_words, solid_letter_names, namespace_palindromes }
- GET /validate?name= -> { name, valid, reason }
- GET /analyze?name= -> { name, valid, score, tier, breakdown:{word,palindrome,repetition,rarity,structure}, tags:[], reasons:[], is_dictionary_word, is_palindrome, repeat_signature }
- GET /access?address= -> { address, zen_balance, tier, source }   // tier ∈ free|holder|pro
- GET /search?contains=&starts_with=&ends_with=&only_words=true&min_score=&limit=&address= -> { count, tier, results:[analyze-shaped] }   // 402 if under-tier
- GET /leaderboard?limit=&address= -> { tier, results:[analyze-shaped] }   // 402 if under-tier
- On 402, the JSON body is { detail:{ error, message, your_tier, your_zen_balance, required_tier, how_to_unlock } } — use it to render the locked state.

SEED THE DEMO
Preload the hero with the example name "ZENITH" already analyzed (score ~51, tier "rare") so the page looks alive on first paint. Show "KAKKAK" and "XXXXXX" as featured mythic examples somewhere tasteful.

DELIVER a polished, cohesive, single-page experience. Prioritize visual quality, typographic precision, and smooth micro-interactions. This needs to win a design-conscious crypto audience on first impression.
```

---

## Follow-up refinement prompts (use after the first build)

1. **Tighten the hero:** "Make the 6-cell name input larger and more central, like a premium license-plate / OTP field. Add a faint animated gem-glow behind it that intensifies slightly as the user types a valid name. Reduce everything else competing with it above the fold."

2. **Score ring polish:** "Animate the score ring with a smooth 800ms ease-out fill on reveal, a soft outer glow matching the tier color, and a subtle conic-gradient stroke. The number in the center should count up in sync."

3. **Locked-state beauty:** "Make the holder-gated locked overlay genuinely beautiful: frosted glass blur over faded sample result cards, a centered lock with the violet→cyan accent, the user's live tier/balance from the 402 body, and a clear 'Stack ZEN to unlock' CTA. It should look intentional, like a Stripe paywall, not an error."

4. **Mobile pass:** "Audit the entire layout on a 390px viewport. The hero input, score ring, search grid, and leaderboard table must all be flawless and thumb-friendly. Collapse the nav into a clean sheet menu."

5. **Brand finish:** "Add a custom favicon and OG image using the ZENITH wordmark on the dark gradient. Set the page title to 'ZENITH — the naming layer for HACD' and a proper meta description. Add a subtle loading state on first paint."

---

## Backend connection checklist

- [ ] Deploy `zenith/backend` (Docker, Render, Railway, Fly, or a tunnel for demo).
- [ ] Confirm `GET /health` returns `{"status":"ok"}` from the public URL.
- [ ] In Lovable, set `VITE_API_BASE` to that URL (project env or hardcode in `src/lib/api.ts`).
- [ ] CORS is already open in the backend (`allow_origins=["*"]`), so the browser calls will work.
- [ ] Optional: set `ZENITH_EXPLORER_API` on the backend to switch token-gating from demo balances to live Hacash explorer balances.
