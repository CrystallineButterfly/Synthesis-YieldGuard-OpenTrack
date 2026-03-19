# Terminal demo

YieldGuard is an agent-native submission, so the demo is terminal-first instead of UI-first.

## Demo flow

1. Export the local gitignored `.env`.
2. Deploy `YieldGuardTreasury` on Sepolia.
3. Deploy `SliceImpactHook` on Sepolia.
4. Bootstrap treasury approvals, caps, cooldowns, profile, and one bounded action.
5. Run the Python agent loop.
6. Render `submissions/synthesis.md`.
7. Open the repo-hosted evidence under `artifacts/` and the Sepolia tx links.

## Commands

```bash
set -a && source .env && set +a
export RPC_URL="$SEPOLIA_RPC_URL"

forge script script/Deploy.s.sol:DeployScript --rpc-url "$RPC_URL" --broadcast \
  --private-key "$OPERATOR_PRIVATE_KEY"

forge script script/DeploySliceImpactHook.s.sol:DeploySliceImpactHookScript \
  --rpc-url "$RPC_URL" --broadcast --private-key "$OPERATOR_PRIVATE_KEY"

forge script script/BootstrapYieldGuard.s.sol:BootstrapYieldGuardScript \
  --rpc-url "$RPC_URL" --broadcast --private-key "$OPERATOR_PRIVATE_KEY"

./scripts/demo_terminal.sh
```

## What to show on screen

- Sepolia deployment receipts for both contracts
- Sepolia bootstrap receipts for policy config, liquid-balance report, profile registration, proof attach, and bounded action
- Live Uniswap quote response
- Live Venice reasoning response
- Bankr status result
- Repo-hosted artifacts in:
  - `artifacts/octant/`
  - `artifacts/filecoin/`
  - `artifacts/locus/`
  - `artifacts/olas/`
  - `artifacts/slice/`
  - `artifacts/verification/`
- Final `submissions/synthesis.md`
