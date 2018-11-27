# coding:utf-8
from mnemonic.mnemonic import Mnemonic
from util.mnemonic_utils import mnemonic_to_private_key
from util.compile_solidity_utils import w3
from eth_account import Account
m = Mnemonic('english')
mnemonic = m.generate()
private_key = mnemonic_to_private_key(mnemonic)
account = w3.eth.account.privateKeyToAccount(private_key)
address = account.address
wallet = Account.encrypt(private_key, "112")
print(mnemonic)
print(private_key.hex())
print(address)
print(wallet)
# private_key = account._key_obj
# public_key = private_key.public_key
# address = public_key.to_checksum_address()
# wallet = Account.encrypt(account.privateKey, pwd)



