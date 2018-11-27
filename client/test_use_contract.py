# coding:utf-8
import requests
import json
payload = {
        "method": "voting_contract",
        "params": {"voting_list": ["zhangsan", "lisi", "wangwu"]},
        "jsonrpc": "2.0",
        "id": 0
    }
url = "http://192.168.1.14:8080/api"
headers = {"content-type": "application/json"}
# response = requests.post(
#             url, data=json.dumps(payload), headers=headers).json()
# print(response)

print(json.dumps([1, 2, 3]))
