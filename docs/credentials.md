# Credentials

## Required external credentials

- **Lido**: `RPC_URL` — https://docs.lido.fi/
- **Uniswap**: `UNISWAP_API_KEY`, `UNISWAP_QUOTE_URL` — https://api-docs.uniswap.org/api-reference/swapping/quote
- **Venice**: `VENICE_API_KEY`, `VENICE_CHAT_COMPLETIONS_URL`, `VENICE_MODEL` — https://docs.venice.ai/
- **Celo**: `CELO_RPC_URL` — https://docs.celo.org/
- **ERC-8004 Receipts**: `RPC_URL` — https://eips.ethereum.org/EIPS/eip-8004
- **Bankr Gateway**: `BANKR_API_KEY`, `BANKR_CHAT_COMPLETIONS_URL`, `BANKR_MODEL` — the key must have **LLM Gateway access enabled** at https://bankr.bot/api
- **MetaMask Delegations**: `RPC_URL` — https://docs.metamask.io/delegation-toolkit/
- **ENS**: `ENS_NAME` — https://docs.ens.domains/

## No longer blocked on partner API keys

These tracks now use repo-hosted, wallet-signed, or onchain flows inside this repo:

- **Octant**: repo-hosted scoring artifacts under `artifacts/octant/`
- **Filecoin**: upload-ready evidence bundles under `artifacts/filecoin/`
- **PayWithLocus**: wallet-signed payment intents under `artifacts/locus/`
- **Olas**: marketplace hire/monetize bundles under `artifacts/olas/`
- **Slice**: onchain hook deployment manifests under `artifacts/slice/` plus `SliceImpactHook`

## Optional live follow-up links

- Filecoin Calibration faucet: https://faucet.calibnet.chainsafe-fil.io/
- Filecoin getting started: https://docs.filecoin.cloud/getting-started/
- Slice hooks repo: https://github.com/slice-so/hooks
- Octant docs: https://docs.octant.app/en-EN/
- Olas hire: https://build.olas.network/hire
- Bankr key management: https://bankr.bot/api
