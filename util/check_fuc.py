# coding:utf-8
import json
from util.compile_solidity_utils import w3
from util.dbmanager import db_manager
from eth_account import Account
from util.mysql_db import ContractOp


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
    import datetime
    t = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return t


def transfer_contract_tool(data):
    # 调用合约 工具函数
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
        ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 200000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        t_dict = eval(ss1)
        signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
        
        result = {"info": "{} ok".format(func_name)}
        type = 1
        pay_gas = ""
    elif "set" in func_name:
        s = f"""contract_instance.functions.{func_name}({func_param}).transact({{'from': '{account}', 'value': w3.toWei({value}, 'ether')}})"""
        tx_hash = eval(s)
        w3.eth.waitForTransactionReceipt(tx_hash)
        
        result = {"info": "set {} ok".format(func_name)}
        type = 1
        pay_gas = ""
    elif "get" in func_name:
        result = eval("contract_instance.functions.{func_name}({func_param}).call()".
                      format(func_name=func_name, func_param=func_param))
        tx_hash = ""
        type = 2
        pay_gas = "0"
    
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
                        op_info=op_info, op_time=op_time, tx_hash=tx_hash, type=type, pay_gas=pay_gas)
        session.add(op)
        session.commit()
        session.close()
    except Exception as e:
        return {
            "code": "fail",
            "error": f"{e}"
        }
    
    return result
