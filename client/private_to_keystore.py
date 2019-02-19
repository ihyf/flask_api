from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0x8214d846e0ae2212f5724fb87f25a7c228c2e94b1c007f3a26d33213e37d9a03"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)


