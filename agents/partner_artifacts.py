"""Local artifact builders for repo-hosted and wallet-signed partner flows."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from agents.logging_utils import read_json, write_json
from agents.models import PartnerRequirement

FILECOIN_FAUCETS = (
    "https://faucet.calibnet.chainsafe-fil.io/",
    "https://docs.filecoin.cloud/getting-started/",
)

SLICE_DEPLOY_COMMAND = (
    'forge script script/DeploySliceImpactHook.s.sol --rpc-url "$RPC_URL" --broadcast'
)


def stable_digest(data: Any) -> str:
    """Return a stable SHA-256 digest for structured artifact content."""
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return "0x" + hashlib.sha256(encoded).hexdigest()


def repo_root_for_payload(payload: dict[str, Any]) -> Path:
    """Return the repository root derived from the persisted plan artifact path."""
    artifact_path = Path(str(payload["artifact_path"]))
    return artifact_path.parents[2]


def load_plan_context(payload: dict[str, Any]) -> dict[str, Any]:
    """Load the serialized plan associated with a partner action payload."""
    return read_json(Path(str(payload["artifact_path"])), default={})


def write_partner_artifact(
    repo_root: Path,
    category: str,
    stem: str,
    data: dict[str, Any],
) -> Path:
    """Persist a partner-specific artifact and return its path."""
    path = repo_root / "artifacts" / category / f"{stem}.json"
    write_json(path, data)
    return path


def relative_path(path: Path, repo_root: Path) -> str:
    """Return a repository-relative path string."""
    return str(path.relative_to(repo_root))


def sign_digest(private_key: str, digest: str) -> dict[str, str]:
    """Sign a digest with cast when a private key is available."""
    if not private_key:
        return {"status": "unsigned", "reason": "missing_private_key"}
    command = ["cast", "wallet", "sign", "--private-key", private_key, digest]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return {
            "status": "unsigned",
            "reason": completed.stderr.strip() or "cast_sign_failed",
        }
    return {"status": "signed", "signature": completed.stdout.strip()}


def contract_call_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Build a structured onchain intent for contract-driven partner actions."""
    repo_root = repo_root_for_payload(payload)
    action = dict(payload["action"])
    plan = load_plan_context(payload)
    intent = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "action_id": action["id"],
        "track": payload["track"],
        "rpc_url": os.getenv("RPC_URL", ""),
        "chain_id": os.getenv("CHAIN_ID", "11155111"),
        "operator_wallet": os.getenv("OPERATOR_WALLET_ADDRESS", ""),
        "treasury_wallet": os.getenv("TREASURY_WALLET_ADDRESS", ""),
        "target_slug": action["target"],
        "notes": action["notes"],
        "safety_controls": [
            "principal_floor",
            "dry_run_required",
            "approved_target",
            "approved_selector",
            "receipt_anchoring",
        ],
        "source_signals": plan.get("signals", []),
    }
    digest = stable_digest(intent)
    signature = sign_digest(os.getenv("OPERATOR_PRIVATE_KEY", ""), digest)
    intent["intent_digest"] = digest
    intent["signature"] = signature
    path = write_partner_artifact(repo_root, "onchain_intents", action["id"], intent)
    return {
        "status": "prepared_contract_call",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "intent_digest": digest,
        "signature_status": signature["status"],
    }


def octant_signal_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Publish a repo-hosted Octant scoring artifact for public-goods review."""
    repo_root = repo_root_for_payload(payload)
    plan = load_plan_context(payload)
    ranked = []
    for index, signal in enumerate(plan.get("signals", []), start=1):
        weighted_score = max(int(signal["score"]) - index * 3, 0)
        ranked.append(
            {
                "signal": signal["name"],
                "description": signal["description"],
                "weighted_score": weighted_score,
                "allocation_bps": weighted_score * 100,
            }
        )
    artifact = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "project_name": payload["project_name"],
        "scoring_method": "yieldguard_public_goods_v1",
        "signals_ranked": ranked,
        "recommended_next_action": payload["action"]["id"],
        "repo_visibility": "public_artifact",
    }
    digest = stable_digest(artifact)
    artifact["artifact_digest"] = digest
    path = write_partner_artifact(repo_root, "octant", payload["plan_id"], artifact)
    return {
        "status": "published_octant_artifact",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "artifact_digest": digest,
    }


def filecoin_bundle_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Create an upload-ready Filecoin evidence bundle without needing a token."""
    repo_root = repo_root_for_payload(payload)
    plan_path = Path(str(payload["artifact_path"]))
    plan_bytes = plan_path.read_bytes()
    content_digest = "sha256:" + hashlib.sha256(plan_bytes).hexdigest()
    bundle = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "source_plan": relative_path(plan_path, repo_root),
        "source_digest": content_digest,
        "target_network": "filecoin_calibration",
        "funding_links": list(FILECOIN_FAUCETS),
        "upload_strategy": {
            "mode": "synapse_ready_bundle",
            "archive_format": "json",
            "retention_policy": "submission_evidence",
        },
        "metadata": {
            "project_name": payload["project_name"],
            "track": payload["track"],
            "overlap_targets": payload["overlap_targets"],
        },
    }
    bundle["bundle_digest"] = stable_digest(bundle)
    path = write_partner_artifact(repo_root, "filecoin", payload["plan_id"], bundle)
    return {
        "status": "prepared_filecoin_bundle",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "bundle_digest": bundle["bundle_digest"],
    }


def locus_payment_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Create a wallet-signed spend-control intent for Locus-style payments."""
    repo_root = repo_root_for_payload(payload)
    action = dict(payload["action"])
    intent = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "payer_ens": os.getenv("ENS_NAME", ""),
        "payer_wallet": os.getenv("OPERATOR_WALLET_ADDRESS", ""),
        "merchant_targets": ["bankr", "slice"],
        "max_amount_usd": action["max_amount_usd"],
        "daily_budget_usd": 160,
        "settlement_network": "base_or_celo",
        "policy": {
            "kind": "bounded_subaccount_intent",
            "requires_dry_run": True,
            "requires_receipt": True,
        },
    }
    digest = stable_digest(intent)
    intent["intent_digest"] = digest
    intent["signature"] = sign_digest(os.getenv("OPERATOR_PRIVATE_KEY", ""), digest)
    path = write_partner_artifact(repo_root, "locus", payload["plan_id"], intent)
    return {
        "status": "prepared_locus_payment_intent",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "intent_digest": digest,
        "signature_status": intent["signature"]["status"],
    }


def olas_marketplace_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Create hire-and-monetize marketplace artifacts for Olas."""
    repo_root = repo_root_for_payload(payload)
    plan = load_plan_context(payload)
    signals = plan.get("signals", [])
    hire_requests = []
    for index in range(10):
        signal = signals[index % len(signals)]
        hire_requests.append(
            {
                "request_id": f"{payload['plan_id']}-req-{index + 1}",
                "prompt": f"Score {signal['name']} for public-goods allocation.",
                "max_fee_usd": 2,
            }
        )
    bundle = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "service_name": "yieldguard-octant-scorer",
        "monetized_service": {
            "unit_price_usd": 0.5,
            "delivery_artifact": f"submissions/{payload['plan_id']}-olas-service.md",
        },
        "hire_requests": hire_requests,
        "operator_wallet": os.getenv("OPERATOR_WALLET_ADDRESS", ""),
    }
    digest = stable_digest(bundle)
    bundle["bundle_digest"] = digest
    bundle["signature"] = sign_digest(os.getenv("OPERATOR_PRIVATE_KEY", ""), digest)
    path = write_partner_artifact(repo_root, "olas", payload["plan_id"], bundle)
    return {
        "status": "prepared_olas_marketplace_bundle",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "bundle_digest": digest,
        "request_count": len(hire_requests),
    }


def slice_hook_artifact(
    requirement: PartnerRequirement,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Create a deployment manifest for the onchain Slice hook contract."""
    repo_root = repo_root_for_payload(payload)
    artifact = {
        "partner": requirement.name,
        "plan_id": payload["plan_id"],
        "contract": "SliceImpactHook",
        "source": "src/SliceImpactHook.sol",
        "deploy_script": "script/DeploySliceImpactHook.s.sol",
        "deploy_command": SLICE_DEPLOY_COMMAND,
        "rpc_url": os.getenv("RPC_URL", ""),
        "chain_id": os.getenv("CHAIN_ID", "11155111"),
        "admin_wallet": os.getenv("ADMIN_WALLET_ADDRESS", ""),
        "merchant_wallet": os.getenv("OPERATOR_WALLET_ADDRESS", ""),
    }
    artifact["manifest_digest"] = stable_digest(artifact)
    path = write_partner_artifact(repo_root, "slice", payload["plan_id"], artifact)
    return {
        "status": "prepared_slice_hook_manifest",
        "partner": requirement.name,
        "artifact_path": relative_path(path, repo_root),
        "manifest_digest": artifact["manifest_digest"],
    }
