# coding:utf-8
import requests
import json
payload = {
        "method": "user_contract",
        "params": {"name": "hyf", "gender": "nan"},
        "jsonrpc": "2.0",
        "id": 0
    }
url = "http://localhost:3000/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)
