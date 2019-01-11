from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0x42e8b143852b53009f80ce0af2fee768f4a52def57c42cd76bb20addf826b5fe"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)

wallet = {'address': '77fb4a966385a0d160457416fbf4b4cccf91f62e', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '0231557c41387c1277f33f82f00c7b02'}, 'ciphertext': '01cabb2429e8071ef8d073954e84f90e96f1522f1b1417e15b020be4b932c6c0', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'be64122d157629eb8e63199d9eb7dc3a'}, 'mac': 'e267d870e14980c5b060a2a3ebe78b7ba088ef2d2b4a83c21246c5a53467febc'}, 'id': '86e8eae1-b980-4a03-b169-dd7d198d3e6f', 'version': 3}
