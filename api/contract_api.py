# coding:utf-8
import json
import os
import logging
import time
from flask import request
from cert.eth_checkout import check_conn
from my_dispatcher import api_add, api
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv


@api_add
@check_conn(request)
def transfer_contract(*args, **kwargs):
    # 调用合约公共接口
    data = kwargs['decrypt']
    necessary_keys = ["account", "contract_name", "func_name"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        account = data.get("account", None)
        contract_name = data.get("contract_name", None)
        func_name = data.get("func_name", None)
        func_param = data.get("func_param", None)
        value = data.get("value", None)
        
        with open("json_files/data_{}.json".format(contract_name), 'r') as f:
            datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]
        contract_name = w3.eth.contract(address=contract_address, abi=abi)
        account = w3.toChecksumAddress(account)
        
        if "get" not in func_name and "set" not in func_name:
            tx_hash = eval("contract_name.functions.{func_name}({func_param})."
                           "transact({{'from': '{account}', 'value': w3.toWei({value}, 'ether')}})".
                           format(contract_name=contract_name, func_name=func_name,
                                  func_param=func_param, account=account, value=value))
            w3.eth.waitForTransactionReceipt(tx_hash)
            # 插入数据库 预留
            
            result = {"data": "{} ok".format(func_name)}
            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()
            
            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
        elif "set" in func_name:
            tx_hash = eval("contract_name.functions.{func_name}({func_param})."
                           "transact({{'from': '{account}', 'value': w3.toWei(0, 'ether')}})".
                           format(contract_name=contract_name, func_name=func_name,
                                  func_param=func_param, account=account))
            w3.eth.waitForTransactionReceipt(tx_hash)

            # 插入数据库 预留
            result = {"data": "set {} ok".format(func_name)}
            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()

            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
        elif "get" in func_name:
            result = eval("contract_name.functions.{func_name}({func_param}).call()".
                          format(contract_name=contract_name, func_name=func_name, func_param=func_param))

            # 插入数据库 预留
            
            result = {"data": result}
            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()

            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
    else:
        return {"code": "fail", "error": check}
    
    
@api_add
def generate_contrants_md(*args, **kwargs):
    with open("client/contracts_func.md", "w", encoding="utf-8") as cf:
        for root, dirs, files, in os.walk("json_files", topdown=False):
            for f_name in files:
                file = root + "/" + f_name
                with open(file, "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
                    abi = data.get("abi", None)
                    contract_address = data.get("contract_address", None)
                f_name = f_name.split(".")[0].split("_")[1]
                cf.write("# 合约名: " + f_name + "\n")
                cf.write("\n")
                for t in abi:
                    if t["type"] == "function":
                        s_func = t["name"]
                        s_input = [it for it in t["inputs"]]
                        s_input1 = [it['name'] for it in t["inputs"]]
                        s_func = s_func + "(" + ','.join(s_input1) + ")"
                        s_return = t["outputs"]
                        cf.write("## " + s_func + "\n")
                        if s_input:
                            cf.write("参数类型:" + "\n")
                            cf.write("\n")
                            for i in s_input:
                                cf.write(i['name'] + "--->" + i['type'] + "\n")
                                cf.write("\n")
                        
                        if s_return:
                            cf.write("返回值:" + "\n")
                            cf.write("\n")
                            for i in s_return:
                                cf.write(i['type'] + "\n")
                        
                        else:
                            cf.write("返回值: 无" + "\n")
        return {"data": "ok"}

