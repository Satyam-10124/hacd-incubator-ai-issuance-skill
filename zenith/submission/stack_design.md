# Stack Design: ZENITH

## Asset type

FT (Fungible Token) — ticker ZEN

## Supply

- Total supply: 16,777,216 ZEN
- HACD lots: 256
- Units per HACD: 65,536 ZEN
- All lots are equal: Yes

Supply formula check:

```
total_supply = total_hacd_lots × units_per_hacd_lot
16,777,216   = 256 × 65,536 ✓
```

The numbers are deliberately thematic: `256 = 16²`, `65,536 = 16⁴`, and `16² × 16⁴ = 16⁶ = 16,777,216` — the exact size of the HACD name space. One ZEN exists for every possible HACD name.

## Stack cost

- Cost per HACD: 50 HAC
- Estimated total formation cost reference: 12,800 HAC (256 × 50 HAC)
- Network fee: standard Hacash transaction fee per lot (paid by participant)
- Formation cost reference is an on-chain cost input, not a guaranteed price floor.

## Genesis sequencing

ZENITH uses a reserved-first genesis, modelled on the production pattern of the largest live Stack Asset on HACD:

- 32 reserved lots (first phase) complete first from the designated reserved address, for an auditable, zero-to-genesis opening.
- 224 public lots open afterward for the community to form.

```
first_phase_hacd_lots + public_phase_hacd_lots = total_hacd_lots
32 + 224 = 256 ✓
```

## Formation rules

1. Each participant must hold at least 1 HACD and enough HAC to cover 50 HAC stack cost per lot plus network fee.
2. Each participant may Stack between 1 and 10 HACD lots per the launch rules.
3. Each Stack transaction on 1 HACD lot produces exactly 65,536 ZEN.
4. All 256 lots follow identical economic rules. The only distinction is sequencing: 32 reserved lots complete before the 224 public lots open.
5. Once all 256 lots are Stacked, no more ZEN can be formed. Supply is permanently fixed at 16,777,216 ZEN.

## Participant flow

1. Prepare 1–10 HACD units.
2. Prepare enough HAC: (number of HACD) × 50 HAC + estimated network fee.
3. Go to HACD Launchpad and find ZENITH (ZEN).
4. Enter HACD name(s) and confirm Stack transaction.
5. Verify formed ZEN balance on Launchpad or Hacash explorer.
6. Connect the address to the ZENITH engine to unlock your access tier.

## Utility binding

ZEN balance maps to live access tiers in the ZENITH engine:

- holder (≥ 1,000 ZEN): premium name search + namescore leaderboard
- pro (≥ 10,000 ZEN): bulk scoring (up to 200 names) + exports

Access is read-only and checks a public address balance. ZENITH never requests a private key, seed phrase, or signature.

## Removal / burn logic

If a participant removes the Stack from a HACD lot, the 65,536 ZEN tied to that lot are burned. The HACD is released but the ZEN units are permanently destroyed, and the access tier funded by those units is reduced accordingly. Stack cost HAC is not refunded. This keeps HACD containers and ZEN supply linked for as long as the Stack is active.
