import requests
import json

payload = {
        "method": "add_app",
        "params": {
        
        },
        "jsonrpc": "2.0",
        "id": 11
    }
url = "http://127.0.0.1:3000/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)
