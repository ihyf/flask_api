# coding:utf-8
import requests
import json
from util.compile_solidity_utils import w3
s = "hyf"
from util.check_fuc import to_byte32
# s = to_byte32("hyf")
payload = {
        "method": "play_contract1",
        "params": {"voting_list": "aaa"},
        "jsonrpc": "2.0",
        "id": 0
    }

url = "http://192.168.1.14:8080/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)






