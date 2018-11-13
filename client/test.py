# coding:utf-8
from web3 import Web3, HTTPProvider
import json
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

x = json.dump(w3.eth.getBlock(12))
print(x)
