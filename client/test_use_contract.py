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
a1 = "0x749cf919d06eedaf10262f75f04aa61839706ad3"
a2 = "0xb7e8bce0c5343df3339705eabfe9d74681080ab9"
a3 = "0x321743c06e0706f08807c63dc5704e3b81068589"
a4 = "0x41f1dbfaade159590aa1a557e80e55c760c758c4"

a0 = "0x274bfd5a0bde79655139b6f1876a5e93613cb3b0"
"betting" "getRandom" "result"
k0 ={'address': '274bfd5a0bde79655139b6f1876a5e93613cb3b0', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'df903ff8132106d97976d9b959de5e2f'}, 'ciphertext': '58fb03cf68f95b61d3cda1bfc5db10ad653cac66cf518b670b87d08ae25d1cb7', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'aa32da67afe61151054996ad29d5ba44'}, 'mac': '6b8ab5d768f734a36d1a664c1e46f0708892966836fb2034b498f674c3c9586d'}, 'id': 'b7cda100-a7fd-4478-ba70-c640ba7e1fbb', 'version': 3}
k1 = {'address': '749cf919d06eedaf10262f75f04aa61839706ad3', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '7f72679d0861a7b67e42d6acc4915de3'}, 'ciphertext': 'db55e075dc3fc7d559e7b81d901187ef8be29681bf4b408c4b3222b69ba7d087', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': 'ef3612453c68a7ad6fc467a55cd9421d'}, 'mac': '895c617aa1d437c9da2032c0e3fa63922cb836366b4dd025b5b6bceb35144700'}, 'id': 'e04eb32c-c4f9-4fb1-bfb7-f98de573eca9', 'version': 3}
k2 = {'address': 'b7e8bce0c5343df3339705eabfe9d74681080ab9', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'dba976c0b25b431bb69ac85b9c4bd2ed'}, 'ciphertext': 'efa46bef8196d792e9eba8d13b6147063adf078063ac560288949f4fe46d164d', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '033748b5fab51e726bc588908ec58258'}, 'mac': '3a9c8d155978b899c85eb267db30147cf059274a094af4d2c5009ec502396d44'}, 'id': 'a7c5d7e6-1fd4-425b-930c-6fd83ab933bd', 'version': 3}
k3 = {'address': '321743c06e0706f08807c63dc5704e3b81068589', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '64021eb91132cd3a8787c5ea1cc4357f'}, 'ciphertext': '8f1e81821234e255a3a7b47bfd150eee674f371cf7e31f1648b99f3f4b2e5116', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '9daf44e20910daae997870e2d8f55210'}, 'mac': '5cea94db65aff83b101aa30d4e2d5bb7dcc0e2db7eb676f0ea3980cd09369de4'}, 'id': '805c1ad1-3e89-4b7e-87f8-c77dd3ec7920', 'version': 3}
k4 = {'address': '41f1dbfaade159590aa1a557e80e55c760c758c4', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '23c9e0e1de117f5475643c0b65da6db4'}, 'ciphertext': 'ca4ff169b8101b66d65a9deb65ad4be2bf47be968816e3d000575194f94f134c', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '7e9a929fa864893429f38c958109cfdc'}, 'mac': 'be19395d1ce81d772bd03b4dfb7d94a708642195ca5a651abd0bd3bef2d5f29c'}, 'id': 'c85de2a6-5915-4be7-8eea-9597f1b98c21', 'version': 3}
k_add = {"address":"974ee15eac43df137f0c7903738000ca50a79a76","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"08edd58428a266bb7246433d4ed44211"},"ciphertext":"c70a4e922d5f782598e9308454b1fa9908bc2fd0554f01b88c143e18f268a309","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"7a8ba1af237313958be4389a67a29e8a"},"mac":"1bec281a4893407367fdb409803750768c10621017110f47e77f686a70894329"},"id":"04afa9ec-f13f-42e5-a242-17ee251d5d25","version":3}
k_add2 = {"address":"a51a9527f3398e2247e6c4aaa16ed71783d755ff","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"d0f81586c82370e545b7c7a8db444dba"},"ciphertext":"b648d320febac018e6e533573c5a3699e1290320229c08418846897120c3436a","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"6746a8c25910dcc0f1127c86b7971150"},"mac":"ad4afd82ac65bcb35064095720ac30e36f3beb4692fcd14aeb3e8aa212d81469"},"id":"bedbf8f4-153a-4a4b-a488-27aaa643535b","version":3}
k_hyf = {"address":"a53683641b86640e539f5224e3a062b10fe8c830","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"0be3e7461ab510e0a4a56bd3c55ba785"},"ciphertext":"94bd89d02f3bfee46e6634c15cba5ad2d4449daf03bd811780069cda880b5181","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"6446f4ef06f1c58794fc8aae631950b3"},"mac":"375e14236a14df9507ad0737a7b037b7e18051a2899edd6ee7092afc6af28eee"},"id":"6d8f91a9-f18d-4377-b590-49befcd8eb04","version":3}
keystore_poa_node1 = {"address":"3ff83cc121adae7953cc96c8fab1463c2756d4d6","crypto":{"cipher":"aes-128-ctr","ciphertext":"9159d08b6b72b26cb9aa0eb22776ad73f12444d1c333f1b77a6350497fbcf486","cipherparams":{"iv":"d073e228b007782f029f2f229c585ddc"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"5e1146850019085d042a7b660d6f6e99266e35d797a5e55d7402c263f4b96c9f"},"mac":"4301617ced915e9a22b5f93b937d8a61f4113a34615feb681cdb0f8a8db87b51"},"id":"e82ce4db-c07a-4959-8c8c-a0e17fd0d6ab","version":3}
url_waiwang = "http://47.52.166.23:9000/api"
"transfer_contract" "getNumPlayerArr"  "setChooseGame" "tBetting" "tResult" "getGameNum"


k_pingtai = {'address': 'a107a8cef11aee3b2e24f59b5e8218c559ba2b72', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': 'ae48d496c8e471193d3b0a1c9ba43998'}, 'ciphertext': '94c1e2e863e04c18ae5828000787d63c276c3e3342a10a0b0754f23c0d1552bb', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '7cbba41298cba5cb81b6752155ffcaa6'}, 'mac': 'b945f5241a32d66132f1332963acdbc400247da0ec688cea8493a08ae3ad12c5'}, 'id': '9a1a7b53-2f25-4bde-966c-f1735d379109', 'version': 3}
payload = {
        "method": "transfer_contract",
        "params": {
            "appid": "c951311c68e15b0918470031d80829ec",
            "sign": "",
            "data": {
                "func_name": "tSaveMoney",
                "func_param": "",
                "value": "900000000",
                "keystore": k_pingtai,
                "pwd": "hyf",
                "time": time.time()
            }
        },
        "jsonrpc": "2.0",
        "id": 11
    }
from cert.eth_certs import EthCert

ec = EthCert("c951311c68e15b0918470031d80829ec_cli")
ec.load_key_from_file()
ec.serialization()
sign = ec.sign(payload["params"]["data"])
payload["params"]["sign"] = sign.decode()

ec1 = EthCert("c951311c68e15b0918470031d80829ec_srv")
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





