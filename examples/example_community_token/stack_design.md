# Stack Design: StackFire

## Asset type

FT (Fungible Token)

## Supply

- Total supply: 1,000,000 SFR
- HACD lots: 100
- Units per HACD: 10,000 SFR
- All lots are equal: Yes

Supply formula check:

```
total_supply = total_hacd_lots × units_per_hacd_lot
1,000,000 = 100 × 10,000 ✓
```

## Stack cost

- Cost per HACD: 50 HAC
- Estimated total formation cost reference: 5,000 HAC (100 × 50 HAC)
- Network fee: standard Hacash transaction fee per lot (paid by participant)
- Formation cost reference is an on-chain cost input, not a guaranteed price floor.

## Formation rules

1. Each participant must hold at least 1 HACD and enough HAC to cover 50 HAC stack cost plus network fee.
2. Each participant may Stack between 1 and 10 HACD lots per the launch rules.
3. Each Stack transaction on 1 HACD lot produces exactly 10,000 SFR.
4. All 100 lots follow identical rules. No tiers, no reserved lots, no designated address requirement.
5. Once all 100 lots are Stacked, no more SFR can be formed. Supply is permanently fixed.

## Participant flow

1. Prepare 1–10 HACD units.
2. Prepare enough HAC: (number of HACD) × 50 HAC + estimated network fee.
3. Go to HACD Launchpad and find StackFire (SFR).
4. Enter HACD name(s) and confirm Stack transaction.
5. Verify formed SFR balance on Launchpad or Hacash explorer.

## Removal / burn logic

If a participant removes the Stack from a HACD lot, the 10,000 SFR tied to that lot are burned. The HACD is released but the SFR units are permanently destroyed. Stack cost HAC is not refunded. This mechanism ensures HACD containers and SFR supply stay linked as long as the Stack is active.
