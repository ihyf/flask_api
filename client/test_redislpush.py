from util.db_redis import redis_store


import requests
import json
import time
from cert.eth_certs import EthCert
from urllib import parse


url = "http://localhost:9000/api"
url11 = "http://192.168.1.14:9000/api"
headers = {"content-type": "application/json"}


payload = {
        "method": "test_redis",
        "jsonrpc": "2.0",
        "id": "0",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "op_id": "30",
                "time": time.time()
            }
        }
}


# ec = EthCert("hyf_app")
# ec.load_key_from_file()
# ec.serialization()
# sign = ec.sign(payload["params"]["data"])
# payload["params"]["sign"] = sign.decode()
#
# ec1 = EthCert("hyf_srv")
# ec1.load_key_from_file()
# ec1.serialization()
# payload["params"]["data"] = ec1.encrypt(payload["params"]["data"]).decode()

for i in range(1):
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

print(response)
# ddata = ec.decrypt(response["result"]["data"])
# print(ddata)
