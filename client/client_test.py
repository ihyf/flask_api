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
    
    keystore = {'address': '198bce50b62c70cc691362d6c1ffbf7fb95045ce', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'cea79bc62e3cb698343ce4be5417a540'}, 'ciphertext': 'b7f5ad1e961a125e75b7d13cb26b887abb7d9dccda8860c4bddde548c3863657', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'ea1e86e8172fe19d46bfb83085949b72'}, 'mac': '5f5f0437d6bd8971ba358a6d80f58a5aaae5d1fb6a5a660afb5bf04823741bc7'}, 'id': '27d686e8-0043-4ca7-b434-9c78cf216024', 'version': 3}

    # Example echo method
    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "to_address": "0xbe8aA6eA0488B92B644327D5106390B4c0F6F49d",
    #         "from_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
    #         "value": 10,
    #         "pwd": "hyf111",
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # }
    # payload = {
    #     "method": "create_account1",
    #     "params": {"password": "hyf"},
    #     "jsonrpc": "2.0",
    #     "id": 0
    #     }
    payload = {
        "method": "send_transaction1",
        "params": {
            "to_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
            "from_address": "0x198bCe50B62c70CC691362d6C1FFBF7FB95045cE",
            "value": 1,
            "pwd": "hyf",
            "keystore": keystore
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)


if __name__ == "__main__":
    main()