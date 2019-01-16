from util.compile_solidity_utils import w3
from eth_account import Account
private_key = "0xd3d0b8a859da969c43e8ba1b531b8ac0e630e4828e36b67fc43a0fa6e698f3f9"
pwd = "hyf"

account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, pwd)
print(wallet)

wallet = {'address': 'f323f1903fcd008206bba9d905bdeacd61f498e7', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '6c3bd1f44b67c8a6387c0650801b73c3'}, 'ciphertext': 'e52f85af32f9cbf3d02cc44c616bf4be30df380a92ee968ce0a103fe6aaebd86', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '36a478ce205ea8108cf10879e418f519'}, 'mac': '4883a52cf8f39733e2777e747f3d6632eef2419714a7498ed9e3f82cf6e36291'}, 'id': 'a61dd6a0-2dcd-46c4-b8b4-f21b97aba326', 'version': 3}
