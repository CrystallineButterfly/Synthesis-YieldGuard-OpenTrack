// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {IProductAction, IProductPrice} from "src/interfaces/ISliceProductHooks.sol";

contract SliceImpactHook is AccessControl, Pausable, IProductPrice, IProductAction {
    bytes32 public constant MERCHANT_ROLE = keccak256("MERCHANT_ROLE");

    struct PurchaseRecord {
        address buyer;
        uint96 quantity;
        uint96 ethValue;
        uint64 purchasedAt;
    }

    address public treasury;
    uint256 public basePriceWei;
    uint16 public supporterDiscountBps;
    uint16 public maxQuantity;
    mapping(bytes32 => PurchaseRecord) public purchaseRecords;

    error QuantityOutOfRange(uint256 quantity, uint256 maxQuantityAllowed);
    error DuplicatePurchase(bytes32 purchaseId);
    error TransferFailed();
    error InvalidBuyer(address buyer);
    error InvalidPricingConfig();
    error ZeroAddressNotAllowed();

    event PurchaseRecorded(
        bytes32 indexed purchaseId,
        uint256 indexed slicerId,
        uint256 indexed productId,
        address buyer,
        uint256 quantity,
        uint256 value
    );
    event PricingUpdated(
        uint256 basePriceWei,
        uint16 supporterDiscountBps,
        uint16 maxQuantity
    );
    event TreasuryUpdated(address treasury);

    constructor(
        address admin,
        address merchant,
        address treasuryAddress,
        uint256 initialBasePriceWei,
        uint16 initialDiscountBps,
        uint16 initialMaxQuantity
    ) {
        _requireAddress(admin);
        _requireAddress(merchant);
        _requireAddress(treasuryAddress);
        _requirePricing(initialDiscountBps, initialMaxQuantity);
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(MERCHANT_ROLE, merchant);
        treasury = treasuryAddress;
        basePriceWei = initialBasePriceWei;
        supporterDiscountBps = initialDiscountBps;
        maxQuantity = initialMaxQuantity;
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    function setPricing(
        uint256 newBasePriceWei,
        uint16 newDiscountBps,
        uint16 newMaxQuantity
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _requirePricing(newDiscountBps, newMaxQuantity);
        basePriceWei = newBasePriceWei;
        supporterDiscountBps = newDiscountBps;
        maxQuantity = newMaxQuantity;
        emit PricingUpdated(newBasePriceWei, newDiscountBps, newMaxQuantity);
    }

    function setTreasury(address newTreasury) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _requireAddress(newTreasury);
        treasury = newTreasury;
        emit TreasuryUpdated(newTreasury);
    }

    function productPrice(
        uint256,
        uint256,
        address,
        uint256 quantity,
        address,
        bytes memory data
    ) external view returns (uint256 ethPrice, uint256 currencyPrice) {
        _requireValidQuantity(quantity);
        uint256 unitPrice = basePriceWei;
        if (data.length != 0) {
            uint256 discount = (unitPrice * supporterDiscountBps) / 10_000;
            unitPrice -= discount;
        }
        ethPrice = unitPrice * quantity;
        currencyPrice = 0;
    }

    function isPurchaseAllowed(
        uint256,
        uint256,
        address buyer,
        uint256 quantity,
        bytes memory,
        bytes memory
    ) external view returns (bool) {
        if (paused()) {
            return false;
        }
        return buyer != address(0) && quantity != 0 && quantity <= maxQuantity;
    }

    function onProductPurchase(
        uint256 slicerId,
        uint256 productId,
        address buyer,
        uint256 quantity,
        bytes memory,
        bytes memory buyerCustomData
    ) external payable onlyRole(MERCHANT_ROLE) whenNotPaused {
        _requireValidQuantity(quantity);
        if (buyer == address(0)) {
            revert InvalidBuyer(buyer);
        }
        bytes32 purchaseId = keccak256(
            abi.encode(slicerId, productId, buyer, quantity, msg.value, buyerCustomData)
        );
        if (purchaseRecords[purchaseId].purchasedAt != 0) {
            revert DuplicatePurchase(purchaseId);
        }
        purchaseRecords[purchaseId] = PurchaseRecord({
            buyer: buyer,
            quantity: uint96(quantity),
            ethValue: uint96(msg.value),
            purchasedAt: uint64(block.timestamp)
        });
        if (msg.value != 0) {
            (bool ok,) = payable(treasury).call{value: msg.value}("");
            if (!ok) {
                revert TransferFailed();
            }
        }
        emit PurchaseRecorded(purchaseId, slicerId, productId, buyer, quantity, msg.value);
    }

    function _requireValidQuantity(uint256 quantity) internal view {
        if (quantity == 0 || quantity > maxQuantity) {
            revert QuantityOutOfRange(quantity, maxQuantity);
        }
    }

    function _requireAddress(address candidate) internal pure {
        if (candidate == address(0)) {
            revert ZeroAddressNotAllowed();
        }
    }

    function _requirePricing(uint16 discountBps, uint16 quantity) internal pure {
        if (quantity == 0 || discountBps > 10_000) {
            revert InvalidPricingConfig();
        }
    }
}
