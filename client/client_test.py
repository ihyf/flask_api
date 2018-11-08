import requests
import json

def main():
    url = "http://localhost:4000/api"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "my_method",
        "params": [{"name":"John Doe","gender":"male"}],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)


if __name__ == "__main__":
    main()