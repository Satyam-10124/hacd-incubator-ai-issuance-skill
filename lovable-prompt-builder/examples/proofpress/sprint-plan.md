# ProofPress — Demo Sprint Plan

The build mapped to the HACD Incubator Cohort 2 window. Read the authoritative
dates from `CAMPAIGN.md` at the repo root; the steps below are the build
skeleton.

- **Lock scope.** Confirm ProofPress / utility / "can't be backdated" as the
  why-HACD. Apply at `hacd.it/incubator`. Freeze out of scope: no wallet, no
  comments, no media uploads.
- **Scaffold.** Generate the app in Lovable from
  [`lovable-prompt.md`](lovable-prompt.md). Get Editor, Library, and Proof page
  rendering with mock data.
- **HACD integration.** Wire Publish → form HacdStackRecord (content hash +
  formation timestamp), faithfully mocked and labeled.
- **The formation moment.** Polish publish → receipt → open public proof in a
  fresh tab. Make the "formed at" time and content hash unmissable.
- **Polish + proof.** Apply the utility accent (#6FB3AB), capture a short demo
  video and screenshots, redact anything sensitive.
- **Pair with issuance.** Generate the 8-document issuance package from the root
  `SKILL.md`. Run
  `python3 scripts/validate_launch_spec.py proofpress/launch_spec.json` until it
  reports `OK: launch spec passed basic validation`.
- **Launch + submit.** Launch / submit per `CAMPAIGN.md`, publish the share link,
  and package the demo with the issuance documents.

## Submission checklist

- [ ] Working ProofPress demo (hosted Lovable app or demo video).
- [ ] The publish → verify formation moment captured as proof.
- [ ] Honest why-HACD that survives the PoW-fit check.
- [ ] Paired 8-document issuance package, `launch_spec.json` validated.
- [ ] No invented metrics, payouts, or price-floor / investment language.
- [ ] Applied / submitted within the `CAMPAIGN.md` window.
