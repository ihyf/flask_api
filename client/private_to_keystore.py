from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0xd01add976d3d5481266c3baec3a56107c10357a53c6183296204c1eb37ecaec8"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)


