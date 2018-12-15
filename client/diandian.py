import requests
import json
import time
from cert.eth_certs import EthCert


def leslie():
    ec_cli = EthCert("diandian_cli")
    ec_cli.load_key_from_file()
    ec_cli.serialization()
    ec_srv = EthCert("diandian_srv")
    ec_srv.load_key_from_file()
    ec_srv.serialization()
    data = {
        "appid": "app_test_9",
        "desc": "创建测试用例3",
        "create_cli_keys": False,
        "create_srv_keys": False,
        "cli_keys_length": 1024,
        "srv_keys_length": 4096,
        "r_cli_publickey": False,
        "r_srv_privatekey": False,
        "cli_keys": {
             "cli_publickey": ec_cli.get_publickey(),
             "cli_privatekey": ""
        },
        "srv_keys": {
             "srv_publickey": "",
             "srv_privatekey": ec_srv.get_privatekey()
        },
        "ip": ["192.168.1.1", "192.168.1.2", "127.0.0.1", 'localhost', '192.168.1.77'],
        "ns": ["localhost", "127.0.0.1", "192.168.1.77"],
        "srv": [],
        "status": 0,
        "time": int(time.time())
    }
    data_str = json.dumps(data, ensure_ascii=False)
    # print(data_str)
    sign = ec_cli.sign_str(data_str)
    encrypt = ec_srv.encrypt_str(data_str)
    post_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "bk_create",
        "params": {
            "appid": "diandian",
            "sign": sign,
            "data": encrypt
        }
    }
    headers = {
        'content-type': "application/json",
        'Authorization': 'PyCharm Test'
    }
    response = requests.post("http://127.0.0.1:3000/api", data=json.dumps(post_data), headers=headers)
    res_js = json.loads(response.text)
    res_data = res_js['result']
    if res_data['code'] == "success":
        decrypt_data = ec_cli.decrypt_str(res_data['data'])
        verify = ec_srv.verify(decrypt_data, res_data['sign'])
        print(verify)
        print(decrypt_data)
    else:
        print(res_js)


if __name__ == "__main__":
    leslie()
