# Review Checklist: StackFire (SFR)

## Formation logic

- [x] Supply matches HACD lots: 100 × 10,000 = 1,000,000 ✓
- [x] Stack cost is clear: 50 HAC per HACD, stated consistently across all documents
- [x] Participant flow is clear: step-by-step in stack_design.md and launchpad_copy.md
- [x] hacd_per_lot is 1 (standard, no unusual structure)
- [x] Removal / burn logic is defined and consistent
- [ ] Maximum per participant (10 HACD) enforcement confirmed at Launchpad level — **Needs issuer confirmation**
- [ ] Stack cost (50 HAC) confirmed as final — **Needs issuer confirmation**

## Copy safety

- [x] No profit promise in any document
- [x] No misleading backing claim: formation cost described as "cost basis reference" not "floor price"
- [x] No legal guarantee: risk disclosure present in launchpad_copy.md and issuer_faq.md
- [x] "Not financial advice" included in launchpad_copy.md and issuer_faq.md
- [x] Governance utility marked as planned / not guaranteed in all relevant documents
- [x] Channel access marked as planned / not guaranteed in all relevant documents
- [x] No mention of exchange listing guarantee
- [x] No use of "yield", "return", "profit", "floor", "guaranteed", or "moon"

## Launch readiness

- [ ] Launchpad URL — **Missing, to be confirmed by HACD Labs**
- [ ] Issuer identity confirmed to HACD Labs privately — **Pending**
- [x] Issuer has confirmed numbers in intake form
- [ ] issuer_confirmed flag set to true in launch_spec.json — **Pending issuer sign-off**
- [ ] hacd_labs_reviewed flag set to true in launch_spec.json — **Pending HACD Labs review**
- [ ] Legal review completed — **Required before publication**

## Validator

- [x] launch_spec.json passes validate_launch_spec.py with no ERRORs
- [x] Supply math validated: 100 × 10,000 = 1,000,000
- [x] Formation cost reference: 5,000 HAC + network fees
- [ ] Final validated spec signed off by HACD Labs — **Pending**

## Outstanding items before Launchpad publication

1. Issuer confirms 50 HAC stack cost is final.
2. Issuer confirms 10 HACD max per participant is Launchpad-enforced.
3. Issuer provides verified team / operator identity to HACD Labs.
4. HACD Labs assigns Launchpad URL and sets hacd_labs_reviewed to true.
5. Legal review completed and any required disclosures added.
6. issuer_confirmed and hacd_labs_reviewed flags updated to true in launch_spec.json.
7. Final re-run of validate_launch_spec.py on the approved spec.

---

*This checklist is part of a draft issuance package. Final parameters must be confirmed by the issuer and reviewed by HACD Labs before Launchpad publication.*
