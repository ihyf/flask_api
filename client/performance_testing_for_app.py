# coding:utf-8
import asyncio
import time
import aiohttp
import json
from cert.eth_certs import EthCert
import random
import hashlib
k_poa_node1 = {"address":"3ff83cc121adae7953cc96c8fab1463c2756d4d6","crypto":{"cipher":"aes-128-ctr","ciphertext":"9159d08b6b72b26cb9aa0eb22776ad73f12444d1c333f1b77a6350497fbcf486","cipherparams":{"iv":"d073e228b007782f029f2f229c585ddc"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"5e1146850019085d042a7b660d6f6e99266e35d797a5e55d7402c263f4b96c9f"},"mac":"4301617ced915e9a22b5f93b937d8a61f4113a34615feb681cdb0f8a8db87b51"},"id":"e82ce4db-c07a-4959-8c8c-a0e17fd0d6ab","version":3}
k_person1 = {"address":"01533b8693bb6a8062542cbee7239fc40089b9ae","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"49f794c57e9d31ba67739e244e6bcf95"},"ciphertext":"c2672c4cd1ff2f4e7ed35a71e6693e041b0c66136837f42cd7054e3407602423","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"5018596f7f336ec301b88b159c17ee74"},"mac":"240f59662dcc94dbeb60a22dff593cff810ada8e52552873992f0e701190c568"},"id":"19e3faa3-c4fd-46b5-85d0-6ffb09984ffe","version":3}
k_person2 = {"address":"0dad229c539b2d62123f50dd1c8a51d5c6a92358","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"d2eebe2ba9983cb945c47d69b817ef8b"},"ciphertext":"36ec243893c40dc8ff6f4b4de9c4356b732c57873c32d1f82f5491526c318600","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"2af25477b71c65b89adbd41a2ee4008d"},"mac":"2338ba73c6e3f4071f85f3bf5809a8a3723ef623108483a80e7accc017c81e66"},"id":"7213cbdc-cc20-49db-87b1-f07a12aca3cb","version":3}
k_person3 = {"address":"d3321fb522fb5114eb398be2a53f1017a95d2c4b","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"d634969fe11ce67a7d17b8cb80f0e2fa"},"ciphertext":"6cb2f9ca1032b222592705a873e1fcab07be0cb9e32a48f4b0084feabcf5b66c","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"ada04082526be4dc0b73a903497220c6"},"mac":"1a966a4ee827b012fbfa00af07182ed62ba1ce2086a594e151e89053f4b1d03f"},"id":"57e21073-3033-4afa-95dc-e65209d5bb14","version":3}
to_address_list = ["0x01533b8693bb6a8062542cbee7239fc40089b9ae", "0x0dad229c539b2d62123f50dd1c8a51d5c6a92358", "0xd3321fb522fb5114eb398be2a53f1017a95d2c4b"]


sema = asyncio.Semaphore(1)
loop = asyncio.get_event_loop()
future = asyncio.Future()


class Testing(object):
    """性能测试"""
    def __init__(self):
        self.appid = "hyf_app"
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
        self.ec_cli = EthCert("hyf_app")
        self.ec_srv = EthCert("hyf_srv")
        self.ec_cli.load_key_from_file()
        self.ec_cli.serialization()
        self.ec_srv.load_key_from_file()
        self.ec_srv.serialization()
        self.url_waiwang = "http://47.52.166.23:9000/api"
        self.url_neiwang = "http://192.168.1.14:9000/api"
        self.url_local = "http://localhost:9000/api"
        self.sha1 = hashlib.sha1()
    
    async def send_request(self, url, method, data):
        self.payload["method"] = method
        self.payload["params"]["sign"] = self.ec_cli.sign_str(data)
        self.payload["params"]["data"] = self.ec_srv.encrypt_str(data)
        with (await sema):
            async with aiohttp.request('POST', url=url, data=json.dumps(self.payload), headers=self.headers) as r:
                response = await r.json()
        # if isinstance(response, bytes):
        #     response = response.decode()
        # else:
        #     response = response.json()
        print(response)
        ddata = self.ec_cli.decrypt(response["result"]["data"])
        print(ddata)
        # print(self.ec_srv.verify(ddata, response["result"]["sign"]))
    
    async def test_create_account(self):
        method = "create_account"
        data = {
            "pwd": "hyf",
            "time": time.time()
        }
        await self.send_request(url=self.url_neiwang, method=method, data=data)
    
    async def test_get_balance(self):
        method = "get_balance"
        data = {
            "address": [
                "0x3ff83cc121adae7953cc96c8fab1463c2756d4d6",
                "0x3ff83cc121adae7953cc96c8fab1463c2756d4d6"
            ],
            "request_type": 2,
            "time": time.time()
        }
        await self.send_request(url=self.url_neiwang, method=method, data=data)
    
    async def test_send_transaction(self, to_address):
        method = "send_transaction"
        data = {
            "to_address": to_address,
            "value": 101,
            "gas_limit": 21000,
            "gas_price": 100,
            "pwd": "123456",
            "keystore": k_poa_node1,
            "time": time.time()
        }
        await self.send_request(url=self.url_local, method=method, data=data)
    
    async def test_use_contract(self):
        method = "transfer_contract"
        data = {
            "func_name": "getPlay",
            "func_param": "0xa4c013179c761a284197f8b4be18a74525650062",
            "value": "0",
            "keystore": to_100_keystore,
            "pwd": "hyf",
            "time": time.time()
        }
        await self.send_request(url=self.url_waiwang, method=method, data=data)
    
    async def test_add_master_contract(self):
        method = "add_master_contract"
        data = {
            "master_contract_name": "hyf_master_20190222_1825",
            "time": time.time()
        }
        await self.send_request(url=self.url_neiwang, method=method, data=data)
    
    async def test_deploy_contract(self):
        method = "deploy_contract"
        self.sha1.update(random.uniform(-10000, 20000))
        data = {
            "contract_name": "luckyNumber_0222_1825",
            "url": "123",
            "master_contract_name": "hyf_master_20190222_1825",
            "master_contract_address": "0x475CBDA0d1C7c922a6883eC2BEE7387f44F2C594",
            "time": self.sha1.hexdigest()
        }
        print(data["time"])
        await self.send_request(url=self.url_local, method=method, data=data)
    

if __name__ == "__main__":
    t = Testing()
    
    # asyncio.ensure_future(slow_task(future))
    # future.add_done_callback(got_result)
    tasks = [asyncio.ensure_future(t.test_create_account())]
    t1 = time.time()
    loop.run_until_complete(asyncio.gather(*tasks))
    t2 = time.time()-t1
    print(t2)
    loop.close()

