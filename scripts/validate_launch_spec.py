#!/usr/bin/env python3
"""Validate a HACD Stack launch_spec.json file.

This validator checks the basic structure and the most important issuance math.
It is intentionally lightweight so non-technical reviewers can run it easily.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = ["schema_version", "project", "asset", "stack", "launch", "copy", "review"]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def warn(message: str) -> None:
    print(f"WARNING: {message}")


def require(data: dict[str, Any], key: str, context: str) -> Any:
    if key not in data:
        fail(f"Missing `{context}.{key}`")
    return data[key]


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python scripts/validate_launch_spec.py path/to/launch_spec.json")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"File not found: {path}")

    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON: {exc}")

    for key in REQUIRED_TOP_LEVEL:
        require(spec, key, "root")

    project = spec["project"]
    asset = spec["asset"]
    stack = spec["stack"]
    launch = spec["launch"]
    review = spec["review"]

    for key in ["name", "ticker", "category", "description"]:
        value = require(project, key, "project")
        if not value:
            warn(f"project.{key} is empty")

    total_supply = require(asset, "total_supply", "asset")
    total_hacd_lots = require(stack, "total_hacd_lots", "stack")
    units_per_hacd_lot = require(stack, "units_per_hacd_lot", "stack")
    hacd_per_lot = require(stack, "hacd_per_lot", "stack")
    stack_cost = require(stack, "stack_cost_hac_per_hacd", "stack")

    if not isinstance(total_supply, int) or total_supply <= 0:
        fail("asset.total_supply must be a positive integer")
    if not isinstance(total_hacd_lots, int) or total_hacd_lots <= 0:
        fail("stack.total_hacd_lots must be a positive integer")
    if not isinstance(units_per_hacd_lot, int) or units_per_hacd_lot <= 0:
        fail("stack.units_per_hacd_lot must be a positive integer")
    if not isinstance(hacd_per_lot, int) or hacd_per_lot <= 0:
        fail("stack.hacd_per_lot must be a positive integer")
    if not isinstance(stack_cost, (int, float)) or stack_cost < 0:
        fail("stack.stack_cost_hac_per_hacd must be a non-negative number")

    expected_supply = total_hacd_lots * units_per_hacd_lot
    if expected_supply != total_supply:
        fail(
            "Supply mismatch: "
            f"total_hacd_lots * units_per_hacd_lot = {expected_supply}, "
            f"but asset.total_supply = {total_supply}"
        )

    if launch.get("status") not in ["draft", "review", "approved", "live", "completed"]:
        warn("launch.status should be one of: draft, review, approved, live, completed")

    if review.get("issuer_confirmed") is not True:
        warn("review.issuer_confirmed is not true")
    if review.get("hacd_labs_reviewed") is not True:
        warn("review.hacd_labs_reviewed is not true")

    print("OK: launch spec passed basic validation")
    print(f"Formation cost reference: {total_hacd_lots * stack_cost} HAC + network fees")


if __name__ == "__main__":
    main()
