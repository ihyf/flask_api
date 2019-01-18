# coding:utf-8
import json
import logging
import time
from my_dispatcher import api_add, api
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv
from flask import request
from eth_account import Account
from mnemonic.mnemonic import Mnemonic
from util.mnemonic_utils import mnemonic_to_private_key
from cert.eth_checkout import check_conn
from util.mysql_db import db_manager, Accounts, TransactionRecord
from sqlalchemy import and_,or_


@api_add
@check_conn(request)
def create_account(*args, **kwargs):
    # 创建账户
    data = kwargs['decrypt']
    pwd = data.get("pwd", None)
    if pwd:
        # m = Mnemonic('english')
        # mnemonic = m.generate()
        # private_key = mnemonic_to_private_key(mnemonic)
        # account = w3.eth.account.privateKeyToAccount(private_key)
        # address = account.address
        # wallet = Account.encrypt(private_key, pwd)
        # old version
        account = Account.create()
        private_key = account._key_obj
        public_key = private_key.public_key
        address = public_key.to_checksum_address()
        wallet = Account.encrypt(account.privateKey, pwd)
        
        # 插入数据库
        create_time = time.strftime("%Y-%m-%d %X", time.localtime())
        session = db_manager.master()
        new_account = Accounts(address=address, balance=0,
                               create_time=create_time, type=1)
        session.add(new_account)
        session.commit()
        session.close()
        
        # result = {
        #     "mnemonic": mnemonic,
        #     "address": address,
        #     "keystore": wallet,
        #     "private_key": private_key.hex()
        # }
        result = {
            "mnemonic": "",
            "address": address,
            "keystore": wallet,
            "private_key": str(private_key)
        }
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
        return {
            "code": "fail",
            "error": "no password"
        }


@api_add
@check_conn(request)
def get_balance(*args, **kwargs):
    # 获取余额
    data = kwargs['decrypt']
    address_list = data.get("address", None)
    L = []
    if address_list:
        address_list = eval(address_list)
        for address in address_list:
            address = w3.toChecksumAddress(address)
            eth_balance = w3.fromWei(w3.eth.getBalance(address, 'latest'), 'ether')
            eth_balance = str(eth_balance)
            d = {
                "address": address,
                "eth_balance": eth_balance
            }
            L.append(d)
        ec_cli = kwargs['ec_cli']
        ec_srv = kwargs['ec_srv']
        sign = ec_srv.sign(L).decode()
        d_list = ec_cli.encrypt(L).decode()
        
        return {
            "code": "success",
            "sign": sign,
            "data": d_list
            
        }
    else:
        return {
            "code": "fail",
            "error": "no address"
        }


@api_add
@check_conn(request)
def send_transaction(*args, **kwargs):
    # 裸交易
    data = kwargs['decrypt']
    necessary_keys = ["to_address", "value", "pwd", "keystore", "gas_limit", "gas_price"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        to_address = data.get("to_address", None)
        to_address = w3.toChecksumAddress(to_address)
        value = data.get("value", None)
        pwd = data.get("pwd", None)
        keystore = data.get("keystore", None)
        gas_limit = data.get("gas_limit", None)
        gas_price = data.get("gas_price", None)
        private_key = Account.decrypt(json.dumps(keystore), pwd)
        account = Account.privateKeyToAccount(private_key)
        from_address = account.address
        nonce = w3.eth.getTransactionCount(account.address)
        transaction_dict = {
            'to': to_address,
            'value': w3.toWei(value, 'ether'),
            'gas': gas_limit,
            'gasPrice': w3.toWei(gas_price, 'gwei'),
            'nonce': nonce,
            'chainId': 1500
        }
        signed = account.signTransaction(transaction_dict)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if receipt:
            # 插入数据库
            transaction_time = time.strftime("%Y-%m-%d %X", time.localtime())
            session = db_manager.master()
            try:
                new_tr = TransactionRecord(from_address=from_address, to_address=to_address,
                                           value=value, transaction_time=transaction_time,
                                           tx_hash=tx_hash.hex(), type=1)
                session.add(new_tr)
                session.commit()
                session.close()
            except Exception as e:
                return {"code": "fail", "error": f"{e}"}
        
        d = {
            "tx_hash": tx_hash.hex()
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
def import_private_key(*args, **kwargs):
    # 导入私钥
    data = kwargs['decrypt']
    necessary_keys = ["private_key", "pwd"]
    check = check_kv(data, necessary_keys)
    if check != "Success":
        return {"code": "fail", "error": check}
    private_key = data.get("private_key", None)
    pwd = data.get("pwd", None)
    if private_key and pwd:
        account = Account.privateKeyToAccount(private_key)
        privateKey = account._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        wallet = Account.encrypt(account.privateKey, pwd)
        
        d = {
            "address": address,
            "keystore": wallet
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
        return {"code": "fail", "error": "no private_key or no pwd"}


@api_add
@check_conn(request)
def import_keystore(*args, **kwargs):
    # 导入keystore
    data = kwargs['decrypt']
    necessary_keys = ["keystore", "pwd"]
    check = check_kv(data, necessary_keys)
    if check != "Success":
        return {"code": "fail", "error": check}
    keystore = data.get("keystore", None)
    pwd = data.get("pwd", None)
    private_key = Account.decrypt(json.dumps(keystore), pwd)
    account = Account.privateKeyToAccount(private_key)
    privateKey = account._key_obj
    publicKey = privateKey.public_key
    address = publicKey.to_checksum_address()
    keystore = Account.encrypt(account.privateKey, pwd)
    
    d = {
        "address": address,
        "keystore": keystore,
        "private_key": private_key.hex()
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


@api_add
@check_conn(request)
def export_private(*args, **kwargs):
    # 导出私钥
    data = kwargs['decrypt']
    necessary_keys = ["pwd", "keystore"]
    check = check_kv(data, necessary_keys)
    if check == "Success":
        keystore = data.get("keystore", None)
        pwd = data.get("pwd", None)
        private_key = Account.decrypt(json.dumps(keystore), pwd)
        
        d = {"private_key": private_key.hex()}
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
def export_keystore(*args, **kwargs):
    # 导出keystore
    data = kwargs['decrypt']
    necessary_keys = ["keystore", "pwd"]
    check = check_kv(data, necessary_keys)
    if check != "Success":
        return {"code": "fail", "error": check}
    keystore = data.get("keystore", None)
    pwd = data.get("pwd", None)
    private_key = Account.decrypt(json.dumps(keystore), pwd)
    account = Account.privateKeyToAccount(private_key)
    keystore = Account.encrypt(account.privateKey, pwd)
    
    d = {"keystore": keystore}
    
    ec_cli = kwargs['ec_cli']
    ec_srv = kwargs['ec_srv']
    sign = ec_srv.sign(d).decode()
    d = ec_cli.encrypt(d).decode()
    
    return {
        "code": "success",
        "sign": sign,
        "data": d
    }


@api_add
@check_conn(request)
def get_all_transaction(*args, **kwargs):
    # 交易列表
    data = kwargs['decrypt']
    necessary_keys = ["address", "page", "limit"]
    address = data.get("address", None)
    page = data.get("page", 1)-1
    limit = data.get("limit", 10)
    check = check_kv(data, necessary_keys)
    if check == "Success":
        session = db_manager.slave()
        try:
            r_list = session.query(TransactionRecord).\
                filter(or_(TransactionRecord.from_address == address,
                           TransactionRecord.to_address == address)).\
                order_by(-TransactionRecord.transaction_time)[page*limit:(page+1)*limit]
            
            session.close()
        except Exception as e:
            return {"code": "fail", "error": f"{e}"}
        transaction_list = []
        for l in r_list:
            d_l = {
                'transaction_time': l.transaction_time,
                'tx_hash': l.tx_hash,
                'from_address': l.from_address,
                'to_address': l.to_address,
                'value': l.value
            }
            transaction_list.append(d_l)
        
        d = {"transaction_list": transaction_list}
        
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
        return {"error": check}


def search_transaction(hx_hash):
    data = w3.eth.getTransaction(hx_hash)
    return data

