import os
from web3 import Web3
from web3.middleware import geth_poa_middleware

import deploy


# Set up web3 connection
provider_url = os.environ.get("CELO_PROVIDER_URL")
w3 = Web3(Web3.HTTPProvider(provider_url))
assert w3.is_connected(), "Not connected to a Celo node"

# Add PoA middleware to web3.py instance
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


abi = deploy.abi
contract_address = deploy.contract_address
private_key = deploy.private_key
user_address = deploy.deployer


contract = w3.eth.contract(address=contract_address, abi=abi)

# Register a new product
product_id = 1
product_name = "Product 1"
product_location = "New York"

nonce = w3.eth.get_transaction_count(user_address)
transaction = {
    'from': user_address,
    'to': contract_address,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
    'data': contract.encodeABI(fn_name="registerProduct", args=[product_id, product_name, product_location]),
}
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(f"Product registered: {transaction_receipt}")

# Get product details
product = contract.functions.getProduct(product_id).call()
print(f"Product details: {product}")

# Get product history
product_history = contract.functions.getProductHistory(product_id).call()
print(f"Product history: {product_history}")

# Transfer product ownership
new_owner = "NEW_OWNER_ADDRESS"
nonce = w3.eth.get_transaction_count(user_address)
transaction = {
    'from': user_address,
    'to': contract_address,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
    'data': contract.encodeABI(fn_name="transferProductOwnership", args=[product_id, new_owner]),
}
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(f"Product ownership transferred: {transaction_receipt}")

# Update product location
new_location = "Los Angeles"
nonce = w3.eth.get_transaction_count(user_address)
transaction = {
    'from': user_address,
    'to': contract_address,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
    'data': contract.encodeABI(fn_name="updateProductLocation", args=[product_id, new_location]),
}
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(f"Product location updated: {transaction_receipt}")