#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

set -a
source .env
set +a

export RPC_URL="${RPC_URL:-$SEPOLIA_RPC_URL}"

echo "== YieldGuard terminal demo =="
echo "Repo: $ROOT_DIR"
echo "Operator: ${OPERATOR_WALLET_ADDRESS}"
echo "ENS: ${ENS_NAME}"
echo "Treasury contract: ${DEPLOYED_CONTRACT_ADDRESS:-PENDING}"
echo "Slice hook: ${SLICE_HOOK_DEPLOYED_ADDRESS:-PENDING}"
echo

echo "== Live agent run =="
python3 scripts/run_agent.py
echo

echo "== Submission render =="
python3 scripts/render_submission.py
echo

echo "== Latest synthesis snippet =="
cat submissions/synthesis.md
