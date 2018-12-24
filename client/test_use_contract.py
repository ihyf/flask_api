# coding:utf-8
import requests
import json
import time
s = "hyf"
from util.check_fuc import to_byte32
# s = to_byte32("hyf")
"""
Available Accounts
==================
(0) 0xaad3d1d86f19b85db4dc8f8cd8edfdcd1884e4dc (~100 ETH)
(1) 0x36bfff2e76b644ef5a94359a81379bee386db371 (~100 ETH)
(2) 0xa318706e0a9159feddcbfbb0a29bbef56a8072a5 (~100 ETH)
(3) 0x9eb9ed62affe924a19c442a198487c721b1b89f4 (~100 ETH)
(4) 0x265dbf9c8131c7d2b25d1636201022b015d75470 (~100 ETH)
(5) 0x8d59378abdb21db7ee21b5a4dd61c858bd26da3f (~100 ETH)
(6) 0x67e76cf882ac4ff4814436236051f2940ff7f36f (~100 ETH)
(7) 0x3633e8d8eda4bf201a253788d6d1f202e2ad5d64 (~100 ETH)
(8) 0xc2cefef5fccbbb7db1391c4fea8d258a0be8984f (~100 ETH)
(9) 0xff21dc61409bd871f44335f91a513295f4cf622b (~100 ETH)

Private Keys
==================
(0) 0xfc3ac2425fa869e83a12cd4f4e2ff0f66cefedf29f671aca05c4fc274080b304
(1) 0xcb5ffe219e6b4e711e7b61f9f3ac758491290b8309d0fdb035fa0a45fef1856b
(2) 0xc8f715a87b37c3593240875d7de7e583b0c12234a83f9b51a7304d8acc08c9cd
(3) 0xf6e8dd4eedfb1302bd52dbb5a324cfc0d0e694d08fa3b011aa29f4b0207a6395
(4) 0xe43370b8fa3136944e03139b9cdff2a969cb578fbfa66f3d2ea6c336ae26d2b2
(5) 0x06bb9c6efd1dc0fbef2011a5af2e8f499a3506717de530360838ae7afda3a37e
(6) 0x70262f5b2705340f7da7be3e235298588fd988442641adb5bcaf0365a1ba84ea
(7) 0x62ad047d758d9cb0fe119c7a3e1ad6c490b953f2ce8f5252341b56d338ab1f4d
(8) 0x985680eed1437faccceea8a3563cb0e6b634aa5b826c251dc436af267618059f
(9) 0x6d713b98261495404b53f4a17b137a58b1ae3e38d042ee3ce12a2b8afa09b0ba

"""
"0xd87f9a8fe5e66cf3e1e06d8f6c4774fba4da372731dd2828186fe06aa373669f"
a0 = "0xaad3d1d86f19b85db4dc8f8cd8edfdcd1884e4dc"
a2 = "0xa318706e0a9159feddcbfbb0a29bbef56a8072a5"
a3 = "0x9eb9ed62affe924a19c442a198487c721b1b89f4"
a4 = "0x265dbf9c8131c7d2b25d1636201022b015d75470"


a1 = "0x36bfff2e76b644ef5a94359a81379bee386db371"
"betting" "getRandom" "result"

"transfer_contract" "getNumPlayerArr"  "setChooseGame" "tBetting" "tResult" "getGameNum"
payload = {
        "method": "transfer_contract",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "account": a1,
                "contract_name": "luckyNumber",
                "func_name": "getGameNum",
                "func_param": "",
                "value": 0,
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


url = "http://192.168.1.14:9000/api"
url1 = "http://127.0.0.1:3000/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
print(response)
ddata = ec.decrypt(response["result"]["data"])
print(ddata)





