#!/usr/bin/env python3
"""Validate a HACD Stack launch_spec.json file and (optionally) its sibling documents.

Checks, in order:
  1. JSON structure and required fields
  2. Type and enum validation (asset.type, launch.status, phase_model, removal_effect)
  3. Issuance math (supply equation, phase-lot sum, formation cost)
  4. Decimals sanity
  5. Cross-document consistency  (numbers in the .md files must match the spec)
  6. Copy-safety lint            (banned promo terms + HACD/HAC confusion across all .md)

Usage:
  python3 scripts/validate_launch_spec.py path/to/launch_spec.json
  python3 scripts/validate_launch_spec.py path/to/launch_spec.json --strict
  python3 scripts/validate_launch_spec.py path/to/launch_spec.json --no-docs

--strict    treat WARNINGs as failures (use this in CI for final submissions)
--no-docs   validate only the JSON, skip the cross-doc + copy-safety passes

Exit codes: 0 = clean (or warnings only without --strict), 1 = error / strict failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = ["schema_version", "project", "asset", "stack", "launch", "copy", "review"]

ASSET_TYPES = {"FT", "NFT", "SFT", "HYBRID"}
LAUNCH_STATUSES = {"draft", "review", "approved", "live", "completed"}
PHASE_MODELS = {"public", "allowlist", "designated_first", "custom"}
REMOVAL_EFFECTS = {"burn", "disable", "no_effect", "unknown"}

# Promo / unsafe language that must never appear in public-facing copy.
# Each entry: (regex, human explanation).
BANNED_TERMS = [
    (r"\bguarantee(d|s)?\b", "implies a promise the issuer cannot make"),
    (r"\bprice floor\b", "stack cost is not a guaranteed floor"),
    (r"\bfloor price\b", "stack cost is not a guaranteed floor"),
    (r"\brisk[- ]free\b", "nothing here is risk-free"),
    (r"\bmoon(ing|shot)?\b", "price-hype language"),
    (r"\bto the moon\b", "price-hype language"),
    (r"\bROI\b", "investment-return framing"),
    (r"\byield\b", "investment-return framing"),
    (r"\bpassive income\b", "investment-return framing"),
    (r"\bprofit(s|able)?\b", "investment-return framing"),
    (r"\bget rich\b", "investment-return framing"),
    (r"\b\d+x\s+(return|gains?)\b", "price-appreciation promise"),
    (r"\bbacked value\b", "use 'formation cost reference', not 'backed value'"),
    (r"\bguaranteed (listing|return|profit|price)\b", "no guarantees permitted"),
]

# Terminology confusion: HACD described incorrectly.
TERMINOLOGY_TRAPS = [
    (r"HACD\s*=\s*HAC\s*\+\s*Diamond", "do not define HACD as 'HAC + Diamond'"),
    (r"\bStack is just minting\b", "Stack is formation, not minting"),
    (r"\bjust an NFT\b", "HACD is a PoW asset container, not 'just an NFT'"),
    (r"stack cost guarantees (the )?price", "stack cost guarantees nothing"),
]

# Phrases that should appear somewhere in the public docs (safety disclosures).
EXPECTED_DISCLOSURES = [
    (r"not financial advice", "missing 'not financial advice' disclosure"),
    (r"(risk disclosure|not an investment)", "missing risk / non-investment disclosure"),
]

errors: list[str] = []
warnings: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def require(data: dict[str, Any], key: str, context: str) -> Any:
    if not isinstance(data, dict) or key not in data:
        err(f"Missing `{context}.{key}`")
        return None
    return data[key]


def check_enum(value: Any, allowed: set[str], field: str) -> None:
    if value not in allowed:
        err(f"{field} = {value!r} is not one of {sorted(allowed)}")


def validate_spec(spec: dict[str, Any]) -> dict[str, Any]:
    for key in REQUIRED_TOP_LEVEL:
        require(spec, key, "root")

    project = spec.get("project", {})
    asset = spec.get("asset", {})
    stack = spec.get("stack", {})
    launch = spec.get("launch", {})
    review = spec.get("review", {})

    for key in ["name", "ticker", "category", "description"]:
        value = require(project, key, "project")
        if value is not None and not value:
            warn(f"project.{key} is empty")

    for key in ["website", "contact"]:
        value = project.get(key, "")
        if not value:
            warn(f"project.{key} is empty (fill before submission)")

    # --- enums ---
    check_enum(asset.get("type"), ASSET_TYPES, "asset.type")
    check_enum(launch.get("status"), LAUNCH_STATUSES, "launch.status")
    check_enum(launch.get("phase_model"), PHASE_MODELS, "launch.phase_model")
    check_enum(stack.get("removal_effect"), REMOVAL_EFFECTS, "stack.removal_effect")

    # --- numeric fields ---
    total_supply = asset.get("total_supply")
    total_hacd_lots = stack.get("total_hacd_lots")
    units_per_hacd_lot = stack.get("units_per_hacd_lot")
    hacd_per_lot = stack.get("hacd_per_lot")
    stack_cost = stack.get("stack_cost_hac_per_hacd")
    decimals = asset.get("decimals")

    def pos_int(value: Any, field: str) -> bool:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            err(f"{field} must be a positive integer (got {value!r})")
            return False
        return True

    ok_supply = pos_int(total_supply, "asset.total_supply")
    ok_lots = pos_int(total_hacd_lots, "stack.total_hacd_lots")
    ok_units = pos_int(units_per_hacd_lot, "stack.units_per_hacd_lot")
    pos_int(hacd_per_lot, "stack.hacd_per_lot")

    if not isinstance(stack_cost, (int, float)) or isinstance(stack_cost, bool) or stack_cost < 0:
        err("stack.stack_cost_hac_per_hacd must be a non-negative number")
        stack_cost = None

    if not isinstance(decimals, int) or isinstance(decimals, bool) or decimals < 0:
        warn("asset.decimals should be a non-negative integer (0 for indivisible units)")

    # --- supply equation ---
    if ok_supply and ok_lots and ok_units:
        expected = total_hacd_lots * units_per_hacd_lot
        if expected != total_supply:
            err(
                "Supply mismatch: total_hacd_lots × units_per_hacd_lot = "
                f"{expected:,}, but asset.total_supply = {total_supply:,}"
            )

    # --- phase-lot sum ---
    first_phase = stack.get("first_phase_hacd_lots")
    public_phase = stack.get("public_phase_hacd_lots")
    if isinstance(first_phase, int) and isinstance(public_phase, int) and ok_lots:
        if first_phase + public_phase != total_hacd_lots:
            err(
                "Phase-lot mismatch: first_phase_hacd_lots + public_phase_hacd_lots = "
                f"{first_phase + public_phase}, but total_hacd_lots = {total_hacd_lots}"
            )

    # --- participant caps ---
    min_p = launch.get("min_hacd_per_participant")
    max_p = launch.get("max_hacd_per_participant")
    if isinstance(min_p, int) and isinstance(max_p, int) and max_p < min_p:
        err(f"launch.max_hacd_per_participant ({max_p}) < min ({min_p})")
    if max_p in (None, 0):
        warn("launch.max_hacd_per_participant is not set — confirm there is intentionally no cap")

    # --- review flags ---
    if review.get("issuer_confirmed") is not True:
        warn("review.issuer_confirmed is not true (expected for a draft)")
    if review.get("hacd_labs_reviewed") is not True:
        warn("review.hacd_labs_reviewed is not true (expected for a draft)")

    return {
        "total_hacd_lots": total_hacd_lots,
        "units_per_hacd_lot": units_per_hacd_lot,
        "total_supply": total_supply,
        "stack_cost": stack_cost,
        "ticker": project.get("ticker"),
    }


# --------------------------------------------------------------------------- #
# Document passes
# --------------------------------------------------------------------------- #

def gather_docs(spec_path: Path) -> dict[str, str]:
    """Read sibling .md files in the same folder as the spec."""
    docs: dict[str, str] = {}
    for md in sorted(spec_path.parent.glob("*.md")):
        try:
            docs[md.name] = md.read_text(encoding="utf-8")
        except OSError:
            warn(f"could not read {md.name}")
    return docs


def numbers_in(text: str) -> set[int]:
    """All integers in the text, with thousands separators normalized."""
    found: set[int] = set()
    for raw in re.findall(r"\d[\d,]*", text):
        digits = raw.replace(",", "")
        if digits.isdigit():
            found.add(int(digits))
    return found


def check_cross_docs(facts: dict[str, Any], docs: dict[str, str]) -> None:
    """Key spec numbers should appear verbatim in the design + copy docs."""
    targets = {
        "stack_design.md": ["total_supply", "total_hacd_lots", "units_per_hacd_lot"],
        "launchpad_copy.md": ["total_supply", "total_hacd_lots"],
    }
    for fname, keys in targets.items():
        if fname not in docs:
            warn(f"{fname} not found — cannot cross-check numbers")
            continue
        present = numbers_in(docs[fname])
        for key in keys:
            value = facts.get(key)
            if isinstance(value, int) and value not in present:
                err(f"{fname} does not mention {key} = {value:,} (cross-doc mismatch with spec)")


# Negation / safe-context cues. A banned term on a line that also carries one of
# these is almost always a disclosure ("no yield is guaranteed") or a checklist
# entry ('No use of "moon"'), not a promise. This is what keeps the linter usable.
NEGATION_CUE = re.compile(
    r"\b(no|not|never|without|cannot|can'?t|don'?t|doesn'?t|isn'?t|aren'?t|won'?t|"
    r"nor|neither|avoid|prohibit(ed)?|banned|n't|do not|does not|must not|"
    r"not a|no such|non-?refundable|disclaim)\b",
    re.IGNORECASE,
)


def _is_safe_context(line: str, term: str) -> bool:
    """True if the banned term on this line is negated or quoted (a disclosure)."""
    if NEGATION_CUE.search(line):
        return True
    # Quoted term — e.g. a checklist listing the banned words themselves.
    if re.search(r'["“‘]\s*' + re.escape(term) + r'\s*["”’]', line, re.IGNORECASE):
        return True
    return False


def check_copy_safety(docs: dict[str, str]) -> None:
    """Lint public-facing markdown for banned terms and terminology traps.

    Detection is line-aware and negation-aware: a banned word that appears inside a
    negated or quoted clause (a risk disclosure) is allowed; an un-negated promise
    is flagged. Reviewer tooling (review_checklist, intake) is exempt from the
    banned-term pass because it legitimately quotes the forbidden words.
    """
    PUBLIC_COPY = {"launchpad_copy.md", "issuer_faq.md", "x_announcement.md", "project_profile.md"}

    for fname, text in docs.items():
        # Terminology traps are always wrong, anywhere.
        for pattern, why in TERMINOLOGY_TRAPS:
            if re.search(pattern, text, re.IGNORECASE):
                err(f"{fname}: terminology error — {why}")

        # Banned-term pass only on genuinely public-facing copy.
        if fname not in PUBLIC_COPY:
            continue
        for line in text.splitlines():
            for pattern, why in BANNED_TERMS:
                for m in re.finditer(pattern, line, re.IGNORECASE):
                    term = m.group(0)
                    if _is_safe_context(line, term):
                        continue
                    snippet = line.strip()[:90]
                    err(f"{fname}: unsafe term '{term}' ({why}) → …{snippet}…")

    # Disclosures must exist somewhere in the public set.
    public = " ".join(t.lower() for n, t in docs.items() if n in {"launchpad_copy.md", "issuer_faq.md"})
    if public:
        for pattern, why in EXPECTED_DISCLOSURES:
            if not re.search(pattern, public):
                warn(why)


# --------------------------------------------------------------------------- #

def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    strict = "--strict" in flags
    do_docs = "--no-docs" not in flags

    if len(args) != 1:
        print("Usage: python3 scripts/validate_launch_spec.py path/to/launch_spec.json [--strict] [--no-docs]")
        sys.exit(1)

    path = Path(args[0])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}")
        sys.exit(1)

    facts = validate_spec(spec)

    if do_docs:
        docs = gather_docs(path)
        if docs:
            check_cross_docs(facts, docs)
            check_copy_safety(docs)

    # --- report ---
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARNING: {w}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)

    if facts.get("total_hacd_lots") and facts.get("stack_cost") is not None:
        cost = facts["total_hacd_lots"] * facts["stack_cost"]
        print(f"OK: launch spec passed validation")
        print(f"Formation cost reference: {cost:,} HAC + network fees")
    else:
        print("OK: launch spec passed validation")

    if warnings and strict:
        print(f"\nFAILED (--strict): {len(warnings)} warning(s) treated as errors")
        sys.exit(1)

    if warnings:
        print(f"({len(warnings)} warning(s) — fine for a draft, resolve before final submission)")

    # Self-guiding next step: only a clean strict pass is submission-ready.
    if not warnings and strict:
        print("\nReady to submit. Package per CAMPAIGN.md, then take it on-chain "
              "via LAUNCH_WALKTHROUGH.md.")
    elif not strict:
        print("Next: fix any warnings, then re-run with --strict for the final check.")


if __name__ == "__main__":
    main()
