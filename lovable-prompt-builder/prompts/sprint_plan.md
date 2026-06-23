# Prompt: Demo Sprint Plan

Map the Lovable build to the campaign window. **Read the actual dates and
milestones from `CAMPAIGN.md` at the repo root** — do not hardcode them here, so
this plan stays in sync if the campaign changes.

Produce a short, dated plan from "applications open" through "launch / submit",
using the day-by-day shape below as a skeleton and slotting in the real dates
from `CAMPAIGN.md`.

## Day-by-day skeleton

- **Lock scope.** Confirm concept, category, why-HACD, and the single formation
  moment. Apply at `hacd.it/incubator`. Freeze what is *out* of scope.
- **Scaffold.** Generate the app in Lovable from the executive prompt. Get the
  core page and data model rendering with mock data.
- **HACD integration.** Wire the Stack / formation flow (real or faithfully
  mocked and labeled) so a HACD formation record is created and displayed.
- **The formation moment.** Build and polish the one interaction a reviewer
  watches — through to the visible proof at the end.
- **Polish + proof.** Apply the visual system, capture a short demo video or
  screenshots, redact anything sensitive.
- **Pair with issuance.** Generate the 8-document issuance package from the root
  `SKILL.md`. Run `python3 scripts/validate_launch_spec.py <project>/launch_spec.json`
  until it reports `OK: launch spec passed basic validation`.
- **Launch + submit.** Launch / submit per `CAMPAIGN.md`, publish the share link,
  and package the demo with the issuance documents.

## Submission checklist

- [ ] Working demo (hosted Lovable app or demo video).
- [ ] A formation moment legible to a reviewer in under a minute.
- [ ] Honest why-HACD that survives the PoW-fit check.
- [ ] Paired 8-document issuance package, `launch_spec.json` validated.
- [ ] No invented metrics, payouts, price floor, or investment-return language.
- [ ] Applied / submitted within the `CAMPAIGN.md` window.
