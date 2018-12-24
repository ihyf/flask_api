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
    url1 = "http://192.168.1.14:8080/api"
    headers = {"content-type": "application/json"}
    
    keystore = {
        "address": "bedc1e0341a85a571243990d7bc057a554966ce5",
        "crypto": {
            "cipher": "aes-128-ctr",
            "cipherparams": {
                "iv": "a8571c222a67b059d0cfb0d04af71cf6"
            },
            "ciphertext": "b3ada3efa4a6bead7de955afd9ec95e521c74723a7cb393af169973fbbece98f",
            "kdf": "pbkdf2",
            "kdfparams": {
                "c": 1000000,
                "dklen": 32,
                "prf": "hmac-sha256",
                "salt": "41e0329a96a2282e6ec12a68c2b2ffd1"
            },
            "mac": "55fc89cf14ab4d5abc98535bb5eb8238123bbc7e1543dae1d596e7a92772c816"
        },
        "id": "e1c4c381-23b8-47d6-b517-ef4c395ae33d",
        "version": 3
    }

    payload = {
        "method": "create_account",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "pwd": "hyf",
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": 0
    }

    # payload = {
    #     "method": "send_transaction",
    #     "params": {
    #         "appid": "hyf_app",
    #         "sign": "",
    #         "data": {
    #             "to_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
    #             "value": 1,
    #             "gas_limit": 200000,
    #             "gas_price": 3000,
    #             "pwd": "hyf",
    #             "keystore": keystore,
    #             "time": time.time()
    #         }
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }
    # payload = {
    #     "method": "import_private_key",
    #     "params": {
    #         "appid": "hyf_app",
    #         "sign": "",
    #         "data": {
    #             "private_key": "1e6dba0c25e107e68c536b1705f0d91fd942769c2407b7752ea5e5eff396ba42",
    #             "pwd": "hyf",
    #             "time": time.time()
    #         }
    #     },
    #     "jsonrpc": "2.0",
    #     "id": ""
    # }

#     payload = {
#     "method": "get_all_transaction",
#     "params": {
#         "appid": "hyf_app",
#         "sign": "",
#         "data": {
#             "address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
#             "time": time.time()
#         }
#     },
#     "jsonrpc": "2.0",
#     "id": ""
# }
#     payload = {
#         "method": "get_balance",
#         "params": {
#             "appid": "hyf_app",
#             "sign": "",
#             "data": {
#                 "address": ["0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1", "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1", "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1", "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1"],
#                 "time": time.time()
#             }
#         },
#         "jsonrpc": "2.0",
#         "id": 0
#     }
    
    from cert.eth_certs import EthCert
    ec = EthCert("hyf_app")
    ec.load_key_from_file()
    ec.serialization()
    sign = ec.sign(payload["params"]["data"])
    payload["params"]["sign"] = sign.decode()
    
    ec1 = EthCert("hyf_srv")
    ec1.load_key_from_file()
    ec1.serialization()
    payload["params"]["data"] = ec1.encrypt(payload["params"]["data"]).decode()

    for i in range(1):
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
    
    print(response)
    ddata = ec.decrypt(response["result"]["data"])
    print(ddata)
    # print(ec1.verify(ddata, response["result"]["sign"]))


if __name__ == "__main__":
    main()
