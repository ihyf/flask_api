# coding:utf-8
from mnemonic.mnemonic import Mnemonic
from util.mnemonic_utils import mnemonic_to_private_key
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/aecf3f6cff734350aca78d0f15d252db"))
# from eth_account import Account
# m = Mnemonic('english')
# mnemonic = m.generate()
# private_key = mnemonic_to_private_key(mnemonic)
# account = w3.eth.account.privateKeyToAccount(private_key)
# address = account.address
# # wallet = Account.encrypt(private_key, "112")
# print(mnemonic)
# print(private_key.hex())
# print(address)
# print(wallet)
# private_key = account._key_obj
# public_key = private_key.public_key
# address = public_key.to_checksum_address()
# wallet = Account.encrypt(account.privateKey, pwd)


address = w3.toChecksumAddress("0x19e8e0D062856cd7c5B639D219284bcEB0027E14")
eth_balance = w3.fromWei(w3.eth.getBalance(address, 'latest'), 'ether')
eth_balance = str(eth_balance)
print(eth_balance)


