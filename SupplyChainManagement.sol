// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SupplyChainManagement {

    struct Product {
        uint256 id;
        string name;
        uint256 timestamp;
        string location;
        address owner;
        bool isRegistered;
    }

    mapping(uint256 => Product) public products;
    mapping(uint256 => string[]) public productHistory;

    event ProductRegistered(uint256 indexed id, string name, string location, uint256 timestamp);
    event ProductOwnershipTransferred(uint256 indexed id, address indexed previousOwner, address indexed newOwner, uint256 timestamp);
    event ProductLocationUpdated(uint256 indexed id, string previousLocation, string newLocation, uint256 timestamp);

    function registerProduct(uint256 _id, string memory _name, string memory _location) public {
        require(!products[_id].isRegistered, "Product is already registered.");
        
        Product memory newProduct = Product({
            id: _id,
            name: _name,
            timestamp: block.timestamp,
            location: _location,
            owner: msg.sender,
            isRegistered: true
        });
        
        products[_id] = newProduct;
        productHistory[_id].push(_location);
        
        emit ProductRegistered(_id, _name, _location, block.timestamp);
    }

    function transferProductOwnership(uint256 _id, address _newOwner) public {
        require(products[_id].isRegistered, "Product is not registered.");
        require(products[_id].owner == msg.sender, "Only the current owner can transfer ownership.");
        
        address previousOwner = products[_id].owner;
        products[_id].owner = _newOwner;
        
        emit ProductOwnershipTransferred(_id, previousOwner, _newOwner, block.timestamp);
    }

    function updateProductLocation(uint256 _id, string memory _newLocation) public {
        require(products[_id].isRegistered, "Product is not registered.");
        require(products[_id].owner == msg.sender, "Only the current owner can update the location.");

        string memory previousLocation = products[_id].location;
        products[_id].location = _newLocation;
        productHistory[_id].push(_newLocation);

        emit ProductLocationUpdated(_id, previousLocation, _newLocation, block.timestamp);
    }

    function getProduct(uint256 _id) public view returns (Product memory) {
        require(products[_id].isRegistered, "Product is not registered.");
        return products[_id];
    }

    function getProductHistory(uint256 _id) public view returns (string[] memory) {
        require(products[_id].isRegistered, "Product is not registered.");
        return productHistory[_id];
    }
}
