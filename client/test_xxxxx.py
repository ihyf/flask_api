# import requests
#
# url = "http://192.168.1.11:82/upload/luckyNumber.sol"
# response = requests.get(url)
# print(response.content)
# with open("xx.sol", "w", encoding="utf-8") as f:
#     f.write(response.content.decode())
#     f.close()
#
# func_name = 1
# func_param = 1
# account = 1
# nonce = 1
# value = 1
# s1 = f"""contract_instance.functions.{func_name}({func_param}).
# transact({{'from': '{account}', 'value': w3.toWei(0, 'ether')}}).
# buildTransaction({{'chainId': 1500, 'gas': 7000, 'gasPrice': w3.toWei('0.01', 'ether'), 'nonce': {nonce}}})"""
# # print(s1)
#
# ssss = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 7000, 'gasPrice': w3.toWei('0.01', 'ether'), 'nonce': {nonce}}})"""
# print(ssss)

from util.compile_solidity_utils import w3
# data = w3.eth.waitForTransactionReceipt()
# print(data)
# data1 = w3.eth.getTransaction("0xa712d2c1aa9cf9db7459650f4c94c1599deb4ad63a79f55427a81d0cd502f849")
# print(data1)
import datetime
t = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
print(t)
