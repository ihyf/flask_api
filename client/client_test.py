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
    geth_url = "http://192.168.1.33:8101"
    url = "http://localhost:9000/api"
    url1 = "http://192.168.1.14:9000/api"
    headers = {"content-type": "application/json"}
    
    keystore_node1 = {'address': 'f323f1903fcd008206bba9d905bdeacd61f498e7', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '6c3bd1f44b67c8a6387c0650801b73c3'}, 'ciphertext': 'e52f85af32f9cbf3d02cc44c616bf4be30df380a92ee968ce0a103fe6aaebd86', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '36a478ce205ea8108cf10879e418f519'}, 'mac': '4883a52cf8f39733e2777e747f3d6632eef2419714a7498ed9e3f82cf6e36291'}, 'id': 'a61dd6a0-2dcd-46c4-b8b4-f21b97aba326', 'version': 3}
    keystore_node1_create = {
    "address": "7cc57311da4a8871697074f6515589802223e892",
    "crypto": {
        "cipher": "aes-128-ctr",
        "cipherparams": {
            "iv": "88ff9f2aff0daace1c6f45021150ca55"
        },
        "ciphertext": "037e7a0df2c270434a24248f9924ffaa1496c8a6d463b8ef3e80d38ac59abb49",
        "kdf": "pbkdf2",
        "kdfparams": {
            "c": 1000000,
            "dklen": 32,
            "prf": "hmac-sha256",
            "salt": "b2efef6c3f7596140609b1cfe0fafb02"
        },
        "mac": "afa24aef26f8b3015b99c97de0b37fbeedb2b057109529ac65dd73d798701834"
    },
    "id": "1ae2dd37-9840-4c3f-9937-f48203e15e98",
    "version": 3
}
    keystore_3 ={
    "address": "d26d9296d23ad149be65c8102954cf474de239cc",
    "crypto": {
        "cipher": "aes-128-ctr",
        "cipherparams": {
            "iv": "b39057f830251797fe525d3180875807"
        },
        "ciphertext": "5bad2f87dc3d8162e90feacf73a9943b8edb6ed1c17bbb5f81b5075125b70472",
        "kdf": "pbkdf2",
        "kdfparams": {
            "c": 1000000,
            "dklen": 32,
            "prf": "hmac-sha256",
            "salt": "056778b197a6d59a113b93daf588ba1a"
        },
        "mac": "674928faefb7e2974e300044ad6c0f8c6bcc8d85e692f3906926bf45e1afd413"
    },
    "id": "081d8a26-7ac2-4dfe-be26-b449e880dc8d",
    "version": 3
}
    keystore4 = {'address': 'f323f1903fcd008206bba9d905bdeacd61f498e7', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '6c3bd1f44b67c8a6387c0650801b73c3'}, 'ciphertext': 'e52f85af32f9cbf3d02cc44c616bf4be30df380a92ee968ce0a103fe6aaebd86', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '36a478ce205ea8108cf10879e418f519'}, 'mac': '4883a52cf8f39733e2777e747f3d6632eef2419714a7498ed9e3f82cf6e36291'}, 'id': 'a61dd6a0-2dcd-46c4-b8b4-f21b97aba326', 'version': 3}
    # payload = {
    #     "method": "create_account",
    #     "params": {
    #         "appid": "hyf_app",
    #         "sign": "",
    #         "data": {
    #             "pwd": "hyf",
    #             "time": time.time()
    #         }
    #     },
    #     "jsonrpc": "2.0",
    #     "id": 0
    # }

    payload = {
        "method": "send_transaction",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "to_address": "0xf323f1903fcd008206bba9d905bdeacd61f498e7",
                "value": 0.1,
                "gas_limit": 200000,
                "gas_price": 3000,
                "pwd": "hyf",
                "keystore": keystore_node1_create,
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": 0
    }
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
#                 "address": [
#     "0x5112f5B7Fea80cADc1F103Cc9A9805c2a4B116aE",
#     "0x2d3168E80413Ac2799Bbb24BAE54825C057819C7",
#     "0x32b1a7eb38F52fca841843789E114f46e682d165",
#     "0x148cB4b6953669ee3ecc74d060Fb7c2475201b66"
# ],
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
