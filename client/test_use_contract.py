# coding:utf-8
import requests
import json
import time
from util.compile_solidity_utils import w3
s = "hyf"
from util.check_fuc import to_byte32
# s = to_byte32("hyf")
"play_contract1"
"play_contract2"
"get_num"
"0xd87f9a8fe5e66cf3e1e06d8f6c4774fba4da372731dd2828186fe06aa373669f"
a0 = "0xfb4a28a561fc3a665020d54a55223eb6c3649314"
a2 = "0x4d2ec296b09f2ca018dfac9c192f3d89881a0865"

a1 = "0x32b4e7246f86ee49a9f82d060cc52b23160f5952"
"betting" "getRandom" "result"

"transfer_contract" "getNumPlayerArr"  "setChooseGame" "tBetting" "tResult"
payload = {
        "method": "transfer_contract",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "account": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "contract_name": "luckyNumber",
                "func_name": "getbonusMoney",
                "func_param": "",
                "value": 2,
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": 11
    }
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


url1 = "http://192.168.1.14:8080/api"
url = "http://127.0.0.1:3000/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)
ddata = ec.decrypt(response["result"]["data"])
print(ddata)





