import time

import requests
import json
from cert.eth_certs import EthCert

keystore_poa_node1 = {"address": "3ff83cc121adae7953cc96c8fab1463c2756d4d6", "crypto": {"cipher": "aes-128-ctr",
                                                                                        "ciphertext": "9159d08b6b72b26cb9aa0eb22776ad73f12444d1c333f1b77a6350497fbcf486",
                                                                                        "cipherparams": {
                                                                                            "iv": "d073e228b007782f029f2f229c585ddc"},
                                                                                        "kdf": "scrypt",
                                                                                        "kdfparams": {"dklen": 32,
                                                                                                      "n": 262144,
                                                                                                      "p": 1, "r": 8,
                                                                                                      "salt": "5e1146850019085d042a7b660d6f6e99266e35d797a5e55d7402c263f4b96c9f"},
                                                                                        "mac": "4301617ced915e9a22b5f93b937d8a61f4113a34615feb681cdb0f8a8db87b51"},
                      "id": "e82ce4db-c07a-4959-8c8c-a0e17fd0d6ab", "version": 3}
dapp_keysetore_poa = {"address": "a84684b7db41dae3a26a5ca7b87bc967a8dd1107",
                      "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "96dadfa262f840e52490585e29ae60ed"},
                                 "ciphertext": "1f7aa48033d5ceb0084fa6aee58e3d595b4fa0c463b1f4acdca8e576d0e89882",
                                 "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256",
                                                                "salt": "5384d6054493a41248f3a3436cd97386"},
                                 "mac": "465ce97cbfde26d71f1ed0c0f948de941af123d26cd92e348da6352296d55544"},
                      "id": "5d711d39-e130-411c-af71-91e835127b04", "version": 3}
to_100_keystore = {"address": "a4c013179c761a284197f8b4be18a74525650062",
                   "crypto": {"cipher": "aes-128-ctr", "cipherparams": {"iv": "2829511654c451cf7190f335ccfa2cf1"},
                              "ciphertext": "e865c7185014f0dc95150b55a5d892c54b4407aa708c8fc8f46584e74451f6dc",
                              "kdf": "pbkdf2", "kdfparams": {"c": 1000000, "dklen": 32, "prf": "hmac-sha256",
                                                             "salt": "9f939221e50b35d5972f85c5e7d0cf02"},
                              "mac": "950643be3039106333dd1198e1cb3f156eaa1c8e136a66fde2c09c5b7e937ffd"},
                   "id": "74d4b229-a702-423f-9028-0ef0a52bb5de", "version": 3}


class Hyf(object):
    def __init__(self):
        # self.appid = "hyf_app"
        self.appid = "c66816dbb90591b1a1740ea0dc9b602e"
        self.headers = {
            "content-type": "application/json",
            "Authorization": "poa test"
        }
        self.payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "",
            "params": {
                "appid": self.appid,
                "sign": "",
                "data": {
                
                }
            }
        }
        self.ec_cli = EthCert("c66816dbb90591b1a1740ea0dc9b602e_cli")
        # self.ec_cli = EthCert("hyf_app")
        # self.ec_srv = EthCert("hyf_srv")
        self.ec_srv = EthCert("c66816dbb90591b1a1740ea0dc9b602e_srv")
        self.ec_cli.load_key_from_file()
        self.ec_cli.serialization()
        self.ec_srv.load_key_from_file()
        self.ec_srv.serialization()
        self.url_waiwang = "http://47.52.166.23:9000/api"
        self.url_neiwang = "http://192.168.1.14:9000/api"
        self.url_local = "http://localhost:9000/api"
    
    def send_request(self, url, method, data):
        self.payload["method"] = method
        self.payload["params"]["sign"] = self.ec_cli.sign_str(data)
        self.payload["params"]["data"] = self.ec_srv.encrypt_str(data)
        
        response = requests.post(url=url, data=json.dumps(self.payload), headers=self.headers)
        if isinstance(response, bytes):
            response = response.decode()
        else:
            response = response.json()
        print(response)
        ddata = self.ec_cli.decrypt(response["result"]["data"])
        print(ddata)
        print(self.ec_srv.verify(ddata, response["result"]["sign"]))
    
    def test_create_account(self):
        method = "create_account"
        data = {
            "pwd": "hyf",
            "time": time.time()
        }
        self.send_request(url=self.url_neiwang, method=method, data=data)
    
    def test_get_balance(self):
        method = "get_balance"
        data = {
            "address": [
                "0xa4c013179c761a284197f8b4be18a74525650062",
                "0xa4c013179c761a284197f8b4be18a74525650062"
            ],
            "time": time.time()
        }
        self.send_request(url=self.url_waiwang, method=method, data=data)
    
    def test_send_transaction(self):
        method = "send_transaction"
        data = {
            "to_address": "0xa84684b7db41dae3a26a5ca7b87bc967a8dd1107",
            "value": 5000000,
            "gas_limit": 40000,
            "gas_price": 90000000,
            "pwd": "123456",
            "keystore": keystore_poa_node1,
            "time": time.time()
        }
        self.send_request(url=self.url_local, method=method, data=data)
    
    def test_use_contract(self):
        method = "transfer_contract"
        data = {
            "func_name": "getPlay",
            "func_param": "0xa4c013179c761a284197f8b4be18a74525650062",
            "value": "0",
            "keystore": to_100_keystore,
            "pwd": "hyf",
            "time": time.time()
        }
        self.send_request(url=self.url_waiwang, method=method, data=data)
    
    def test_add_master_contract(self):
        method = "add_master_contract"
        data = {
            "master_contract_name": "hyf_master_20190222_1825",
            "time": time.time()
        }
        self.send_request(url=self.url_neiwang, method=method, data=data)
    
    def test_deploy_contract(self):
        method = "deploy_contract"
        data = {
            "contract_name": "luckyNumber_0222_1825",
            "url": "123",
            "master_contract_name": "hyf_master_20190222_1825",
            "master_contract_address": "0x475CBDA0d1C7c922a6883eC2BEE7387f44F2C594",
            "time": time.time()
        }
        self.send_request(url=self.url_local, method=method, data=data)


if __name__ == "__main__":
    hyf = Hyf()
    # hyf.test_add_master_contract()
    # hyf.test_deploy_contract()
    # hyf.test_use_contract()
    # hyf.test_create_account()
    # hyf.test_get_balance()
    # hyf.test_send_transaction()
