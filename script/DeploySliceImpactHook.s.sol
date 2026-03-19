// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script} from "forge-std/Script.sol";
import {SliceImpactHook} from "src/SliceImpactHook.sol";

contract DeploySliceImpactHookScript is Script {
    function run() external returns (SliceImpactHook deployed) {
        address admin = vm.envAddress("ADMIN_WALLET_ADDRESS");
        address merchant = vm.envAddress("OPERATOR_WALLET_ADDRESS");
        address treasury = vm.envAddress("TREASURY_WALLET_ADDRESS");
        vm.startBroadcast();
        deployed = new SliceImpactHook(admin, merchant, treasury, 0.005 ether, 1_000, 5);
        vm.stopBroadcast();
    }
}
