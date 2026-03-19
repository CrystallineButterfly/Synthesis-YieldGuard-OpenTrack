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

## Loom recording script

Use this exact sequence:

### Shot 1 — show the published project URL

```bash
printf '%s\n' 'https://synthesis.devfolio.co/projects/4c86d2bae1344238a4e0b0768383cfb5'
```

Say: "This is the published Synthesis submission."

### Shot 2 — show the Sepolia deployment manifest

```bash
cat artifacts/deployments/sepolia.json
```

Say: "These are the Sepolia contract deployments and bootstrap transactions for YieldGuardTreasury and SliceImpactHook."

### Shot 3 — show the demo checklist

```bash
python3 scripts/plan_live_demo.py
```

Say: "This is the agent-native demo checklist and partner surface."

### Shot 4 — run the full live agent loop

```bash
python3 scripts/run_agent.py
```

Pause on the JSON output and point out:

- `execution_status`
- `partner_statuses.Uniswap`
- `partner_statuses.Venice`
- `partner_statuses.Bankr Gateway`
- `tx_ids`

Say: "This run executes the live reasoning and finance integrations and anchors receipts on Sepolia."

### Shot 5 — render and show the final submission snippet

```bash
python3 scripts/render_submission.py
sed -n '1,220p' submissions/synthesis.md
```

Say: "This is the final submission artifact tying together the repo, tracks, receipts, and evidence."

### Shot 6 — show the evidence folders

```bash
find artifacts -maxdepth 2 -type f | sort
```

Say: "These are the repo-hosted Octant, Filecoin, Locus, Olas, Slice, and verification artifacts produced by the agent flow."
