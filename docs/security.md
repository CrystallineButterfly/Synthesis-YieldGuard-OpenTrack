# Security

## Enforced controls

- `YieldGuardTreasury` gates spend through:
  - approved targets
  - approved selectors
  - per-action caps
  - daily caps
  - cooldown windows
  - principal floor accounting
  - reporter-anchored receipt digests
- `SliceImpactHook` gates commerce actions through:
  - role-based merchant execution
  - pausability
  - quantity limits
  - duplicate-purchase protection
  - treasury forwarding checks

## Audit notes

### Access control

Good:
- no `tx.origin` auth
- no EOA-detection anti-patterns
- state-changing treasury functions are role-gated
- hook admin and merchant permissions are explicit
- zero-address guards now cover constructor role wiring, target approval, and hook treasury/admin wiring
- Slice pricing config now rejects invalid discount and quantity settings
- state-changing Slice purchases now reject zero-address buyers

Operational caveat:
- local setup currently uses one key for admin/operator/reporter for convenience
- for final public live deployment, split these roles across separate wallets

### External integrations

- Uniswap quote path is live and now matches the current Trading API request shape
- Venice chat-completions path is live and returns data with the configured API key
- Bankr integration is implemented and now returns a structured credits blocker after gateway access was enabled
- Octant, Filecoin, Locus, Olas, and Slice no longer depend on placeholder URLs or fake envs

## Remaining non-code work

- Bankr LLM credits
- fund any required demo wallets
- attach final TxIDs and media links in submission assets
