import requests
import json
import time
from cert.eth_certs import EthCert
from urllib import parse
keystore0 = {'address': 'bb77bbdfe61713495fe3041b9783c51a07adae8a', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '70355b45fdc19eba96767c8fa8ddcb8f'}, 'ciphertext': '21a52f50e8e97091d32e7beaea2c34c095f2e009c35cb250a30fa419d46ef8d8', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e8af32b28379a095145eb612016959a4'}, 'mac': '8d27821345a59a80f8509b6d4e215ce526e5b2e29edd25fcd34200c28f8c9420'}, 'id': '9b05b11a-7e5b-4b26-9b90-694e3069fe18', 'version': 3}
keystore1 = {'address': '2f22eff53d62ad4b1433de288c3abcc3021668f1', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'fe5df6ff428eac4654ca89638b5ed0e6'}, 'ciphertext': '4abafd68c712cd0e499b16e0c78d99d35b910e3c20f73241375d85c34e0db5f1', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'd595870f58d2cd67e3e86c9c4b54f839'}, 'mac': '01261f6ffce5864c0bd3d00f63a6ffb0d8a63d89b90a0c7307b6d233cc40e386'}, 'id': 'ff0e9448-2b0c-487c-8b68-448ba3798a7b', 'version': 3}
keystore2 = {'address': '9f931061882ff40c3d91d64bcccd3b1a9660430f', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'acefbd989bcbbb327f88c9894b2bc0fa'}, 'ciphertext': '7ba2e7c90c47552d4f2affb15ae247c7c232aff11edbc692c93deeb0b3826fba', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'fd52833b8d9341504c05a85fd450cf84'}, 'mac': '093b55177c9a95d0d0cde9d5dfd0a381ecb9e590198e249401461e4566579405'}, 'id': '0a6a897d-f6cf-4055-ba50-74954fd542ab', 'version': 3}
keystore3 = {'address': '2119f46f94bffdcdee2d0c8a0101c2dd269dcbd1', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '9407d970ddbabf77bfc7a91f75df9b09'}, 'ciphertext': '5c34f01af34dd1fa40ea1675aaeae8b1b182227946c97c4d91eeb8f53963eca3', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e27d678e4e43c240d57927aec6d1528f'}, 'mac': '5add4d78783e6ba62e0b14d5c9b5d2045104b30daea7ba5cbbf06713035ac46f'}, 'id': 'a0f2e01d-0258-42db-9f9d-8fd962814c50', 'version': 3}
keystore4 = {'address': '3cd1dd1000638e383bae1dba304ad1ba097705f5', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '39960af370d477090bf41b2fa77933be'}, 'ciphertext': 'bd10d042efc3891bf0bd3a3d448822315b4503f2fdab078dd9bb48bf9f6a6c1d', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e99a1ab005e5259e147bfa41e9153a64'}, 'mac': '936497966c057a0f5837891531e21dcc4ce8d2a4e47fbc2af90c3a196afb627e'}, 'id': '672198aa-5f9e-49fc-9fcd-fd7b02c271c5', 'version': 3}
pwd = "hyf"


a1 = "0x2f22eff53d62ad4b1433de288c3abcc3021668f1"
a2 = "0x9f931061882ff40c3d91d64bcccd3b1a9660430f"
a3 = "0x2119f46f94bffdcdee2d0c8a0101c2dd269dcbd1"
a4 = "0x3cd1dd1000638e383bae1dba304ad1ba097705f5"

a0 = "0xbb77bbdfe61713495fe3041b9783c51a07adae8a"
url = "http://localhost:9000/api"
url11 = "http://192.168.1.14:9000/api"
url_waiwang = "http://47.52.166.23:9000/api"
headers = {"content-type": "application/json"}
k_hyf = {"address":"a53683641b86640e539f5224e3a062b10fe8c830","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"0be3e7461ab510e0a4a56bd3c55ba785"},"ciphertext":"94bd89d02f3bfee46e6634c15cba5ad2d4449daf03bd811780069cda880b5181","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"6446f4ef06f1c58794fc8aae631950b3"},"mac":"375e14236a14df9507ad0737a7b037b7e18051a2899edd6ee7092afc6af28eee"},"id":"6d8f91a9-f18d-4377-b590-49befcd8eb04","version":3}

payload = {
        "method": "pay_transfer_op",
        "jsonrpc": "2.0",
        "id": "0",
        "params": {
            "appid": "hyf_app",
            "sign": "",
            "data": {
                "op_id": "69",
                "keystore": k_hyf,
                "pwd": "hyf",
                "time": time.time()
            }
        }
}


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
