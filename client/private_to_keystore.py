from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0x42107ea71cbb53229c3ef4687bcb5307bf57204afcade5a8899e371cf077a386"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)


