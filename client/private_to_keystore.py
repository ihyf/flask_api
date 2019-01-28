from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0xec007767eb7302486b1ebe42a489a5e4fc90d31e65bc1974722de86f36d3bd9d"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)


