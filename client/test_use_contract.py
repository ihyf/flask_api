# coding:utf-8
import requests
import json
from util.compile_solidity_utils import w3
s = "hyf"
from util.check_fuc import to_byte32
# s = to_byte32("hyf")
"play_contract1"
"play_contract2"
"get_num"
"0xd87f9a8fe5e66cf3e1e06d8f6c4774fba4da372731dd2828186fe06aa373669f"
a0 = "0x3de2a8cceffe9e3dc5022991743ba0ade3765649"
a2 = "0xbefddca2dbf1d1ad3da72c334c31c3ab5aac8bd3"

a1 = "0x0bee62b2b06bd4ecf8c14444b076bbfe28bf2889"
"betting" "getRandom" "result"
"transfer_contract"
"luckyNumber_contract"
payload = {
        "method": "luckyNumber_contract",
        "params": {
            "account": a0,
            "contract_name": "luckyNumber",
            "func_name": "getBalance",
            "func_param": ""
        },
        "jsonrpc": "2.0",
        "id": 0
    }

url = "http://192.168.1.14:8080/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)






