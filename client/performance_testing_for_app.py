# coding:utf-8
import asyncio
import time
import aiohttp
import json
from cert.eth_certs import EthCert
import random
import hashlib


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
        # print(response)
        ddata = self.ec_cli.decrypt(response["result"]["data"])
        # print(ddata)
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
    
    async def test_send_transaction(self):
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
    
    async def my_method(self):
        method = "my_method"
        data = {
            "time": time.time()
        }
        await self.send_request(url=self.url_neiwang, method=method, data=data)


if __name__ == "__main__":
    t = Testing()
    
    # asyncio.ensure_future(slow_task(future))
    # future.add_done_callback(got_result)
    asyncio.ensure_future(t.test_create_account())
    tasks = [asyncio.ensure_future(t.test_get_balance()) for i in range(1)]
    t1 = time.time()
    loop.run_until_complete(asyncio.gather(*tasks))
    t2 = time.time()-t1
    print(t2)
    loop.close()

