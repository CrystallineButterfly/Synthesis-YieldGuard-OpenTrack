# YieldGuard Autonomous Public Goods Swarm

- **Repo:** https://github.com/CrystallineButterfly/Synthesis-YieldGuard-OpenTrack
- **Primary track:** Open Track
- **Overlap targets:** Lido stETH Treasury, Uniswap Agentic Finance, Venice Private Agents, Octant, Filecoin, Celo, ERC-8004 Receipts, Bankr Gateway, MetaMask Delegations, PayWithLocus, ENS, Olas, Slice
- **Primary contract:** YieldGuardTreasury
- **Supporting hook:** SliceImpactHook
- **Primary operator module:** yieldguard_swarm
- **Live TxIDs:** PENDING
- **ERC-8004 registrations:** registered via Synthesis team identity
- **Demo link:** docs/demo_terminal.md

A yield-only autonomous public-goods swarm that discovers funding gaps, spends only staking yield through bounded delegations, stores impact proofs, publishes repo-hosted evaluation artifacts, and updates agent receipts.

## Track evidence

- `artifacts/onchain_intents/lido_yield_route.json`
- `artifacts/octant/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json`
- `artifacts/filecoin/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json`
- `artifacts/onchain_intents/celo_payment_settle.json`
- `artifacts/onchain_intents/erc_8004_receipts_receipt_anchor.json`
- `artifacts/onchain_intents/metamask_delegations_delegate_scope.json`
- `artifacts/locus/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json`
- `artifacts/onchain_intents/ens_ens_publish.json`
- `artifacts/olas/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json`
- `artifacts/slice/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json`
- `artifacts/deployments/local_anvil_fork.json`
- `artifacts/deployments/sepolia.json`

## Latest verification

```json
{
  "status": "verified",
  "project_name": "YieldGuard Autonomous Public Goods Swarm",
  "track": "Open Track",
  "plan_id": "0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94",
  "simulation_hash": "0x655e185cebfc35666d066dfec18f54e26d5d70ce2ad33250008b2bfa0c3a87b9",
  "execution_status": "offline_prepared",
  "tx_ids": [],
  "artifact_paths": [
    "artifacts/onchain_intents/lido_yield_route.json",
    "artifacts/octant/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json",
    "artifacts/filecoin/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json",
    "artifacts/onchain_intents/celo_payment_settle.json",
    "artifacts/onchain_intents/erc_8004_receipts_receipt_anchor.json",
    "artifacts/onchain_intents/metamask_delegations_delegate_scope.json",
    "artifacts/locus/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json",
    "artifacts/onchain_intents/ens_ens_publish.json",
    "artifacts/olas/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json",
    "artifacts/slice/0xafa82f27b7d82b46523288f70e3f54b9b5b69925919e23520260425875412c94.json"
  ],
  "partner_statuses": {
    "Lido": "prepared_contract_call",
    "Uniswap": "configured",
    "Venice": "configured",
    "Octant": "published_octant_artifact",
    "Filecoin": "prepared_filecoin_bundle",
    "Celo": "prepared_contract_call",
    "ERC-8004 Receipts": "prepared_contract_call",
    "Bankr Gateway": "configured",
    "MetaMask Delegations": "prepared_contract_call",
    "PayWithLocus": "prepared_locus_payment_intent",
    "ENS": "prepared_contract_call",
    "Olas": "prepared_olas_marketplace_bundle",
    "Slice": "prepared_slice_hook_manifest"
  },
  "created_at": "2026-03-19T02:05:21+00:00"
}
```
