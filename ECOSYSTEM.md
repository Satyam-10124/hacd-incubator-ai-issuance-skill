# Hacash Ecosystem — Single Source of Truth

> This file is the canonical reference for every fact, link, number, and benchmark used across the skill.
> All prompts, the README, CAMPAIGN.md, and the ACP system prompt should defer to this file.
> **If a fact changes, change it here first, then propagate.** Do not hardcode these values elsewhere.

Last verified: 2026-06-17. Facts marked **[VERIFY LIVE]** change over time — confirm with a web search or the explorer before relying on them in a launch.

---

## The Three PoW Coins

**HAC** — primary currency. Divisible to 10^248. No hard cap (supply responds to network activity). Used for Stack costs, network fees, and bidding on new HACD. **[VERIFY LIVE]** trades on CoinEx, Vindax, Dex-trade.

**HACD** — the PoW NFT / asset container. Each HACD is a unique 6-letter combination from the 16 letters `W T Y U I A H X V M E K B S Z N`. Total possible: 16^6 = **16,777,216**. Every HACD requires mining AND HAC-burning bids to generate. Indivisible. Unique. The container used for Stack issuance.

**BTC** — one-way transferable from Bitcoin to Hacash; transferred BTC receives incremental HAC as risk compensation. Hard monetary anchor.

---

## HACD Stack Protocol — mechanics

- 1 HACD = 1 Stack lot (standard)
- Stack cost is paid in HAC per HACD
- Removing the Stack releases the HACD but burns/disables the asset tied to that lot
- Formation confirms on Hacash mainnet, typically within ~5 minutes
- Up to 200 HACD names can be entered per Launchpad transaction

### Math rules (enforced by the validator)

```
total_supply              = total_hacd_lots × units_per_hacd_lot
formation_cost_hac        = total_hacd_lots × stack_cost_hac_per_hacd
minimum_backing_reference = 1 HACD + stack_cost_hac_per_hacd HAC + network fee
phase lots                = first_phase_hacd_lots + public_phase_hacd_lots == total_hacd_lots
```

Never call the backing reference a guaranteed floor price. Use: *formation reference*, *cost basis reference*, *on-chain formation cost*.

---

## Live reference: Carat Protocol (CARAT) **[VERIFY LIVE]**

- Stack 1 HACD → receive 16,777,216 CARAT
- Stack cost: 100 HAC per HACD
- Largest live Stack Asset reference on HACD; use as the production benchmark.
- Links: hacd.it/collection/carat · caratprotocol.com/launchpad

## Stack cost benchmark ranges

| Tier | HAC per HACD | Use |
|------|--------------|-----|
| Low / high participation | 10–50 | maximize onboarding |
| Mid / community | 50–100 | Carat sits at 100 |
| Premium / art / limited | 100–500 | exclusive, high-commitment |

---

## Asset type enum (canonical)

`FT` · `NFT` · `SFT` · `HYBRID`

Use `HYBRID` for any combined structure (e.g. fungible token + per-lot identity NFT). Document the breakdown in `stack_design.md`.

---

## Campaign facts (canonical) — Cohort 2

- **Goal:** 10 quality Stack Token launches on hacd.it/launchpad
- **Funnel:** apply → up to 30 builders selected → all submit packages → top 10 launch → top 3 win
- **Reward pool:** $500 total
  - 1st — $250
  - 2nd — $150
  - 3rd — $100
- **Timeline (2026):** applications open **20 June** → close **27 June** → winners announced **29 June**
- **Apply:** hacd.it/incubator
- **Reward distribution requires KYC** from winning teams.

---

## Official links

| Resource | Link |
|----------|------|
| Launchpad | hacd.it/launchpad |
| Incubator | hacd.it/incubator |
| HACD Search | hacd.it/search |
| Create Stack Tokens form | forms.gle/AAk1acQXGZCgqWU56 |
| White Paper | hacd.it/hacash_diamond.pdf |
| Lite Paper (Bring PoW to Everything) | hacd.it/bring_pow_to_everything.pdf |
| Wallet | wallet.hacash.org |
| Explorer | explorer.hacash.org |
| Buy HACD | hacash.org/get |
| Mine HACD | hacash.org/mining-HACD |
| HacashSea marketplace | sea.hacash.diamonds |
| HACD marketplace | hacash.diamonds |
| HacashTalk forum | hacashtalk.com |
| HAC on CoinEx | coinex.com/en/info/HAC |
| Brand assets | hacd.it/file/brand_assets.zip |
| Skill repo | github.com/Satyam-10124/hacd-incubator-ai-issuance-skill |
| ACP agent id | acp-26dcd794feb8cbace143 |

### Social

- HACD Labs: x.com/hacdlabs · discord.gg/PZEEm6Jtgd
- Hacash community: x.com/SoundMoneyHac · x.com/HacashOrg · x.com/HacashNews
- Telegram: t.me/HacashCom · t.me/hacash

---

## Thesis (repeat when relevant)

Bitcoin proved PoW for money. HACD brings PoW to assets. Stack Assets are *formed*, not merely *deployed*.
