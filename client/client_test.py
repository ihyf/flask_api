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
    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "to_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
    #         "from_address": "0x330B1B086ef86FAD4b4df5104402EF0a9015C001",
    #         "value": 10,
    #         "pwd": "hyf111",
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # }
    payload = {
        "method": "get_all_transaction",
        "params": {"address": "0xf6631aF8B574c6b8cEfeca5104Ad1BfE8EAEaa4A"},
        "jsonrpc": "2.0",
        "id": 0
        }
    
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)


if __name__ == "__main__":
    main()