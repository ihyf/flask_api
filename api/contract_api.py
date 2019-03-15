# coding:utf-8
import json
import os
import logging
import time
import requests
from sqlalchemy import desc
from flask import request
from cert.eth_checkout import check_conn
from my_dispatcher import api_add, api
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv, get_srv_time, format_func_param
from util.compile_solidity_utils import deploy_n_transact
from util.mysql_db import db_manager, DeployContracts, ContractOp, Apps
from util.dbmanager import db_manager
from eth_account import Account
from urllib import parse
from util.check_fuc import transfer_contract_tool
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from util.db_redis import redis_store
from util.errno import err_format
from util.tools import add_to_transaction


@api_add
@check_conn(request)
def transfer_contract(*args, **kwargs):
    # 调用合约公共接口
    appid = kwargs["appid"]
    data = kwargs['decrypt']
    master_contract_address = kwargs["master_contract_address"]
    necessary_keys = ["func_name"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        func_name = data.get("func_name", None)
        func_param = data.get("func_param", None)
        value = data.get("value", None)
        keystore = data.get("keystore", None)
        pwd = data.get("pwd", None)

        session = db_manager.master()
        try:
            dc = session.query(DeployContracts). \
                filter(DeployContracts.master_contract_address == master_contract_address). \
                order_by(desc(DeployContracts.id)).first()
            contract_name = dc.contract_name
            contract_address = dc.contract_address
        except Exception as e:
            return err_format(errno_n=-10201)

        with open("json_files/data_{}.json".format(contract_name), 'r') as f:
            datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)
        if keystore and pwd:
            try:
                private_key = Account.decrypt(json.dumps(keystore), pwd)
                account_instance = Account.privateKeyToAccount(private_key)
                address = account_instance.address
                account = w3.toChecksumAddress(address)
                print(account)
                nonce = w3.eth.getTransactionCount(account)
            except Exception as e:
                return err_format(errno_n=-11103)
        
        try:
            if "get" not in func_name and "set" not in func_name:
                func_param = format_func_param(func_param)
                s1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
                # print(s1)
                t_dict = eval(s1)
                # print(t_dict)
                signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
                tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                w3.eth.waitForTransactionReceipt(tx_hash)
                result = {"info": "{} ok".format(func_name)}
                type = 1
                pay_gas = ""

                # 增加到交易列表
                add_to_transaction(from_address=account, to_address=contract_address, value=value,
                                   tx_hash=tx_hash.hex(), tr_appid=appid)
            elif "set" in func_name:
                func_param = format_func_param(func_param)
                s2 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
                t_dict = eval(s2)
                signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
                tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                w3.eth.waitForTransactionReceipt(tx_hash)
    
                result = {"info": "set {} ok".format(func_name)}
                type = 1
                pay_gas = ""
                # 增加到交易列表
                add_to_transaction(from_address=account, to_address=contract_address, value=0,
                                   tx_hash=tx_hash.hex(), tr_appid=appid)
            elif "get" in func_name:
                func_param = format_func_param(func_param)
                s3 = "contract_instance.functions.{func_name}({func_param}).call()".format(func_name=func_name,
                                                                                             func_param=func_param)
                print(s3)
                result = eval(s3)
                print(result)
        
                tx_hash = ""
                type = 2
                pay_gas = "0"
        except Exception as e:
            return err_format(errno_n=-12101)

        # 插入数据库
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
                tx_hash = "call funcition"
            op = ContractOp(contract_name=contract_name, contract_address=contract_address,
                            op_info=op_info, op_time=op_time, tx_hash=tx_hash, type=type, pay_gas=pay_gas, op_appid=appid)
            session.add(op)
            session.commit()
            session.close()
        except Exception as e:
            return err_format(errno_n=-10205)

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
        return err_format(errno_n=-10106)
    
    
def generate_contrants_md(*args, **kwargs):
    with open("client/contracts_func.md", "w", encoding="utf-8") as cf:
        for root, dirs, files, in os.walk("json_files", topdown=False):
            for f_name in files:
                file = root + "/" + f_name
                with open(file, "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
                    abi = data.get("abi", None)
                    contract_address = data.get("contract_address", None)
                # f_name = f_name.split(".")[0].split("_")[1]
                show_f_name = f_name.split(".")[0]
                cf.write("# 合约名: " + show_f_name + "\n")
                cf.write("\n")
                cf.write("# 合约地址: " + contract_address + "\n")
                cf.write("\n")
                cf.write("函数名|参数名|参数类型|返回|返回类型|说明")
                cf.write("\n")
                cf.write(":--:|:--:|:--:|:--:|:--:|:--")
                for t in abi:
                    cf.write("\n")
                    if t["type"] == "function":
                        s_func = t["name"]
                        s_input = [it for it in t["inputs"]]
                        s_input1 = [it['name'] for it in t["inputs"]]
                        s_func = s_func + "(" + ','.join(s_input1) + ")"
                        s_return = t["outputs"]
                        cf.write(s_func + "|")
                        if s_input:
                            name_l = []
                            type_l = []
                            for i in s_input:
                                name_l.append(i["name"])
                                type_l.append(i["type"])
                            cf.write(",".join(name_l) + "|")
                            cf.write(",".join(type_l) + "|")
                        else:
                            cf.write("无" + "|")
                            cf.write("无" + "|")
                        if s_return:
                            name_l = []
                            type_l = []
                            for i in s_return:
                                name_l.append(i["name"])
                                type_l.append(i["type"])
                            cf.write(",".join(name_l) + "|")
                            cf.write(",".join(type_l) + "|")
                
                        else:
                            cf.write("无" + "|")
                            cf.write("无" + "|")
        return {"data": "ok"}
    

@api_add
@check_conn(request)
def deploy_contract(*args, **kwargs):
    data = kwargs.get("data", None)
    if data is None:
        return err_format(errno_n=-10005)
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
            new_dc = DeployContracts(master_contract_name=master_contract_name, deploy_account=account,
                                     deploy_tx_hash=tx_hash, deploy_time=deploy_time, pay_gas=pay_gas,
                                     master_contract_address=master_contract_address,
                                     contract_name=contract_name, contract_address=contract_address[0])
            session.add(new_dc)
            session.commit()
            session.close()
        except Exception as e:
            return err_format(errno_n=-10205)
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
        return err_format(errno_n=-10106)


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
        try:
            new_dc = DeployContracts(master_contract_name=master_contract_name, deploy_account=account, deploy_tx_hash=tx_hash,
                                     deploy_time=deploy_time, pay_gas=pay_gas, master_contract_address=contract_address[0],
                                     master_mark="master", contract_address="", contract_name="")
            
            session.add(new_dc)
            session.commit()
            session.close()
        except Exception as e:
            return err_format(errno_n=-10205)

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
        return err_format(errno_n=-10106)
    

@api_add
@check_conn(request)
def transfer_nopay_op(*args, **kwargs):
    # 未支付的合约调用 操作订单
    data = kwargs['decrypt']
    necessary_keys = ["func_name", "order_id"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        appid = kwargs["appid"]
        try:
            session = db_manager.master()
            app = session.query(Apps).filter(Apps.appid == appid).one()
            if app:
                master_contract_address = app.master_contract_address[0]
                dc = session.query(DeployContracts). \
                    filter(DeployContracts.master_contract_address == master_contract_address). \
                    order_by(desc(DeployContracts.id)).first()
                contract_name = dc.contract_name
                contract_address = dc.contract_address
            else:
                return err_format(errno_n=-12201)
            
            func_name = data.get("func_name")
            func_param = data.get("func_param")
            callback_url = data.get("callback_url")
            value = str(data.get("value"))
            order_id = data.get("order_id")
            op_info = {
                "func_name": func_name,
                "func_param": func_param,
                "value": value,
                "callback_url": callback_url,
                "address": "",
                "appid": appid
            }
            # op_time = time.strftime("%Y-%m-%d %X", time.localtime())
            op_time = get_srv_time()

            # type 2为无需支付 1为已支付 0为初始态 -1为失效
            op = ContractOp(contract_name=contract_name, contract_address=contract_address,
                            op_info=op_info, op_time=op_time, tx_hash="", type=0, order_id=order_id)
            session.add(op)
            session.commit()
            session.close()
        except Exception as e:
            return err_format(errno_n=-10205)
        result = {"op_id": str(op.op_id)}
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
        return err_format(errno_n=-10106)


@api_add
@check_conn(request)
def op_details(*args, **kwargs):
    # 操作详情
    data = kwargs['decrypt']
    necessary_keys = ["op_id"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        try:
            op_id = data.get("op_id")
            session = db_manager.slave()
            op = session.query(ContractOp).filter(ContractOp.op_id == op_id).one()
            result = {"op_info": op.op_info}
            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()

            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
        except Exception as e:
            return err_format(errno_n=-40000)
    else:
        return err_format(errno_n=-10106)


@api_add
@check_conn(request)
def pay_transfer_op(*args, **kwargs):
    data = kwargs['decrypt']
    necessary_keys = ["op_id", "keystore", "pwd"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        try:
            op_id = data.get("op_id")
            keystore = data.get("keystore")
            pwd = data.get("pwd")
            session = db_manager.slave()
            op = session.query(ContractOp).filter(ContractOp.op_id == op_id).one()
            contract_name = op.contract_name
            func_name = op.op_info.get("func_name")
            func_param = op.op_info.get("func_param")
            value = op.op_info.get("value")
            appid = op.op_info.get("appid")
            app = session.query(Apps).filter(Apps.appid == appid).one()
            callback_url = op.op_info.get("callback_url")
            order_id = op.order_id
            data = {
               "keystore": keystore,
                "pwd": pwd,
                "contract_name": contract_name,
                "func_name": func_name,
                "func_param": func_param,
                "value": value
            }
            result_list = transfer_contract_tool(data)
            result = result_list[0]
            tx_hash = result_list[1]
            pay_gas = result_list[2]
            type = result_list[3]
            account = result_list[4]
            op_time = get_srv_time()
            
            op.tx_hash = tx_hash
            op.pay_gas = pay_gas
            op.op_time = op_time
            op_info = {
                "func_name": func_name,
                "func_param": func_param,
                "value": value,
                "callback_url": callback_url,
                "address": account,
                "appid": appid
            }
            op.op_info = op_info
            op.type = type
            
            session.commit()
            session.close()

            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            
            # 要push到redis的数据
            
            notify_queue = {
                "order_id": order_id,
                "fee": value,
                "op_id": op_id,
                "callback_url": callback_url,
                "address": account,
                "srv_private_key": app.srv_privatekey,
                "cli_public_key": app.cli_publickey
            }
            notify_queue = json.dumps(notify_queue)
            redis_store.lpush("notify_queue", notify_queue)
            
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()
    
            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
        except Exception as e:
            return err_format(errno_n=-40000)
    else:
        return err_format(errno_n=-10106)


@api_add
@check_conn(request)
def op_details_fordapp(*args, **kwargs):
    # 操作详情 dapp查询订单接口
    data = kwargs['decrypt']
    necessary_keys = ["op_id"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        try:
            op_id = data.get("op_id")
            session = db_manager.slave()
            op = session.query(ContractOp).filter(ContractOp.op_id == op_id).one()
            result = {"op_info": op.op_info, "order_id": op.order_id, "type": op.type}
            ec_cli = kwargs['ec_cli']
            ec_srv = kwargs['ec_srv']
            sign = ec_srv.sign(result).decode()
            result = ec_cli.encrypt(result).decode()

            return {
                "code": "success",
                "sign": sign,
                "data": result
            }
        except Exception as e:
            return err_format(errno_n=-40000)
    else:
        return err_format(errno_n=-10106)
