# coding:utf-8
from my_dispatcher import api_add, api
from marshmallow import Schema, fields, ValidationError
import json
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv
from flask import Flask, Response, request, jsonify
from eth_account import Account


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
    return jsonify({"data": user_data}), 200


@api_add
def create_account(*args, **kwargs):
    # 创建账户
    password = kwargs.get("password", None)
    if password:
        account = w3.personal.newAccount(password)
        return {"account": account}
    else:
        return {"error": "no password"}
    
    
@api_add
def create_account1(*args, **kwargs):
    password = kwargs.get("password", None)
    if password:
        account = Account.create()
        private_key = account._key_obj
        public_key = private_key.public_key
        address = public_key.to_checksum_address()
        wallet = Account.encrypt(account.privateKey, password)
        data = {
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
def send_transaction(*args, **kwargs):
    # 转账
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
def import_private_key(*args, **kwargs):
    # 导入私钥
    private_key = kwargs.get("private_key", None)
    if private_key:
        account = Account.privateKeyToAccount(private_key)
        privateKey = account._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        return {"address": address}
    else:
        return {"error": "no privete_key"}


@api_add
def get_all_transaction(*args, **kwargs):
    address = kwargs.get("address", None)
    filter = w3.eth.filter({'fromBlock': 0, 'toBlock': 'latest', 'address': address})
    b = dir(filter)
    a = filter.__dict__.items()
    print(a)
