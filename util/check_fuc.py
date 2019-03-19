# coding:utf-8
import json
import os

from util.compile_solidity_utils import w3
from util.dbmanager import db_manager
from eth_account import Account
from util.mysql_db import ContractOp, TransactionRecord
from util.tools import add_to_transaction
import config


def check_kv(d1, necessary_keys):
    """校验接口传入的keys values和必要的参数差别"""
    error = ""
    for k in necessary_keys:
        if k not in d1.keys():
            error += str(k) + " key error"
            return error
        if not d1[k]:
            error += str(k) + " do not have value"
            return error
    if error:
        return error
    else:
        return "Success"


def to_byte32(s):
    len1 = len(s)
    if len1 > 32:
        print('input string length: ' + str(len1) + ' is too long')
        s = s[:32]
    else:
        print('input string length: ' + str(len1) + ' is too short')
        print('More characters needed: ' + str(32 - len1))
        s = bytes(s.ljust(32, '0'), 'utf-8')
    return s


def bytes_str_to_dict(b):
    return eval(str(b, encoding="utf-8"))


def get_srv_time():
    """获取服务器当前时间，并格式化成字符串"""
    # 服务器时间 + 8 hour
    import datetime
    t = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return t


def transfer_contract_tool(data):
    # 调用合约 工具函数
    appid = data.get("appid", None)
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

    private_key = Account.decrypt(json.dumps(keystore), pwd)
    account_instance = Account.privateKeyToAccount(private_key)
    account = account_instance.address
    account = w3.toChecksumAddress(account)
    nonce = w3.eth.getTransactionCount(account)
    
    if "get" not in func_name and "set" not in func_name:
        func_param = format_func_param(func_param)
        # ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        s1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        print(s1)
        t_dict = eval(s1)
        print(t_dict)
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
        #ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        s2 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        print(s2)
        t_dict = eval(s2)
        print(t_dict)
        signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
    
        pay_gas = ""
        result = {"info": "set {} ok".format(func_name)}
        type = 1
        pay_gas = ""
        # 增加到交易列表
        add_to_transaction(from_address=account, to_address=contract_address, value=value,
                           tx_hash=tx_hash.hex(), tr_appid=appid)
    elif "get" in func_name:
        # func_param = w3.toChecksumAddress(func_param)
        # ss = "contract_instance.functions.{func_name}('{func_param}').call()".format(func_name=func_name,
        #                                                                              func_param=func_param)
        func_param = format_func_param(func_param)
        s3 = "contract_instance.functions.{func_name}({func_param}).call()".format(func_name=func_name,
                                                                                   func_param=func_param)
        print(s3)
        result = eval(s3)
        print(result)

        tx_hash = ""
        type = 2
        pay_gas = "0"
    return [result, tx_hash.hex(), pay_gas, type, account]


def send_100_to_new_account(to_address):
    # 创建账户送100个币
    keystore = config.to_100_keystore
    pwd = "hyf"
    private_key = Account.decrypt(json.dumps(keystore), pwd)
    account = Account.privateKeyToAccount(private_key)
    from_address = account.address
    nonce = w3.eth.getTransactionCount(account.address)
    transaction_dict = {
        'to': to_address,
        'value': w3.toWei(100, 'ether'),
        'gas': 200000,
        'gasPrice': w3.toWei(30, 'gwei'),
        'nonce': nonce,
        'chainId': 1500
    }
    signed = account.signTransaction(transaction_dict)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    
    # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    receipt = 1
    if receipt:
        # 插入数据库
        # transaction_time = time.strftime("%Y-%m-%d %X", time.localtime())
        # 服务器时间 + 8 hour
        transaction_time = get_srv_time()
        session = db_manager.master()
        try:
            new_tr = TransactionRecord(from_address=from_address, to_address=to_address,
                                       value=100, transaction_time=transaction_time,
                                       tx_hash=tx_hash.hex(), type=1)
            session.add(new_tr)
            session.commit()
            session.close()
        except Exception as e:
            return {"code": "fail", "error": f"{e}"}


def format_func_param(func_param):
    func_param = func_param.split(",")
    t = []
    for f in func_param:
        if isinstance(f, str) and "0x" in f:
            f = "'" + w3.toChecksumAddress(f) + "'"
        t.append(f)
    func_param = ",".join(t)
    return func_param


def generate_contrants_md_bak(*args, **kwargs):
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