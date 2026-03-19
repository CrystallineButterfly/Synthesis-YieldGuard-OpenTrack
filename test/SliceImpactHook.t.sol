// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {SliceImpactHook} from "src/SliceImpactHook.sol";

contract SliceImpactHookTest is Test {
    SliceImpactHook private hook;
    address private admin = address(0xA11CE);
    address private merchant = address(0xB0B);
    address payable private treasury = payable(address(0xCAFE));
    address private buyer = address(0xD00D);

    function setUp() public {
        hook = new SliceImpactHook(admin, merchant, treasury, 0.005 ether, 1_000, 5);
    }

    function testProductPriceAppliesSupporterDiscount() public view {
        (uint256 standardPrice,) = hook.productPrice(1, 1, address(0), 2, buyer, bytes(""));
        (uint256 supporterPrice,) = hook.productPrice(
            1,
            1,
            address(0),
            2,
            buyer,
            abi.encode("supporter")
        );
        assertEq(standardPrice, 0.01 ether);
        assertEq(supporterPrice, 0.009 ether);
    }

    function testPurchaseRecordsAndForwardsValue() public {
        uint256 treasuryBalanceBefore = treasury.balance;
        vm.deal(merchant, 1 ether);
        vm.prank(merchant);
        hook.onProductPurchase{value: 0.01 ether}(
            1,
            2,
            buyer,
            2,
            bytes(""),
            abi.encode("member")
        );
        assertEq(treasury.balance, treasuryBalanceBefore + 0.01 ether);
    }

    function testPurchaseRejectedWhenPaused() public {
        vm.prank(admin);
        hook.pause();
        bool allowed = hook.isPurchaseAllowed(1, 1, buyer, 1, bytes(""), bytes(""));
        assertFalse(allowed);
    }

    function testPurchaseRejectsZeroBuyer() public {
        vm.deal(merchant, 1 ether);
        vm.prank(merchant);
        vm.expectRevert(abi.encodeWithSignature("InvalidBuyer(address)", address(0)));
        hook.onProductPurchase{value: 0.01 ether}(
            1,
            2,
            address(0),
            2,
            bytes(""),
            abi.encode("member")
        );
    }

    function testSetPricingRejectsInvalidConfig() public {
        vm.prank(admin);
        vm.expectRevert(abi.encodeWithSignature("InvalidPricingConfig()"));
        hook.setPricing(0.005 ether, 10_001, 5);
    }
}
