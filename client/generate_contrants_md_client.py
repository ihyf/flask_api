import requests
import json
import time


url = "http://127.0.0.1:3000/api"
headers = {"content-type": "application/json"}


payload = {
        "method": "generate_contrants_md",
        "params": {
            "time": time.time()
        },
        "jsonrpc": "2.0",
        "id": 0
    }


for i in range(1):
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

print(response)
