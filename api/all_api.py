# coding:utf-8
from my_dispatcher import api_add, api
from marshmallow import Schema, fields, ValidationError
import json
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv
from flask import Flask, Response, request, jsonify
from eth_account import Account
from util.pgsql_db import get_conn, fetchall
from mnemonic.mnemonic import Mnemonic
from util.mnemonic_utils import mnemonic_to_private_key


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
    
    
@api_add
def create_account(*args, **kwargs):
    # 创建账户
    pwd = kwargs.get("pwd", None)
    if pwd:
        m = Mnemonic('english')
        mnemonic = m.generate()
        private_key = mnemonic_to_private_key(mnemonic)
        account = w3.eth.account.privateKeyToAccount(private_key)
        address = account.address
        wallet = Account.encrypt(private_key, pwd)
        # old version
        # account = Account.create()
        # private_key = account._key_obj
        # public_key = private_key.public_key
        # address = public_key.to_checksum_address()
        # wallet = Account.encrypt(account.privateKey, pwd)
        data = {
            "mnemonic": mnemonic,
            "address": address,
            "keystore": wallet
        }
        return data
    else:
        return {"error": "no password"}


@api_add
def get_balance(*args, **kwargs):
    # 获取余额
    account = kwargs.get("account", None)
    if account:
        eth_balance = w3.eth.getBalance(account, 'latest')
        return {"eth_balance": eth_balance}
    else:
        return {"error": "no account"}
    

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
            return {"error": "pwssword not ture!"}
    else:
        return {"error": check}
    

@api_add
def send_transaction(*args, **kwargs):
    # 裸交易
    necessary_keys = ["to_address", "from_address", "value", "pwd", "keystore"]
    check = check_kv(kwargs, necessary_keys)
    if check == "Success":
        to_address = kwargs.get("to_address", None)
        value = kwargs.get("value", None)
        pwd = kwargs.get("pwd", None)
        keystore = kwargs.get("keystore", None)
        private_key = Account.decrypt(json.dumps(keystore), pwd)
        account = Account.privateKeyToAccount("162a0fcdf157ef4b78e0b6caccf1fa2dabc77c8f053342454a0035dac36a01b6")
        nonce = w3.eth.getTransactionCount(account.address)
        transaction_dict = {
            'to': to_address,
            'value': w3.toWei(value, 'ether'),
            'gas': 200000,
            'gasPrice': w3.toWei(3000, 'gwei'),
            'nonce': nonce,
            'chainId': 1
        }
        signed = account.signTransaction(transaction_dict)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return {"tx_hash": tx_hash.hex()}
    else:
        return {"error": check}


@api_add
def import_private_key(*args, **kwargs):
    # 导入私钥
    private_key = kwargs.get("private_key", None)
    pwd = kwargs.get("pwd", None)
    if private_key and pwd:
        account = Account.privateKeyToAccount(private_key)
        privateKey = account._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        wallet = Account.encrypt(account.privateKey, pwd)
        data = {
            "address": address,
            "keystore": wallet
        }
        return data
    else:
        return {"error": "no privete_key or no pwd"}


@api_add
def export_private(*args, **kwargs):
    # 导出私钥
    necessary_keys = ["pwd", "keystore"]
    check = check_kv(kwargs, necessary_keys)
    if check == "Success":
        keystore = kwargs.get("keystore", None)
        pwd = kwargs.get("kwd", None)
        private_key = Account.decrypt(json.dumps(keystore), pwd)
        return {"private_key": private_key}
    else:
        return {"error": check}


@api_add
def get_all_transaction(*args, **kwargs):
    # 交易列表
    address = kwargs.get("address", None)
    necessary_keys = ["address"]
    check = check_kv(kwargs, necessary_keys)
    if check == "Success":
        sql = """select hash,from1,to1,value1 from transaction_db where from1='{}' or to1='{}'"""\
            .format(address, address)
        conn = get_conn()
        result_list = fetchall(conn, sql)
        transaction_list = []
        for l in result_list:
            d = {
                't_hash': l[0],
                'from1': l[1],
                'to1': l[2],
                'value1': w3.fromWei(int(l[3]), 'ether')
            }
            transaction_list.append(d)
        return {"transaction_list": transaction_list}
    else:
        return {"error": check}
