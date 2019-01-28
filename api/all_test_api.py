# coding:utf-8
import json
import logging
import time
from my_dispatcher import api_add, api
from marshmallow import Schema, fields, ValidationError
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv
from flask import Flask, Response, request, jsonify
from my_dispatcher import api_add
from util.dbmanager import db_manager
from util.mysql_db import Apps
from cert.eth_certs import EthCert
from eth_account import Account
from util.pgsql_db import get_conn, fetchall
from mnemonic.mnemonic import Mnemonic
from util.mnemonic_utils import mnemonic_to_private_key
from cert.eth_checkout import check_conn
from util.mysql_db import db_manager, Accounts, TransactionRecord
from sqlalchemy import and_,or_


def check_gender(data):
    valid_list = ["male", "female"]
    if data not in valid_list:
        raise ValidationError(
            'Invalid gender. Valid choices are' + valid_list
        )
    
    
class UserSchema(Schema):
    name = fields.String(required=True)
    gender = fields.String(required=True, validate=check_gender)
    
    
@api_add
def my_method(*args, **kwargs):
    d = {"ihyf": 111}
    return d


# @api_add
# def transfer_contract(*args, **kwargs):
#     # 调用合约公共接口
#     necessary_keys = ["account", "contract_name", "func_name"]
#     check = check_kv(kwargs,
# )
#     if check == "Success":
#         account = kwargs.get("account", None)
#         contract_name = kwargs.get("contract_name", None)
#         func_name = kwargs.get("func_name", None)
#         func_param = kwargs.get("func_param", None)
#         value = kwargs.get("func_param", None)
#
#         with open("json_files/data_{}.json".format(contract_name), 'r') as f:
#             datastore = json.load(f)
#         abi = datastore["abi"]
#         contract_address = datastore["contract_address"]
#         contract_name = w3.eth.contract(address=contract_address, abi=abi)
#         account = w3.toChecksumAddress(account)
#
#         if "get" not in func_name and "set" not in func_name:
#             tx_hash = eval("contract_name.functions.{func_name}({func_param})."
#                            "transact({{'from': '{account}', 'value': w3.toWei({value}, 'ether')}})".
#                            format(contract_name=contract_name, func_name=func_name,
#                                   func_param=func_param, account=account, value=value))
#             w3.eth.waitForTransactionReceipt(tx_hash)
#             return {"data": "{} ok".format(func_name)}
#         elif "set" in func_name:
#             tx_hash = eval("contract_name.functions.{func_name}({func_param})."
#                            "transact({{'from': '{account}', 'value': w3.toWei(0, 'ether')}})".
#                            format(contract_name=contract_name, func_name=func_name,
#                                   func_param=func_param, account=account))
#             w3.eth.waitForTransactionReceipt(tx_hash)
#             return {"data": "set {} ok".format(func_name)}
#         elif "get" in func_name:
#             result = eval("contract_name.functions.{func_name}({func_param}).call()".
#                           format(contract_name=contract_name, func_name=func_name, func_param=func_param))
#             return {"data": result}
#     else:
#         return {"error": check}

    
@api_add
def voting_contract(*args, **kwargs):
    w3.eth.defaultAccount = w3.eth.accounts[1]
    
    with open("data_voting.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    
    # Create the contract instance with the newly-deployed address
    voting = w3.eth.contract(
        address=contract_address, abi=abi,
    )
    voting_list = kwargs.get("voting_list", None)
    tx_hash = voting.functions.setUpVote(
        voting_list
    )
    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...
    w3.eth.waitForTransactionReceipt(tx_hash)
    # user_data = voting.functions.getUser().call()
    return {"data": "voting ok"}


@api_add
def user_contract(*args, **kwargs):
    # 测试合约
    w3.eth.defaultAccount = w3.eth.accounts[1]
    
    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    
    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )
    body = request.get_json()
    name = body['params']['name']
    gender = body['params']['gender']
    # result, error = UserSchema().load(body)
    # if error:
    #     return jsonify(error), 422
    tx_hash = user.functions.setUser(
        name, gender
    )
    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...
    w3.eth.waitForTransactionReceipt(tx_hash)
    user_data = user.functions.getUser().call()
    return {"data": user_data}


@api_add
def create_account_11(*args, **kwargs):
    # 创建账户 11
    password = kwargs.get("password", None)
    if password:
        account = w3.personal.newAccount(password)
        return {"account": account}
    else:
        return {"error": "no password"}
    
    
# @api_add
# @check_conn(request)
# def create_account(*args, **kwargs):
#     # 创建账户
#     data = kwargs['decrypt']
#     pwd = data.get("pwd", None)
#     if pwd:
#         m = Mnemonic('english')
#         mnemonic = m.generate()
#         private_key = mnemonic_to_private_key(mnemonic)
#         account = w3.eth.account.privateKeyToAccount(private_key)
#         address = account.address
#         wallet = Account.encrypt(private_key, pwd)
#         # old version
#         # account = Account.create()
#         # private_key = account._key_obj
#         # public_key = private_key.public_key
#         # address = public_key.to_checksum_address()
#         # wallet = Account.encrypt(account.privateKey, pwd)
#
#         # 插入数据库
#         create_time = time.strftime("%Y-%m-%d %X", time.localtime())
#         session = db_manager.master()
#         new_account = Accounts(address=address, balance=0,
#                                create_time=create_time, type=1)
#         session.add(new_account)
#         session.commit()
#         session.close()
#
#         result = {
#             "mnemonic": mnemonic,
#             "address": address,
#             "keystore": wallet,
#             "private_key": private_key.hex()
#         }
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(result).decode()
#         result = ec_cli.encrypt(result).decode()
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": result
#         }
#     else:
#         return {
#             "code": "fail",
#             "error": "no password"
#         }


# @api_add
# @check_conn(request)
# def get_balance(*args, **kwargs):
#     # 获取余额
#     data = kwargs['decrypt']
#     address = data.get("address", None)
#     if address:
#         eth_balance = w3.fromWei(w3.eth.getBalance(address, '  '), 'ether')
#         eth_balance = str(eth_balance)
#         d = {
#             "eth_balance": eth_balance
#         }
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(d).decode()
#         d = ec_cli.encrypt(d).decode()
#
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": d
#         }
#     else:
#         return {
#             "code": "fail",
#             "error": "no address"
#         }
    

@api_add
def send_transaction_11(*args, **kwargs):
    # 转账 明文..
    necessary_keys = ["to_address", "from_address", "value", "pwd"]
    check = check_kv(kwargs, necessary_keys)
    if check == "Success":
        to_address = kwargs.get("to_address", None)
        from_address = kwargs.get("from_address", None)
        value = kwargs.get("value", None)
        pwd = kwargs.get("pwd", None)
        # 解锁账户
        if w3.personal.unlockAccount(from_address, pwd):
        
            transaction_dict = {
                "to": to_address,
                "from": from_address,
                "value": w3.toWei(value, 'ether')
            }
        
            tx_hash_bytes = w3.eth.sendTransaction(transaction_dict)
            tx_hash = tx_hash_bytes.hex()
            return {"tx_hash": tx_hash}
        else:
            return {"error": "password not right!"}
    else:
        return {"error": check}
    

# @api_add
# @check_conn(request)
# def send_transaction(*args, **kwargs):
#     # 裸交易
#     data = kwargs['decrypt']
#     necessary_keys = ["to_address", "value", "pwd", "keystore", "gas_limit", "gas_price"]
#     check = check_kv(data, necessary_keys)
#     if check == "Success":
#         to_address = data.get("to_address", None)
#         to_address = w3.toChecksumAddress(to_address)
#         value = data.get("value", None)
#         pwd = data.get("pwd", None)
#         keystore = data.get("keystore", None)
#         gas_limit = data.get("gas_limit", None)
#         gas_price = data.get("gas_price", None)
#         private_key = Account.decrypt(json.dumps(keystore), pwd)
#         account = Account.privateKeyToAccount("7af5932779d6d3323af7709f6de598828e872e75cf255a482db9e006eb95abd7")
#         from_address = account.address
#         nonce = w3.eth.getTransactionCount(account.address)
#         transaction_dict = {
#             'to': to_address,
#             'value': w3.toWei(value, 'ether'),
#             'gas': gas_limit,
#             'gasPrice': w3.toWei(gas_price, 'gwei'),
#             'nonce': nonce,
#             'chainId': 1
#         }
#         signed = account.signTransaction(transaction_dict)
#         tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
#         receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#         if receipt:
#             # 插入数据库
#             transaction_time = time.strftime("%Y-%m-%d %X", time.localtime())
#             session = db_manager.master()
#             new_tr = TransactionRecord(from_address=from_address, to_address=to_address,
#                                        value=value, transaction_time=transaction_time,
#                                        tx_hash=tx_hash.hex(), type=1)
#             session.add(new_tr)
#             session.commit()
#             session.close()
#
#         d = {
#             "tx_hash": tx_hash.hex()
#         }
#
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(d).decode()
#         d = ec_cli.encrypt(d).decode()
#
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": d
#         }
#     else:
#         return {"code": "fail", "error": check}


# @api_add
# @check_conn(request)
# def import_private_key(*args, **kwargs):
#     # 导入私钥
#     data = kwargs['decrypt']
#     necessary_keys = ["private_key", "pwd"]
#     check = check_kv(data, necessary_keys)
#     if check != "Success":
#         return {"code": "fail", "error": check}
#     private_key = data.get("private_key", None)
#     pwd = data.get("pwd", None)
#     if private_key and pwd:
#         account = Account.privateKeyToAccount(private_key)
#         privateKey = account._key_obj
#         publicKey = privateKey.public_key
#         address = publicKey.to_checksum_address()
#         wallet = Account.encrypt(account.privateKey, pwd)
#
#         d = {
#             "address": address,
#             "keystore": wallet
#         }
#
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(d).decode()
#         d = ec_cli.encrypt(d).decode()
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": d
#         }
#     else:
#         return {"code": "fail", "error": "no private_key or no pwd"}
#
#
# @api_add
# @check_conn(request)
# def import_keystore(*args, **kwargs):
#     # 导入keystore
#     data = kwargs['decrypt']
#     necessary_keys = ["keystore", "pwd"]
#     check = check_kv(data, necessary_keys)
#     if check != "Success":
#         return {"code": "fail", "error": check}
#     keystore = data.get("keystore", None)
#     pwd = data.get("pwd", None)
#     private_key = Account.decrypt(json.dumps(keystore), pwd)
#     account = Account.privateKeyToAccount(private_key)
#     privateKey = account._key_obj
#     publicKey = privateKey.public_key
#     address = publicKey.to_checksum_address()
#     keystore = Account.encrypt(account.privateKey, pwd)
#
#     d = {
#         "address": address,
#         "keystore": keystore,
#         "private_key": private_key.hex()
#     }
#
#     ec_cli = kwargs['ec_cli']
#     ec_srv = kwargs['ec_srv']
#     sign = ec_srv.sign(d).decode()
#     d = ec_cli.encrypt(d).decode()
#
#     return {
#         "code": "success",
#         "sign": sign,
#         "data": d
#     }
#
#
# @api_add
# @check_conn(request)
# def export_private(*args, **kwargs):
#     # 导出私钥
#     data = kwargs['decrypt']
#     necessary_keys = ["pwd", "keystore"]
#     check = check_kv(data, necessary_keys)
#     if check == "Success":
#         keystore = data.get("keystore", None)
#         pwd = data.get("pwd", None)
#         private_key = Account.decrypt(json.dumps(keystore), pwd)
#
#         d = {"private_key": private_key.hex()}
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(d).decode()
#         d = ec_cli.encrypt(d).decode()
#
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": d
#         }
#     else:
#         return {"code": "fail", "error": check}
#
#
# @api_add
# @check_conn(request)
# def export_keystore(*args, **kwargs):
#     # 导出keystore
#     data = kwargs['decrypt']
#     necessary_keys = ["keystore", "pwd"]
#     check = check_kv(data, necessary_keys)
#     if check != "Success":
#         return {"code": "fail", "error": check}
#     keystore = data.get("keystore", None)
#     pwd = data.get("pwd", None)
#     private_key = Account.decrypt(json.dumps(keystore), pwd)
#     account = Account.privateKeyToAccount(private_key)
#     keystore = Account.encrypt(account.privateKey, pwd)
#
#     d = {"keystore": keystore}
#
#     ec_cli = kwargs['ec_cli']
#     ec_srv = kwargs['ec_srv']
#     sign = ec_srv.sign(d).decode()
#     d = ec_cli.encrypt(d).decode()
#
#     return {
#         "code": "success",
#         "sign": sign,
#         "data": d
#     }
#
#
# @api_add
# @check_conn(request)
# def get_all_transaction(*args, **kwargs):
#     # 交易列表
#     data = kwargs['decrypt']
#     address = data.get("address", None)
#     necessary_keys = ["address"]
#     check = check_kv(data, necessary_keys)
#     if check == "Success":
#         session = db_manager.slave()
#         try:
#             r_list = session.query(TransactionRecord).filter(or_(TransactionRecord.from_address == address,
#                                                             TransactionRecord.to_address == address)).all()
#
#             session.close()
#         except Exception as e:
#             return {"code": "fail", "error": f"{e}"}
#         transaction_list = []
#         for l in r_list:
#             d_l = {
#                 'tx_hash': l.tx_hash,
#                 'from_address': l.from_address,
#                 'to_address': l.to_address,
#                 'value': l.value
#             }
#             transaction_list.append(d_l)
#
#         d = {"transaction_list": transaction_list}
#
#         ec_cli = kwargs['ec_cli']
#         ec_srv = kwargs['ec_srv']
#         sign = ec_srv.sign(d). ()
#         d = ec_cli.encrypt(d).decode()
#
#         return {
#             "code": "success",
#             "sign": sign,
#             "data": d
#         }
#     else:
#         return {"error": check}


@api_add
def add_app(*args, **kwargs):
    ec = EthCert("hyf_app")
    ec.generate(4096)
    cli_pbk = ec.public_key_str
    cli_prk = ec.private_key_str
    ec.save_file()
    
    ec1 = EthCert("hyf_srv")
    ec1.generate(4096)
    srv_pbk = ec1.public_key_str
    srv_prk = ec1.private_key_str
    ec1.save_file()
    
    session = db_manager.master()
    new_app = Apps(appid="hyf_app", ip=["localhost"], ns=["127.0.0.1"],
                   cli_publickey=cli_pbk, cli_privatekey=cli_prk, status=1,
                   srv_publickey=srv_pbk, srv_privatekey=srv_prk, desc="xxxx", srv="xxx")
    session.add(new_app)
    session.commit()
    session.close()
    return "add app ok"


@api_add
def test_redis(*args, **kwargs):
    import json
    from util.db_redis import redis_store
    r = {
        "order_id": "1",
        "fee": "2",
        "op_id": "3",
        "call_back_url": "",
        "address": "4"
    }
    r_j = json.dumps(r)
    redis_store.lpush("data", r_j)
    return {"data": "liujin zhenshuai"}
