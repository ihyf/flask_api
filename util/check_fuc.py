# coding:utf-8
import json
from util.compile_solidity_utils import w3
from util.dbmanager import db_manager
from eth_account import Account
from util.mysql_db import ContractOp, TransactionRecord


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
        ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        print(ss1)
        t_dict = eval(ss1)
        print(t_dict)
        signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
        result = {"info": "{} ok".format(func_name)}
        type = 1
        pay_gas = ""
    elif "set" in func_name:
        ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
        print(ss1)
        t_dict = eval(ss1)
        print(t_dict)
        signed_txn = w3.eth.account.signTransaction(t_dict, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
    
        pay_gas = ""
        result = {"info": "set {} ok".format(func_name)}
        type = 1
        pay_gas = ""
    elif "get" in func_name:
        func_param = w3.toChecksumAddress(func_param)
        ss = "contract_instance.functions.{func_name}('{func_param}').call()".format(func_name=func_name,
                                                                                     func_param=func_param)
        print(ss)
        result = eval(ss)
        print(result)
    
        tx_hash = ""
        type = 2
        pay_gas = "0"
    return [result, tx_hash.hex(), pay_gas, type, account]


def send_100_to_new_account(to_address):
    # 创建账户送100个币
    keystore = {'address': '564871bc2f5768abd302b8631398cca4626af875', 'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '5d4e943bf44ca9e8fe3ca65169a652df'}, 'ciphertext': '07e8f166927a04b56c0b053c56ffac87a92dddf6b5809f1e01465e4af61566c4', 'kdf': 'pbkdf2', 'kdfparams': {'c': 1000000, 'dklen': 32, 'prf': 'hmac-sha256', 'salt': '3d0b73826b081a7109d34b91878a1d52'}, 'mac': 'fd2beb020a8f1ca3f53fd72f8c8b1f253ae22b03a3bd9d3a3e9c20499cd9f817'}, 'id': '593880ec-8713-42af-a060-92be55cf5fdd', 'version': 3}
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

