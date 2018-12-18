import requests
import json
import time
import re
from cert.eth_certs import EthCert

"""接口测试用"""


class DianDian(object):

    def __init__(self):
        self.ec_cli = EthCert("diandian_cli")
        self.ec_cli.load_key_from_file()
        self.ec_cli.serialization()
        self.ec_srv = EthCert("diandian_srv")
        self.ec_srv.load_key_from_file()
        self.ec_srv.serialization()

    def request(self, data):
        headers = {
            'content-type': "application/json",
            'Authorization': 'PyCharm Test'
        }
        response = requests.post("http://192.168.1.14:8080/api", data=json.dumps(data), headers=headers)
        return response.text

    def request_json(self, method, sign, encrypt):
        post_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": {
                "appid": "diandian",
                "sign": sign,
                "data": encrypt
            }
        }
        return post_data

    def check_rt(self, res):
        res_js = json.loads(res)
        if "error" in res_js:
            return res_js
        res_data = res_js['result']
        if res_data['code'] == "success":
            decrypt_data = self.ec_cli.decrypt_str(res_data['data'])
            if self.ec_srv.verify(decrypt_data, res_data['sign']):
                return decrypt_data
            else:
                return self.ec_srv.error
        else:
            return res_js

    def action(self, data, api):
        data_str = json.dumps(data, ensure_ascii=False)
        sign = self.ec_cli.sign_str(data_str)
        encrypt = self.ec_srv.encrypt_str(data_str)
        res = self.request(self.request_json(api, sign, encrypt))
        result = self.check_rt(res)
        return result

    def ck_domain(self, doamin):
        ns = []
        ns_re = '(' + '|'.join(ns) + ')$'
        ns_re = ns_re.replace(".", "\.")
        if not re.match(ns_re, doamin, re.I):
            print("No Match")
        else:
            print("Match")

    def bk_create(self):
        data = {
<<<<<<< Updated upstream
            "appid": "app_test_3",
=======
            "appid": "app_test_11",
>>>>>>> Stashed changes
            "desc": "创建测试用例3",
            "create_cli_keys": True,
            "create_srv_keys": True,
            "cli_keys_length": 2048,
            "srv_keys_length": 4096,
            "r_cli_publickey": False,
            "r_srv_privatekey": False,
            "cli_keys": {
                 "cli_publickey": "",
                 "cli_privatekey": ""
            },
            "srv_keys": {
                 "srv_publickey": "",
                 "srv_privatekey": ""
            },
<<<<<<< Updated upstream
            "ip": ["192.168.1.0/255.255.255.0", "192.168.1.2", "127.0.0.1", '192.168.1.77'],
            "ns": ["localhost", "127.0.0.1", "192.168.1.77"],
=======
            "ip": ["192.168.1.1", "192.168.1.2", "127.0.0.1", 'localhost', '192.168.1.7'],
            "ns": ["localhost", "127.0.0.1", "192.168.1.7"],
>>>>>>> Stashed changes
            "srv": [],
            "status": 0,
            "time": time.time()
        }
        result = self.action(data, 'bk_create')
        print("bk_create <=>", result)

    def bk_remove(self):
        data = {
            "appid": "app_test_9",
            "time": int(time.time())
        }
        result = self.action(data, 'bk_remove')
        print("bk_remove <=>", result)

    def bk_edit(self):
        data = {
            "appid": "app_test_8",
            "ns": ["全部更新，不接受增量更新", "ns2"],
            "ip": ["全部更新，不接受增量更新", "ip2"],
            "srv": ["全部更新，不接受增量更新", "srv2"],
            "cli_publickey": self.ec_cli.get_publickey(),
            "cli_privatekey": self.ec_cli.get_privatekey(),
            "srv_publickey": self.ec_srv.get_publickey(),
            "srv_privatekey": self.ec_srv.get_privatekey(),
            "status": 100,
            "lelsie": True,
            "time": time.time()
        }
        result = self.action(data, 'bk_edit')
        print("bk_edit <=>", result)

    def bk_info(self):
        data = {
            "appid": "app_test_8",
            "field": ["ip", "ns", "srv", "cli_publickey", "cli_privatekey", "srv_publickey", "srv_privatekey"],
            "time": time.time()
        }
        result = self.action(data, 'bk_info')
        print("bk_info <=>", result)

    def bk_status(self):
        data = {
            "appids": ["app_test_8", "app_test_7"],
            "time": time.time()
        }
        result = self.action(data, 'bk_status')
        print("bk_status <=>", result)

    def bk_cleanup(self):
        data = {
            "appid": "canigreen",
            "time": int(time.time())
        }
        result = self.action(data, 'bk_cleanup')
        print("bk_cleanup <=>", result)


if __name__ == "__main__":
    dd = DianDian()
    # dd.bk_remove()
    # dd.bk_create()
    # dd.bk_edit()
    # dd.bk_info()
    # dd.bk_status()
    dd.bk_cleanup()







