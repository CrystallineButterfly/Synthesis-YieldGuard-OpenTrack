"""Project-specific context for YieldGuard Autonomous Public Goods Swarm."""

        from __future__ import annotations

        PROJECT_CONTEXT = {
    "project_name": "YieldGuard Autonomous Public Goods Swarm",
    "track": "Open Track",
    "pitch": "A yield-only autonomous public-goods swarm that discovers funding gaps, spends only staking yield through bounded delegations, stores impact proofs, and updates agent receipts.",
    "overlap_targets": [
        "Lido stETH Treasury",
        "Uniswap Agentic Finance",
        "Venice Private Agents",
        "Octant",
        "Filecoin",
        "Celo",
        "ERC-8004 Receipts",
        "Bankr Gateway",
        "MetaMask Delegations",
        "PayWithLocus",
        "ENS",
        "Olas",
        "Slice"
    ],
    "goals": [
        "discover a bounded opportunity",
        "plan a dry-run-first action",
        "verify receipts and proofs"
    ]
}


        def seed_targets() -> list[str]:
            """Return the first batch of overlap targets for planning."""
            return list(PROJECT_CONTEXT['overlap_targets'])
