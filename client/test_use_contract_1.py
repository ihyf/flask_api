# coding:utf-8
import requests
import json
import time
s = "hyf"
from util.check_fuc import to_byte32
# s = to_byte32("hyf")
keystore0 = {'address': 'bb77bbdfe61713495fe3041b9783c51a07adae8a', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '70355b45fdc19eba96767c8fa8ddcb8f'}, 'ciphertext': '21a52f50e8e97091d32e7beaea2c34c095f2e009c35cb250a30fa419d46ef8d8', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e8af32b28379a095145eb612016959a4'}, 'mac': '8d27821345a59a80f8509b6d4e215ce526e5b2e29edd25fcd34200c28f8c9420'}, 'id': '9b05b11a-7e5b-4b26-9b90-694e3069fe18', 'version': 3}
keystore1 = {'address': '2f22eff53d62ad4b1433de288c3abcc3021668f1', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'fe5df6ff428eac4654ca89638b5ed0e6'}, 'ciphertext': '4abafd68c712cd0e499b16e0c78d99d35b910e3c20f73241375d85c34e0db5f1', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'd595870f58d2cd67e3e86c9c4b54f839'}, 'mac': '01261f6ffce5864c0bd3d00f63a6ffb0d8a63d89b90a0c7307b6d233cc40e386'}, 'id': 'ff0e9448-2b0c-487c-8b68-448ba3798a7b', 'version': 3}
keystore2 = {'address': '9f931061882ff40c3d91d64bcccd3b1a9660430f', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'acefbd989bcbbb327f88c9894b2bc0fa'}, 'ciphertext': '7ba2e7c90c47552d4f2affb15ae247c7c232aff11edbc692c93deeb0b3826fba', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'fd52833b8d9341504c05a85fd450cf84'}, 'mac': '093b55177c9a95d0d0cde9d5dfd0a381ecb9e590198e249401461e4566579405'}, 'id': '0a6a897d-f6cf-4055-ba50-74954fd542ab', 'version': 3}
keystore3 = {'address': '2119f46f94bffdcdee2d0c8a0101c2dd269dcbd1', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '9407d970ddbabf77bfc7a91f75df9b09'}, 'ciphertext': '5c34f01af34dd1fa40ea1675aaeae8b1b182227946c97c4d91eeb8f53963eca3', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e27d678e4e43c240d57927aec6d1528f'}, 'mac': '5add4d78783e6ba62e0b14d5c9b5d2045104b30daea7ba5cbbf06713035ac46f'}, 'id': 'a0f2e01d-0258-42db-9f9d-8fd962814c50', 'version': 3}
keystore4 = {'address': '3cd1dd1000638e383bae1dba304ad1ba097705f5', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '39960af370d477090bf41b2fa77933be'}, 'ciphertext': 'bd10d042efc3891bf0bd3a3d448822315b4503f2fdab078dd9bb48bf9f6a6c1d', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'e99a1ab005e5259e147bfa41e9153a64'}, 'mac': '936497966c057a0f5837891531e21dcc4ce8d2a4e47fbc2af90c3a196afb627e'}, 'id': '672198aa-5f9e-49fc-9fcd-fd7b02c271c5', 'version': 3}
pwd = "hyf"
"""
Ganache CLI v6.1.8 (ganache-core: 2.2.1)

Available Accounts
==================
(0) 0xbb77bbdfe61713495fe3041b9783c51a07adae8a (~100 ETH)
(1) 0x2f22eff53d62ad4b1433de288c3abcc3021668f1 (~100 ETH)
(2) 0x9f931061882ff40c3d91d64bcccd3b1a9660430f (~100 ETH)
(3) 0x2119f46f94bffdcdee2d0c8a0101c2dd269dcbd1 (~100 ETH)
(4) 0x3cd1dd1000638e383bae1dba304ad1ba097705f5 (~100 ETH)
(5) 0xa631638e0d850996cdf8a8bcaf0e2091f3bd9d16 (~100 ETH)
(6) 0xf8fbc02d79a8a5ff9bafd0c1c2719fabb757e06e (~100 ETH)
(7) 0xdfd56f1cd49e8aeff17634e2e9fef75d6916c1dd (~100 ETH)
(8) 0x011819db348efdab77b228cdeb0770ae3336986f (~100 ETH)
(9) 0x7062a84c78bea5699fe6794f1c79f91bb5e594b5 (~100 ETH)

Private Keys
==================
(0) 0xf72292fd8e2be54f8b824caf8b5dc1a0f9846d9dce3be6a6b8819c47d811fc4a
(1) 0x9e6a7f700558e30ec4310e6732a75320b6fdf6d678cdf27a7065892152a18e76
(2) 0xdc8ca76dfc3dd75b01c9b32842f6d580a9aee3a883b6e6c59703b3d83380ab96
(3) 0xb72a7d894ef1da6fbff3b88e6789f75bbba09cd121c8142a1d823512c4c5620c
(4) 0xec007767eb7302486b1ebe42a489a5e4fc90d31e65bc1974722de86f36d3bd9d
(5) 0xc25bacacff6f3193e691126c850edda9c89982d0d22edba2dca12b7df34a1009
(6) 0x40b1ddf6843ea8928d4f2fe32b3c6ffda287cac9919ef2bbf18f65170e4ac879
(7) 0xd82b9f5eea522bbe9dcc9647059d07b105c0775eb08f2c015bbe285538271efd
(8) 0xbbb738a50105f4d52764c2c6bfda6a2ef76661926ec0f3b3a9a163c27e60aae1
(9) 0xa4c3659890d002ec8ba682188be6d68fd053785e3a655844d03cd52070bd61a5

HD Wallet
==================
Mnemonic:      supply neglect swarm aware voice run actor arena hurry taste demand mystery
Base HD Path:  m/44'/60'/0'/0/{account_index}

Gas Price
==================
20000000000

Gas Limit
==================
6721975

Listening on 127.0.0.1:8545



"""
"0xd87f9a8fe5e66cf3e1e06d8f6c4774fba4da372731dd2828186fe06aa373669f"
a1 = "0x2f22eff53d62ad4b1433de288c3abcc3021668f1"
a2 = "0x9f931061882ff40c3d91d64bcccd3b1a9660430f"
a3 = "0x2119f46f94bffdcdee2d0c8a0101c2dd269dcbd1"
a4 = "0x3cd1dd1000638e383bae1dba304ad1ba097705f5"

a0 = "0xbb77bbdfe61713495fe3041b9783c51a07adae8a"
"betting" "getRandom" "result"
url_waiwang = "http://47.52.166.23:9000/api"
"transfer_contract" "getNumPlayerArr"  "setChooseGame" "tBetting" "tResult" "getGameNum"

k = {"address":"7da035166ec65a73224867c9721179024d54406c","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"88ff7fa6e73a57b819231627ff58ef2e"},"ciphertext":"aa93a6e0d0e6093a44185579137d3436ff5ed2075412839bbccd589ee2860469","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"1eca57161df5ad13d51b2d28b4a8b6af"},"mac":"5ad3460a7de09ffb7df3253f432001c02f62921c4ead93a7d85199617ec1145b"},"id":"303725d9-9926-43fd-b6dd-547aa594b386","version":3}
k_0 = {'address': 'cddd1a4d1c811e9ef5fa392266de98022107583f', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '64515c130f765d2d745e23cd43214c8e'}, 'ciphertext': 'f8f6869612819db27a8109e344c849cee048033e131ddb347f00177eb7736d08', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'f12b533c4d005381ed67b09b49f1ef55'}, 'mac': '1141f601fb125dafff5d3a1fba63b197cad94e95a266cebbedcccde0f2b0327d'},  'version': 3}
k_0_bak = {'address': 'cddd1a4d1c811e9ef5fa392266de98022107583f', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '64515c130f765d2d745e23cd43214c8e'}, 'ciphertext': 'f8f6869612819db27a8109e344c849cee048033e131ddb347f00177eb7736d08', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'f12b533c4d005381ed67b09b49f1ef55'}, 'mac': '1141f601fb125dafff5d3a1fba63b197cad94e95a266cebbedcccde0f2b0327d'}, 'id': '9a173bb2-8427-4a4b-a8e6-6023dd361e43', 'version': 3}
payload = {
        "method": "transfer_contract",
        "params": {
            "appid": "dfe5f60fa172245e5e285f20bbc2509d",
            "sign": "",
            "data": {
                "func_name": "setRefund",
                "func_param": "0x6a98047F56BE2F599B56805F02FDad6b387C74C9",
                "value": "0",
                "keystore": k_0,
                "pwd": "hyf",
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": 11
    }
from cert.eth_certs import EthCert

ec = EthCert("dfe5f60fa172245e5e285f20bbc2509d_cli")
ec.load_key_from_file()
ec.serialization()
sign = ec.sign(payload["params"]["data"])
print(sign)
payload["params"]["sign"] = sign.decode()

ec1 = EthCert("dfe5f60fa172245e5e285f20bbc2509d_srv")
ec1.load_key_from_file()
ec1.serialization()
payload["params"]["data"] = ec1.encrypt(payload["params"]["data"]).decode()


url = "http://192.168.1.14:9000/api"
url1 = "http://127.0.0.1:3000/api"
headers = {"content-type": "application/json"}
response = requests.post(
            url_waiwang, data=json.dumps(payload), headers=headers).json()
print(response)
ddata = ec.decrypt(response["result"]["data"])
print(ddata)





