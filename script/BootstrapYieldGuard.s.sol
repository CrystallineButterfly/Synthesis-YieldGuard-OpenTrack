// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script} from "forge-std/Script.sol";
import {YieldGuardTreasury} from "src/YieldGuardTreasury.sol";

contract BootstrapYieldGuardScript is Script {
    function run() external {
        YieldGuardTreasury treasury = YieldGuardTreasury(
            vm.envAddress("DEPLOYED_CONTRACT_ADDRESS")
        );
        address operator = vm.envAddress("OPERATOR_WALLET_ADDRESS");
        address target = vm.envAddress("TREASURY_WALLET_ADDRESS");
        bytes4 selector = bytes4(keccak256("routeYield(bytes32,uint256)"));
        bytes32 actionId = keccak256(bytes("lido_yield_route"));
        bytes32 subjectId = keccak256(bytes(vm.envString("ENS_NAME")));
        uint256 adminKey = vm.envOr(
            "ADMIN_PRIVATE_KEY",
            vm.envUint("OPERATOR_PRIVATE_KEY")
        );
        uint256 reporterKey = vm.envUint("REPORTER_PRIVATE_KEY");
        uint256 operatorKey = vm.envUint("OPERATOR_PRIVATE_KEY");
        uint64 validAfter = uint64(block.timestamp);
        uint64 validBefore = uint64(block.timestamp + 30 days);

        vm.startBroadcast(adminKey);
        treasury.setTargetApproval(target, true);
        treasury.setSelectorApproval(selector, true);
        treasury.configureActionPolicy(actionId, 0.25 ether, 0.5 ether, 900, validAfter, validBefore);
        vm.stopBroadcast();

        vm.startBroadcast(reporterKey);
        treasury.reportLiquidBalance(1.2 ether);
        treasury.registerProfile(
            subjectId,
            operator,
            keccak256(bytes("agent.json")),
            keccak256(bytes("submissions/synthesis.md"))
        );
        treasury.attachProof(subjectId, keccak256(bytes("bootstrap-proof")));
        vm.stopBroadcast();

        vm.startBroadcast(operatorKey);
        treasury.recordDryRun(actionId, keccak256(bytes("bootstrap-dry-run")));
        treasury.executeBoundedAction(
            actionId,
            target,
            selector,
            0.1 ether,
            keccak256(bytes("bootstrap-call"))
        );
        vm.stopBroadcast();
    }
}
