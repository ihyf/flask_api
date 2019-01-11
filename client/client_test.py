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
    url1 = "http://localhost:9000/api"
    url = "http://192.168.1.14:9000/api"
    headers = {"content-type": "application/json"}
    
    keystore = {'address': '77fb4a966385a0d160457416fbf4b4cccf91f62e', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '0231557c41387c1277f33f82f00c7b02'}, 'ciphertext': '01cabb2429e8071ef8d073954e84f90e96f1522f1b1417e15b020be4b932c6c0', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'be64122d157629eb8e63199d9eb7dc3a'}, 'mac': 'e267d870e14980c5b060a2a3ebe78b7ba088ef2d2b4a83c21246c5a53467febc'}, 'id': '86e8eae1-b980-4a03-b169-dd7d198d3e6f', 'version': 3}

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
                "to_address": "0xFa54B304c5b1F6344e069dc35e3f23a5971bc5b9",
                "value": 20,
                "gas_limit": 200000,
                "gas_price": 3000,
                "pwd": "hyf",
                "keystore": keystore,
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
