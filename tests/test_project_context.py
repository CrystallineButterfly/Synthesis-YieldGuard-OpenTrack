from __future__ import annotations

import importlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
MODULE = importlib.import_module("agents.yieldguard_swarm")


class ProjectContextTest(unittest.TestCase):
    def test_spec_has_actions_and_partners(self) -> None:
        spec = MODULE.build_project_spec()
        self.assertGreaterEqual(len(spec.actions), 3)
        self.assertGreaterEqual(len(spec.partners), 2)

    def test_local_overlap_tracks_do_not_require_partner_env(self) -> None:
        spec = MODULE.build_project_spec()
        partner_envs = {partner.name: partner.env_vars for partner in spec.partners}
        self.assertEqual(partner_envs["Octant"], ())
        self.assertEqual(partner_envs["Filecoin"], ())
        self.assertEqual(partner_envs["PayWithLocus"], ())
        self.assertEqual(partner_envs["Olas"], ())
        self.assertEqual(partner_envs["Slice"], ())

    def test_primary_names_match(self) -> None:
        spec = MODULE.build_project_spec()
        self.assertEqual(spec.primary_python_module, "yieldguard_swarm")
        self.assertEqual(spec.primary_contract_name, "YieldGuardTreasury")


if __name__ == "__main__":
    unittest.main()
