"""Token-gating for ZENITH.

ZENITH is a *usage-first* Stack Token: the ZEN token is not a speculation
vehicle, it is the access key to the naming engine's premium surfaces. This
module defines the access tiers and the (stubbed, verifiable-later) balance
check.

IMPORTANT (safety): this module never asks for a private key, seed phrase, or
signature. Gating is read-only — it checks a *public* address balance via the
Hacash explorer. Until that integration is wired to a live endpoint, the
checker runs in OFFLINE mode and returns a clearly-labelled simulated balance
so the product is fully demoable without custody of anything.

Access tiers (ZEN held):
    0          -> "free"      basic single-name analysis only
    >= 1,000   -> "holder"    + search, leaderboard
    >= 10,000  -> "pro"       + bulk analysis, watchlists, exports
"""
from __future__ import annotations

import os
from dataclasses import dataclass

FREE_TIER = "free"
HOLDER_TIER = "holder"
PRO_TIER = "pro"

HOLDER_MIN = 1_000
PRO_MIN = 10_000

# Feature -> minimum tier required.
FEATURE_MIN_TIER = {
    "analyze": FREE_TIER,
    "validate": FREE_TIER,
    "search": HOLDER_TIER,
    "leaderboard": HOLDER_TIER,
    "bulk": PRO_TIER,
    "export": PRO_TIER,
}

_TIER_RANK = {FREE_TIER: 0, HOLDER_TIER: 1, PRO_TIER: 2}


@dataclass
class AccessResult:
    address: str
    zen_balance: int
    tier: str
    source: str  # "offline-sim" | "explorer"
    allowed: bool = True
    feature: str = ""
    required_tier: str = FREE_TIER


def tier_for_balance(balance: int) -> str:
    if balance >= PRO_MIN:
        return PRO_TIER
    if balance >= HOLDER_MIN:
        return HOLDER_TIER
    return FREE_TIER


def _offline_balance(address: str) -> int:
    """Deterministic pseudo-balance derived from the address string.

    Lets the whole product be demoed without a chain connection. Any address
    ending in a high hex-ish char lands in a higher tier, so reviewers can try
    all three tiers by hand. Clearly labelled as a simulation in the response.
    """
    if not address:
        return 0
    seed = sum(ord(c) for c in address)
    # Map into a spread that hits all three tiers.
    return (seed * 137) % 25_000


def lookup_balance(address: str) -> tuple[int, str]:
    """Return (zen_balance, source).

    When ZENITH_EXPLORER_API is set we would query the live explorer for the
    ZEN Stack Asset balance of `address`. That call is intentionally left as a
    single well-marked seam so this never blocks the demo or the tests.
    """
    address = (address or "").strip()
    api = os.environ.get("ZENITH_EXPLORER_API", "").strip()
    if not api:
        return _offline_balance(address), "offline-sim"

    # --- live seam (not exercised in offline/test mode) ---
    try:  # pragma: no cover - network path
        import urllib.request

        url = f"{api.rstrip('/')}/zen/balance/{address}"
        with urllib.request.urlopen(url, timeout=4) as resp:  # noqa: S310
            import json

            data = json.loads(resp.read().decode("utf-8"))
            return int(data.get("balance", 0)), "explorer"
    except Exception:
        # Fail safe: never crash a request because the explorer is down.
        return _offline_balance(address), "offline-sim"


def check_access(feature: str, address: str = "") -> AccessResult:
    balance, source = lookup_balance(address)
    tier = tier_for_balance(balance)
    required = FEATURE_MIN_TIER.get(feature, FREE_TIER)
    allowed = _TIER_RANK[tier] >= _TIER_RANK[required]
    return AccessResult(
        address=address, zen_balance=balance, tier=tier, source=source,
        allowed=allowed, feature=feature, required_tier=required,
    )
