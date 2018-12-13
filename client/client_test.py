import requests
import json
import time
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
    
    keystore = {
    "address": "bedc1e0341a85a571243990d7bc057a554966ce5",
    "crypto": {
        "cipher": "aes-128-ctr",
        "cipherparams": {
            "iv": "0e7dab3c2fef8bbd70b2a7a12ba01633"
        },
        "ciphertext": "820473a094929db7923f37fcf0b1f1d1434563d2c58ba2ba536dffb74b3d251b",
        "kdf": "pbkdf2",
        "kdfparams": {
            "c": 1000000,
            "dklen": 32,
            "prf": "hmac-sha256",
            "salt": "1ee7233d8e954c35dbbe32476f13ed39"
        },
        "mac": "9012f4059fc223f485ca6acce7089f0d4b4d51e5eea0215eca5903b126b532fd"
    },
    "id": "275413f5-89d7-4c2b-91c5-ceee7c167ef8",
    "version": 3
}

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
#     payload = {
#     "method": "create_account",
#     "params": {
#         "appid": "hyf_app",
#         "sign": "",
#         "data": {
#             "pwd": "hyf"
#         }
#     },
#     "jsonrpc": "2.0",
#     "id": 0
# }
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
    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "appid": "hyf_app",
    #         "sign": "",
    #         "data": {
    #             "to_address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
    #             "value": 10,
    #             "gas_limit": 200000,
    #             "gas_price": 3000,
    #             "pwd": "hyf",
    #             "keystore": keystore
    #         }
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    payload = {
        "method": "export_private",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "keystore": keystore,
                "pwd": "hyf",
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": ""
    }
    
    from cert.eth_certs import EthCert
    ec = EthCert("hyf_app")
    ec.load_key_from_file()
    ec.serialization()
    sign = ec.sign(payload["params"]["data"])
    print("sign")
    print(sign)
    payload["params"]["sign"] = sign.decode()
    
    ec1 = EthCert("hyf_srv")
    ec1.load_key_from_file()
    ec1.serialization()
    payload["params"]["data"] = ec1.encrypt(payload["params"]["data"]).decode()

    
    print("xxx")
    print(payload["params"]["data"])
    # print(payload)
    for i in range(1):
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        # print(response)
    ddata = ec.decrypt(response["result"]["data"])
    # print(ddata)  # jiamishuju
    # print(ec1.verify(ddata, response["result"]["sign"]))


if __name__ == "__main__":
    main()
