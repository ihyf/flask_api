# coding:utf-8
import json
import os
import logging
import time
import requests
import config
from flask import request
from cert.eth_checkout import check_conn
from my_dispatcher import api_add, api
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv, get_srv_time
from util.compile_solidity_utils import deploy_n_transact
from util.mysql_db import db_manager, DeployContracts, ContractOp
from util.dbmanager import db_manager
from eth_account import Account
from urllib import parse


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
        keystore = data.get("keystore", None)
        pwd = data.get("pwd", None)

        with open("json_files/data_{}.json".format(contract_name), 'r') as f:
            datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)
        account = w3.toChecksumAddress(account)
        nonce = w3.eth.getTransactionCount(account)
        private_key = Account.decrypt(json.dumps(keystore), pwd)
        account_instance = Account.privateKeyToAccount(private_key)

        if "get" not in func_name and "set" not in func_name:
            ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 200000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
            t_dict = eval(ss1)
            print(t_dict)
            signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            w3.eth.waitForTransactionReceipt(tx_hash)
            
            result = {"data": "{} ok".format(func_name)}
        elif "set" in func_name:
            s = f"""contract_instance.functions.{func_name}({func_param}).transact({{'from': '{account}', 'value': w3.toWei({value}, 'ether')}})"""
            tx_hash = eval(s)
            w3.eth.waitForTransactionReceipt(tx_hash)

            result = {"data": "set {} ok".format(func_name)}

        elif "get" in func_name:
            result = eval("contract_instance.functions.{func_name}({func_param}).call()".
                          format(func_name=func_name, func_param=func_param))
            tx_hash = ""

        # 插入数据库 预留
        try:
            session = db_manager.master()
            op_info = {
                "func_name": func_name,
                "func_param": func_param,
                "value": value
            }
            # op_time = time.strftime("%Y-%m-%d %X", time.localtime())
            op_time = get_srv_time()
            if tx_hash:
                tx_hash = tx_hash.hex()
            else:
                tx_hash = "无"
            op = ContractOp(contract_name=contract_name, contract_address=contract_address,
                            op_info=op_info, op_time=op_time, tx_hash=tx_hash)
            session.add(op)
            session.commit()
            session.close()
        except Exception as e:
            return {
                "code": "fail",
                "error": f"{e}"
            }

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
                cf.write("# 合约地址: " + contract_address + "\n")
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
    

@api_add
@check_conn(request)
def deploy_contract(*args, **kwargs):
    data = kwargs.get("data", None)
    if data is None:
        return {"code": "fail", "error": "no data"}
    necessary_keys = ["contract_name", "master_contract_name", "url"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        contract_name = data.get("contract_name")
        url = data.get("url")
        url = parse.unquote(url, encoding="utf-8")
        # 获取子合约
        response = requests.get(url)
        contract_content = response.content.decode()
        with open(f"contracts/{contract_name}.sol", "w", encoding="utf-8") as f:
            f.write(contract_content)
            f.close()

        # 部署合约
        account = w3.eth.accounts[0]
        contract_address, abi = deploy_n_transact([f'contracts/{contract_name}.sol'], account=account)
        tx_hash = contract_address[1]
        tx_receipt = contract_address[2]
        pay_gas = tx_receipt.get("gasUsed", "0")
        with open(f'json_files/data_{contract_name}.json', 'w') as outfile:
            json_data = {
                "abi": abi,
                "contract_address": contract_address[0]
            }
            json.dump(json_data, outfile, indent=4, sort_keys=True)
        # 调用主合约函数，将子合约传入主合约
        master_contract_name = data.get("master_contract_name", None)
        with open(f"master_contracts/master_contracts_json/{master_contract_name}_recordAddr.json", 'r') as f:
            datastore = json.load(f)
        abi = datastore["abi"]
        master_contract_address = datastore["contract_address"]
        func_name = "setAddr"
        func_param = contract_address[0]
        contract_instance = w3.eth.contract(address=master_contract_address, abi=abi)
        account = w3.toChecksumAddress(account)
        s1 = "functions.{func_name}('{func_param}').transact({{'from': '{account}'}})".format(func_name=func_name, func_param=func_param, account=account)
        master_tx_hash = eval("contract_instance."+s1)

        w3.eth.waitForTransactionReceipt(master_tx_hash)
        # 插入数据库
        try:
            session = db_manager.master()
            deploy_time = get_srv_time()
            new_dc = DeployContracts(contract_name=contract_name, address=account, tx_hash=tx_hash,
                                     deploy_time=deploy_time, pay_gas=pay_gas, contract_address=contract_address[0])
            session.add(new_dc)
            session.commit()
            session.close()
        except Exception as e:
            return {"code": "fail", "error": f"{e}"}
        # 生成接口文档
        generate_contrants_md()
        
        d = {
            "contract_name": contract_name,
            "tx_hash": tx_hash,
            "contract_address": contract_address[0]
        }

        ec_cli = kwargs['ec_cli']
        ec_srv = kwargs['ec_srv']
        sign = ec_srv.sign(d).decode()
        d = ec_cli.encrypt(d).decode()
        return {
            "code": "success",
            "sign": sign,
            "data": d
        }
    else:
        return {"code": "fail", "error": check}


@api_add
@check_conn(request)
def add_master_contract(*args, **kwargs):
    data = kwargs['decrypt']
    necessary_keys = ["master_contract_name"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        master_contract_name = data.get("master_contract_name", None)
        master_contract1 = "pragma solidity ^0.4.25;\n\ncontract recordAddr"
        master_contract2 = """{
    address [] contractAddr;

    //添加地址
    function setAddr(address _addr)public{
        contractAddr.push(_addr);
    }
    //返回所有地址
    function getAll()view public returns(address[]){
        return contractAddr;
    }
}"""
        with open("master_contracts/{}_recordAddr.sol".format(master_contract_name), "w", encoding="utf-8") as f:
            f.write(master_contract1+master_contract2)
            f.close()

        # 部署合约
        account = w3.eth.accounts[0]
        contract_address, abi = deploy_n_transact([f'master_contracts/{master_contract_name}_recordAddr.sol'],
                                                  account=account)
        tx_hash = contract_address[1]
        tx_receipt = contract_address[2]
        pay_gas = tx_receipt.get("gasUsed", "0")
        with open(f'master_contracts/master_contracts_json/{master_contract_name}_recordAddr.json', 'w') as outfile:
            data = {
                "abi": abi,
                "contract_address": contract_address[0]
            }
            json.dump(data, outfile, indent=4, sort_keys=True)

        session = db_manager.master()
        deploy_time = get_srv_time()
        new_dc = DeployContracts(contract_name=master_contract_name, address=account, tx_hash=tx_hash,
                                 deploy_time=deploy_time, pay_gas=pay_gas, contract_address=contract_address[0],
                                 master_mark="master")
        
        session.add(new_dc)
        session.commit()
        session.close()

        d = {
            "master_contract_name": master_contract_name,
            "tx_hash": tx_hash,
            "contract_address": contract_address[0]
        }

        ec_cli = kwargs['ec_cli']
        ec_srv = kwargs['ec_srv']
        sign = ec_srv.sign(d).decode()
        d = ec_cli.encrypt(d).decode()
        return {
            "code": "success",
            "sign": sign,
            "data": d
        }
        return {"data": "ok"}
    else:
        return {"code": "fail", "error": check}
