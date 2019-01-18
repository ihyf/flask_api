import json
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
from eth_account import Account
# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.21;

contract Greeter {
    string public greeting;

    function Greeter() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://192.168.1.33:8101"))
# set pre-funded account as sender
# w3.eth.defaultAccount = w3.eth.accounts[0]
w3.eth.defaultAccount = w3.toChecksumAddress("0x5b365efb9c6142678fcb1cefe39180754c6e5d91")
address = w3.toChecksumAddress("0x5b365efb9c6142678fcb1cefe39180754c6e5d91")

keystore = {"address": "5b365efb9c6142678fcb1cefe39180754c6e5d91", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "bad335f6fbfe302a3805983f46f2447a"}, "ciphertext": "1f7b91bf1ee929c581becafbab1afc32f4a0fbdd30ccde73c6a061cd2fc48e6a", "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256", "salt": "b610efc763cede53535ef0268ff2822d"}, "mac": "0542b308ea83fb76c1da5371b34b0618fececcbba93ab4e6fc80912683966137"}, "id": "ec93dfb7-dcce-437a-a4fe-f83aa0aae082", "version": 3}
pwd = "hyf"
private_key = Account.decrypt(json.dumps(keystore), pwd)
account = Account.privateKeyToAccount(private_key)
# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
nonce = w3.eth.getTransactionCount(address)
t_dict = Greeter.constructor().transact().buildTransaction({
    "chainId": 1500,
    "gas": 700000,
    "gas": 50000,
    "nonce": nonce
})
signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("deploy success")

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# Display the default greeting from the contract
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

print('Setting the greeting to Nihao...')
tx_hash = greeter.functions.setGreeting('Nihao').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
print('Updated contract greeting: {}'.format(
    greeter.functions.greet().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(greeter)
assert reader.greet() == "Nihao"