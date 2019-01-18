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
    
    keystore_node1 = {"address":"b5143167d9873699ec2ba75917c4661e5f8ab04d","crypto":{"cipher":"aes-128-ctr","ciphertext":"d817054e98aeb13f891d21995860a69b8312be6609b26e7d09110333196e1910","cipherparams":{"iv":"a886543aaa99095f1c5f80c4b204c68b"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"8f3b652fcb14f5f3e87847d3860e1da3dbb06ed03b36b0a35143eb954f5967c0"},"mac":"d386dbeee949ab658c9409c645baecf94fc153593cef82b6d93fafbcc4d5efc6"},"id":"578e661b-5ddd-4da9-be77-9df6e406d11e","version":3}
    keystore_node1_create = {"address": "5b365efb9c6142678fcb1cefe39180754c6e5d91", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "bad335f6fbfe302a3805983f46f2447a"}, "ciphertext": "1f7b91bf1ee929c581becafbab1afc32f4a0fbdd30ccde73c6a061cd2fc48e6a", "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256", "salt": "b610efc763cede53535ef0268ff2822d"}, "mac": "0542b308ea83fb76c1da5371b34b0618fececcbba93ab4e6fc80912683966137"}, "id": "ec93dfb7-dcce-437a-a4fe-f83aa0aae082", "version": 3}
    keystore_node1_create_02 = {"address": "6b9f89be707fe4eb772f9f37e47bbba4089b56fc", "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "fe29e948049e1788af34aa568b0d913d"}, "ciphertext": "2b5803ae915b94861a7308c42ae178e1a8976af529f262169d1c94dc88b8f7be", "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256", "salt": "527ca4bb50731d15da25f3ca945831f6"}, "mac": "f18be87ed64d2007fb2d5bc1b2fe17adfa46a5326ce4f48abc2e7cd940dfe1fb"}, "id": "c685e48f-bd70-47ce-b58f-0facb8f98919", "version": 3}
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
                "to_address": "0x6b9f89be707fe4eb772f9f37e47bbba4089b56fc",
                "value": 0.1,
                "gas_limit": 30000,
                "gas_price": 20000,
                "pwd": "123456",
                "keystore": keystore_node1,
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
#     "0x5b365efb9c6142678fcb1cefe39180754c6e5d91"
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
