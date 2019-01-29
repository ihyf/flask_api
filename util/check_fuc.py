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
    keystore = {"address":"8a80d5366e28b1157e3aa99452a664846cfa0934","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"64c8387c7fecbf766a594f943952c2cd"},"ciphertext":"39c14d37f0bb4ea1fe7252a71089d375a2d6c2e188481c740b2969fdad0fd7a9","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"6071d213c82aae7672f79bf5556c55b3"},"mac":"f7f035687a9e90e9aeab978c7e1f2b07a88380ee00cb2dd9356cfd0841c4ae65"},"id":"a693ca7d-0cd7-476c-934f-225e3a5ae220","version":3}
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


