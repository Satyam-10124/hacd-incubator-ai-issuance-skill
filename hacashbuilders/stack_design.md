# Stack Design: HacashBuilders

## Asset type

Hybrid FT + NFT

- **FT:** BUILD (fungible balance)
- **NFT:** HACD name as Builder ID (unique per lot)

## Supply

- Total supply: 10,000,000 BUILD
- HACD lots: 500
- Units per HACD: 20,000 BUILD
- Builder IDs: up to 500 (one unique HACD name per lot)
- All lots are equal: Yes

Supply formula check:

```
total_supply = total_hacd_lots × units_per_hacd_lot
10,000,000 = 500 × 20,000 ✓
```

## Stack cost

- Cost per HACD: 50 HAC
- Estimated total formation cost reference: 25,000 HAC (500 × 50 HAC)
- Network fee: standard Hacash transaction fee per lot (paid by participant)
- Formation cost reference is an on-chain cost input, not a guaranteed price floor.

Minimum backing reference per lot: 1 HACD + 50 HAC + network fee.

## Formation rules

1. Each participant must hold at least 1 HACD and enough HAC to cover 50 HAC stack cost plus network fee per lot.
2. Each participant may Stack between 1 and 10 HACD lots per the launch rules.
3. Each Stack transaction on 1 HACD lot produces exactly 20,000 BUILD and registers that HACD name as one Builder ID.
4. All 500 lots follow identical rules. No tiers, no reserved lots, no designated address requirement.
5. Once all 500 lots are Stacked, no more BUILD can be formed and no more Builder IDs can be created. Supply is permanently fixed.

## Participant flow

1. Prepare 1–10 HACD units. (Their names will become your Builder IDs.)
2. Prepare enough HAC: (number of HACD) × 50 HAC + estimated network fee.
3. Go to the HACD Launchpad and find HacashBuilders (BUILD).
4. Enter your HACD name(s) and confirm the Stack transaction. (Up to 200 HACD names can be entered per Launchpad transaction.)
5. Verify your formed BUILD balance and registered Builder ID(s) on the Launchpad or Hacash explorer.

## Removal / burn logic

If a participant removes the Stack from a HACD lot, the 20,000 BUILD tied to that lot are burned and that Builder ID is retired. The HACD is released back to the holder's free HACD. Stack cost HAC is not refunded. This mechanism keeps HACD containers, Builder IDs, and BUILD supply linked as long as the Stack is active.

## Hybrid clarification

- The **BUILD balance** is fungible — 20,000 BUILD from lot A is identical to 20,000 BUILD from lot B.
- The **Builder ID** is the unique HACD name and is not fungible — it identifies which builder formed which lot.
- Both are produced by the same single Stack action; participants do not pay or transact twice.

---

*Draft design. Issuer confirmation required on stack cost, supply, and transferability of the Builder ID. Not financial advice. Final Launchpad parameters must be verified by HACD Labs.*
