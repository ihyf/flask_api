from web3 import Web3, WebsocketProvider

from util.check_fuc import format_func_param

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# func_param = "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1, 2, 3"
# func_param = format_func_param(func_param)
account = 1
nonce = 1
func_name = "tSaveMoney"
value = 1
# ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
# print(ss1)

func_param = ""
func_param = format_func_param(func_param)
s1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""

print(s1)



