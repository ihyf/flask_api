import requests
import json
"""curl -H "Content-Type: application/json" --request POST -d '{
        "method": "user_contract",
        "params": {"name": "John Doe", "gender":"male"},
        "jsonrpc": "2.0",
        "id": 0,
    }' http://localhost:4000/api
"""
def main():
    url = "http://localhost:3000/api"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "send_transaction",
        "params": {
            "to_address": "0xdc948Ac6BF4AA1107e6edD08391aeCfAfF602564",
            "from_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
            "value": 122,
            "pwd": "hyf",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)


if __name__ == "__main__":
    main()