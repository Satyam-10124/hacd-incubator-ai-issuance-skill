# On-Chain Launch Walkthrough — From Package to Live Stack Asset

The skill produces your 8-document package. This guide covers what happens **after** that:
actually getting HAC and HACD, and performing the Stack on Hacash. The package tells you *what*
to launch; this tells you *how* to do it on-chain.

> Safety first: **No one — not HACD Labs, not this skill, not any "support" account — will ever
> ask for your seed phrase, private key, or wallet password.** Anyone who does is trying to rob
> you. The skill never asks for these and never signs transactions for you.

> Time-sensitive numbers (HAC price, network fee, what's in stock on the marketplace) change.
> Verify them live before you transact — see `prompts/web_research.md` (Research Mode).

---

## Overview — the whole path

```
1. Set up a Hacash wallet            → wallet.hacash.org
2. Get HAC   (for stack cost + fees) → CoinEx / Vindax / Dex-trade, or mine
3. Get HACD  (your containers)       → buy (hacash.org/get) / marketplace / mine
4. Submit your project to HACD Labs  → hacd.it/incubator  (they configure the Launchpad)
5. Stack on the Launchpad            → hacd.it/launchpad
6. Verify formation                  → explorer.hacash.org
```

You only personally Stack if you are also a participant in your own launch. As the issuer, your
main on-chain prerequisites are a wallet, some HAC for fees, and the HACD you intend to commit.

---

## Step 1 — Set up a Hacash wallet

1. Go to **wallet.hacash.org**.
2. Create a new wallet. **Write your seed phrase on paper and store it offline.** If you lose
   it, no one can recover your funds. If someone else gets it, they own your funds.
3. Confirm you can see your HAC address and (once you hold any) your HACD list.

**Checkpoint:** you have an address and your seed phrase is backed up offline.

---

## Step 2 — Get HAC

HAC pays the **stack cost** (set by the issuer, per HACD) and the **network fee** (per
transaction). You need enough for both.

Where to get it (**[VERIFY LIVE]** — confirm the venue still lists HAC and check the rate):
- **CoinEx** — coinex.com/en/info/HAC
- **Vindax**
- **Dex-trade**
- **Mining** the Hacash network directly

How much: use the `hac_cost_calculator.md` prompt on your `launch_spec.json` to get an exact
table. Rule of thumb per lot: `stack_cost_hac_per_hacd` + network fee. Add a buffer for fee
fluctuation.

After buying, **withdraw the HAC to your own wallet address** from Step 1. Do not try to Stack
from an exchange account.

**Checkpoint:** HAC is sitting in your own Hacash wallet, amount ≥ your formation cost + a fee buffer.

---

## Step 3 — Get HACD

Each Stack lot needs 1 HACD (standard). Three ways to acquire them:

| Method | Where | Notes |
|--------|-------|-------|
| Buy | hacash.org/get | Fastest. Pay in HAC/crypto for existing HACD. |
| Marketplace | sea.hacash.diamonds · hacash.diamonds | Pick specific 6-letter names — useful if the name *is* your brand/identity. |
| Mine | hacash.org/mining-HACD | Requires PoW mining + HAC bidding. Slowest, most "native". |

HACD names are unique 6-letter combinations from `W T Y U I A H X V M E K B S Z N`. If your
project uses the HACD name as an identity (e.g. a hybrid Builder-ID design), choose names on the
marketplace deliberately.

**Checkpoint:** the HACD units you plan to Stack are in your wallet. Count them — it must cover
the lots you intend to form.

---

## Step 4 — Submit to HACD Labs (Launchpad configuration)

You do not deploy the Launchpad page yourself. HACD Labs configures it from your validated package.

1. Run the validator on your spec, ideally in strict mode for a final check:
   ```bash
   python3 scripts/validate_launch_spec.py your_project/launch_spec.json --strict
   ```
2. Run `roast_mode.md` and fix everything it flags.
3. Submit your complete package via **hacd.it/incubator**.
4. HACD Labs reviews, may request changes, and on approval sets up your Stack Asset on the
   Launchpad and assigns your `launchpad_url`.

**Checkpoint:** validator passes with no ERRORs; package submitted; Launchpad listing approved.

---

## Step 5 — Stack on the Launchpad

Once your asset is live on **hacd.it/launchpad**, you (and your community) form the asset:

1. Open your project on the Launchpad and connect your wallet.
2. Prepare HAC for `(number of HACD) × stack_cost + network fee`.
3. Enter your HACD name(s) — up to **200 per transaction**.
4. Confirm the Stack transaction in your wallet.
5. Wait for mainnet confirmation — typically **~5 minutes**.

Your HACD is the formation container; it is not consumed. If a Stack is later removed, the HACD
is released but the asset tied to that lot is burned/disabled per your `removal_effect`, and the
stack cost HAC is **not** refunded.

**Checkpoint:** transaction confirmed; your asset balance appears on the Launchpad.

---

## Step 6 — Verify formation

1. Open **explorer.hacash.org** and find your transaction / address.
2. Confirm the formed units and the HACD lots involved match your spec.
3. Cross-check against your `stack_design.md` numbers.

**Checkpoint:** on-chain reality matches your package. You are live.

---

## Common questions

**Do I need HAC and HACD both?** Yes. HACD is the container (Step 3); HAC pays the stack cost
and network fee (Step 2).

**What if the network fee changed?** It varies — check explorer.hacash.org before transacting,
or run Research Mode for a live snapshot. Always keep a fee buffer.

**Can I undo a Stack?** You can remove it to release the HACD, but the asset for that lot is
burned/disabled and the stack cost is not refunded. Treat formation as permanent.

**Is any of this an investment?** No. Forming a Stack Asset is not buying a security and
guarantees no price, liquidity, listing, or return.

---

*Not financial advice. Not legal advice. Verify all live figures before transacting. Final
Launchpad parameters are set by HACD Labs.*
