# Focused security review

Date: 2026-03-19

## Scope

- `src/AutonomousActionCore.sol`
- `src/AutonomousActionHub.sol`
- `src/YieldGuardTreasury.sol`
- `src/SliceImpactHook.sol`
- `agents/partners.py`
- `agents/runtime.py`

## Checks performed

- access-control review against the repo's privileged entry points
- grep pass for `tx.origin`, `selfdestruct`, EOA-detection anti-patterns, and role gates
- Foundry tests
- Python unit tests
- Python bytecode compilation

## Findings fixed before Sepolia deployment

### Fixed: zero-address guard gaps

- `src/AutonomousActionCore.sol:46-58`
- `src/SliceImpactHook.sol:43-58`
- `src/SliceImpactHook.sol:78-80`

The core role constructor, target approval path, and Slice treasury/admin wiring now reject `address(0)`.

### Fixed: invalid Slice pricing configuration

- `src/SliceImpactHook.sol:67-76`
- `src/SliceImpactHook.sol:153-157`

The hook now rejects `supporterDiscountBps > 10_000` and `maxQuantity == 0`.

### Fixed: inconsistent buyer validation

- `src/SliceImpactHook.sol:115-143`

`isPurchaseAllowed()` already rejected `address(0)` buyers, but `onProductPurchase()` did not. The state-changing path now enforces the same rule.

### Fixed: partner API request robustness

- `agents/partners.py:103-127`
- `agents/partners.py:178-196`

The Uniswap request now uses string chain IDs, explicit slippage, the router-version header, and the documented `urgency` field. Bankr auth failures for keys without gateway access now downgrade to a structured status instead of a generic error.

## Current posture

### Good

- No `tx.origin` authorization
- No EOA-detection anti-patterns
- Treasury execution is gated by:
  - approved target allowlist
  - approved selector allowlist
  - per-action cap
  - daily cap
  - cooldown window
  - validity window
  - principal floor check
  - pause switch
- Receipt anchoring is reporter-gated
- Slice purchase execution is merchant-gated and pauseable
- Duplicate purchase protection exists in the hook

### Residual operational risks

1. `DEFAULT_ADMIN_ROLE` is still highly privileged.
2. The current live setup reuses one wallet for admin, operator, reporter, and treasury.

## Recommended production posture

- split admin, operator, and reporter wallets
- move admin to a multisig
- keep the bootstrap script only for demo/single-operator environments
- keep the Sepolia operator hot wallet low-balance and rotate it after the demo
