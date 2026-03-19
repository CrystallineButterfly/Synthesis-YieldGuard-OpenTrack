from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def latest_verification_path(verification_dir: Path) -> Path | None:
    """Return the most recently modified verification artifact, if any."""
    latest_files = list(verification_dir.glob("*.json"))
    if not latest_files:
        return None
    return max(latest_files, key=lambda path: path.stat().st_mtime)


def main() -> None:
    """Render the latest submission snippet from existing artifacts."""
    from agents.logging_utils import read_json
    from agents.runtime import AgentRuntime
    from agents.yieldguard_swarm import build_project_spec

    runtime = AgentRuntime(REPO_ROOT, build_project_spec())
    verification_dir = REPO_ROOT / "artifacts" / "verification"
    latest_file = latest_verification_path(verification_dir)
    payload = runtime.run() if latest_file is None else read_json(latest_file, default={})
    runtime.render_submission(payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
