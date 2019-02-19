import requests
import json
import time
from util.compile_solidity_utils import w3
import urllib3
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
    url_waiwang = "http://47.52.166.23:9000/api"
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
    keystore_hyf = {"address":"e05c112ca739671f014efc2e684b9ac96865d459","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"277c5a4cd33901350007c9c87670f293"},"ciphertext":"dd44c7257cb33b572827ef7e2c5cebb3bba538760a9b68d1ec34de00a45665c3","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"72a6ec62856d92f09a4510751dc19140"},"mac":"55c3f7be7cfd9d52f2bb37d9dda1356f7d252e08d4d809eb9cdf22f37c1e3318"},"id":"74b8a9b8-49c8-4b01-ae73-ac0a83a83c7e","version":3}
    keystore_poa_node1 = {"address":"3ff83cc121adae7953cc96c8fab1463c2756d4d6","crypto":{"cipher":"aes-128-ctr","ciphertext":"9159d08b6b72b26cb9aa0eb22776ad73f12444d1c333f1b77a6350497fbcf486","cipherparams":{"iv":"d073e228b007782f029f2f229c585ddc"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"5e1146850019085d042a7b660d6f6e99266e35d797a5e55d7402c263f4b96c9f"},"mac":"4301617ced915e9a22b5f93b937d8a61f4113a34615feb681cdb0f8a8db87b51"},"id":"e82ce4db-c07a-4959-8c8c-a0e17fd0d6ab","version":3}
    k_hyf = {"address":"a53683641b86640e539f5224e3a062b10fe8c830","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"0be3e7461ab510e0a4a56bd3c55ba785"},"ciphertext":"94bd89d02f3bfee46e6634c15cba5ad2d4449daf03bd811780069cda880b5181","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"6446f4ef06f1c58794fc8aae631950b3"},"mac":"375e14236a14df9507ad0737a7b037b7e18051a2899edd6ee7092afc6af28eee"},"id":"6d8f91a9-f18d-4377-b590-49befcd8eb04","version":3}
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
    kdd8 = {'address': '3af1ee88d8e3987294073896c5bf6cf07474de74', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'dabb2bbd3511c19bcc19bf4b26811c41'}, 'ciphertext': '4443b3df9d0f642c062cd66b74a830e62830f3b9ea9ec64ec097641f2f50ee5c', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '542004944fcff3605f0843f983921f76'}, 'mac': '86b824bc2e8262fa488db35b126dcccea1163f04964d9de404266a2cad6223f5'}, 'id': 'bb63bb14-627c-4a17-bdcb-2b32ae214185', 'version': 3}
    k6 = {'address': '25d239ea15c864b44beb14d97f97cf74fe8f516d', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'f79187a8a06b7ff604f3769ac146fa05'}, 'ciphertext': 'ebb42feff845f52bd5b210be5ac0a774a0d913e830229cf216d597c14d6c0d3f', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'f5941f1ab1f00d69a32c1f0714bd6883'}, 'mac': '285ddb48eb459bc71b787181014b227c53cbcb08a6601f5a45edb3852f694ae8'}, 'id': '07a3e21e-19d8-4d4e-9e5a-cbe57a36e755', 'version': 3}
    k9 = {'address': '564871bc2f5768abd302b8631398cca4626af875', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '1fbc4571850557ee4e6dee01de1567da'}, 'ciphertext': 'f6706e129ef78bcccc1e4ff257140a493c20548231bb98cab964ee9253fdc849', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '7e877bd615b4416e5d6a50bed73a5b75'}, 'mac': 'c501fddc6595bbe10eef51285295598645db424436c97f040276f811456858e5'}, 'id': '29c9dcb8-fa0a-4deb-a38f-1809b5491245', 'version': 3}
    
    k_create_account_to_new_100 = {"address":"8a47c8aadbbe059ed1fa26224678ee06b46c4c82","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"a6e3caaa6cc10470eb0cedcc4f3568b6"},"ciphertext":"54f7bbb940ba31fd58640d929b282ab30bd14fb2ad528f34f07be635b3c4cba1","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"be89b5c10e32de78c4743854ee6e66e0"},"mac":"ab9acf1f49d97c38ec63b7719cec8185a1f8bd6544248ee5c599ca4c93a54d52"},"id":"a6d10ad2-6647-483a-a0ae-c6d1a72efe31","version":3}
    k8 = {'address': '5d3e9c2b6909489fb4e68628f769047abfbf3e0a', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'f6848d524e2c1e68bfde83d0abb6f9ea'}, 'ciphertext': '8507b93dfc413306b77fdc4295e3ec7c077d5366b598a227df95862f5d279291', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '28f1e57173172bc5d3b79a58eec37ca4'}, 'mac': '4aa2e5f2a4131088b7cee3c58f1ad94a34a5da8c252462026472c67bad9093df'}, 'id': '2bdfd378-242f-4275-b53d-50cee66b4c5f', 'version': 3}
    gas_price = w3.eth.gasPrice
    print(gas_price)
    payload = {
        "method": "send_transaction",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "to_address": "0x5030a2589e9a0bd58fd6708f92c325c7b9433118",
                "value": 99000000,
                "gas_limit": 40000,
                "gas_price": gas_price,
                "pwd": "hyf",
                "keystore": k8,
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
#             "address": "0xC2AC9218d05cE91Bd891b936df08FaE5d298eD94",
#             "page": 1,
#             "limit": 10,
#             "time": time.time()
#         }
#     },
#     "jsonrpc": "2.0",
#     "id": ""
# }
    payload = {
            "method": "get_balance",
            "params": {
                "appid": "hyf_app",
                "sign": "",
                "data": {
                    "address": ["0xcddd1a4d1c811e9ef5fa392266de98022107583f",
                                "0xcddd1a4d1c811e9ef5fa392266de98022107583f"],
                    "time": time.time()
                }
            },
            "jsonrpc": "2.0",
            "id": 0
        }
#     payload = {
#     "method": "get_all_transaction",
#     "params": {
#         "appid": "hyf_app",
#         "sign": "",
#         "data": {
#             "address": "0xe6aAE8cd183383c161117158c8Ba7A4D02F45fDf",
#             "page": 1,
#             "limit": 10,
#             "time": time.time()
#         },
#
#     },
#     "jsonrpc": "2.0",
#     "id": 0
# }
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
            url_waiwang, data=json.dumps(payload), headers=headers).json()

    print(response)
    ddata = ec.decrypt(response["result"]["data"])
    print(ddata)
    print(ec1.verify(ddata, response["result"]["sign"]))


if __name__ == "__main__":
    main()
