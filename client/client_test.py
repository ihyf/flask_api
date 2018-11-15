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
    
    keystore = {"address": "198bce50b62c70cc691362d6c1ffbf7fb95045ce", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "cea79bc62e3cb698343ce4be5417a540"}, "ciphertext": "b7f5ad1e961a125e75b7d13cb26b887abb7d9dccda8860c4bddde548c3863657", "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256", "salt": "ea1e86e8172fe19d46bfb83085949b72"}, "mac": "5f5f0437d6bd8971ba358a6d80f58a5aaae5d1fb6a5a660afb5bf04823741bc7"}, "id": "27d686e8-0043-4ca7-b434-9c78cf216024", "version": 3}

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
    payload = {
        "method": "create_account",
        "params": {"pwd": "hyf"},
        "jsonrpc": "2.0",
        "id": 0
        }
    # payload = {
    #     "method": "send_transaction1",
    #     "params": {
    #         "to_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
    #         "from_address": "0x198bCe50B62c70CC691362d6C1FFBF7FB95045cE",
    #         "value": 1,
    #         "pwd": "hyf",
    #         "keystore": keystore
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)
{
	"result": {
		"address": "0xe3A81Fc2C6d38763D2C167A602B1b540554f57F4",
		"keystore": {
			"address": "e3a81fc2c6d38763d2c167a602b1b540554f57f4",
			"crypto": {
				"cipher": "aes-128-ctr",
				"cipherparams": {
					"iv": "75371729d87a56b9598c69533856a5d3"
				},
				"ciphertext": "2119778e59ab0191419c6134423241948e862a8b979258cfa73e4e61a83f2b79",
				"kdf": "pbkdf2",
				"kdfparams": {
					"c": 1000000,
					"dklen": 32,
					"prf": "hmac-sha256",
					"salt": "9acab82ebea752bf921cc408966e8b21"
				},
				"mac": "5593bf5c41bf9a3b9fb2ddc7764125b63739d5e39dd649d498444ec7c4c736d1"
			},
			"id": "b6875b47-0dca-457e-9d13-236e7a4f15bb",
			"version": 3
		}
	},
	"id": 0,
	"jsonrpc": "2.0"
}

if __name__ == "__main__":
    main()