# coding:utf-8
import json
import logging
import time
from my_dispatcher import api_add, api
from util.compile_solidity_utils import w3
from util.check_fuc import check_kv


@api_add
def transfer_contract(*args, **kwargs):
    # 调用合约公共接口
    necessary_keys = ["account", "contract_name", "func_name"]
    check = check_kv(kwargs, necessary_keys)
    if check == "Success":
        account = kwargs.get("account", None)
        contract_name = kwargs.get("contract_name", None)
        func_name = kwargs.get("func_name", None)
        func_param = kwargs.get("func_param", None)
        value = kwargs.get("func_param", None)
        
        with open("json_files/data_{}.json".format(contract_name), 'r') as f:
            datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]
        contract_name = w3.eth.contract(address=contract_address, abi=abi)
        account = w3.toChecksumAddress(account)
        
        if "get" not in func_name and "set" not in func_name:
            tx_hash = eval("contract_name.functions.{func_name}({func_param})."
                           "transact({{'from': '{account}', 'value': w3.toWei({value}, 'ether')}})".
                           format(contract_name=contract_name, func_name=func_name,
                                  func_param=func_param, account=account, value=value))
            w3.eth.waitForTransactionReceipt(tx_hash)
            return {"data": "{} ok".format(func_name)}
        elif "set" in func_name:
            tx_hash = eval("contract_name.functions.{func_name}({func_param})."
                           "transact({{'from': '{account}', 'value': w3.toWei(0, 'ether')}})".
                           format(contract_name=contract_name, func_name=func_name,
                                  func_param=func_param, account=account))
            w3.eth.waitForTransactionReceipt(tx_hash)
            return {"data": "set {} ok".format(func_name)}
        elif "get" in func_name:
            result = eval("contract_name.functions.{func_name}({func_param}).call()".
                          format(contract_name=contract_name, func_name=func_name, func_param=func_param))
            return {"data": result}
    else:
        return {"error": check}
