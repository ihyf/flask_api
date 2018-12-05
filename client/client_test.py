import requests
import json
"""curl -H "Content-Type: application/json" --request POST -d "{
        "method": "user_contract",
        "params": {"name": "John Doe", "gender":"male"},
        "jsonrpc": "2.0",
        "id": 0,
    }" http://localhost:4000/api
"""
def main():
    url = "http://localhost:3000/api"
    headers = {"content-type": "application/json"}
    
    keystore = \
	{'address': '7c908389026b978422cd8ee9d28c17c44fad7af0',
	 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'd2fdbce8725e93d736b5c1ad3926c72d'},
				'ciphertext': '741e8d9c4d15d2d9f5c979e3a692094c0335b673c11aacfc88fb01396481421a', 'kdf': 'pbkdf2',
				'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256',
							  'salt': '3dc4d554d1ed511dc75a0fdfa6734848'},
				'mac': '9d589f6f1b5120517fb2ba04a26555da6f70a485172e585d71c37dc0effda4b7'},
	 'id': '488c4ff2-429d-4bc1-aaf2-4c186d0c7970', 'version': 3}

    # Example echo method
    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "to_address": "0x11a64FC5Da3EaACa563b417c447F66bdC80f15E9",
    #         "from_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
    #         "value": 10,
    #         "pwd": "hyf",
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # }
    # payload = {
    #     "method": "create_account",
    #     "params": {"pwd": "hyf"},
    #     "jsonrpc": "2.0",
    #     "id": 0
    #     }
    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "to_address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
    #         "from_address": "0x792DE4e56ec5280694C7e4cAc4e831D831FBE568",
    #         "value": 2,
    #         "pwd": "hyf",
    #         "keystore": keystore
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    payload = {
        "method": "test1",
        "params": {"address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1"},
        "jsonrpc": "2.0",
        "id": 0
    }
    for i in range(1):
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
    
        print(response)


if __name__ == "__main__":
    main()
