# coding:utf-8
from web3 import Web3, HTTPProvider
from util.pgsql_db import execute, get_conn
import time
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
check = 0
key_list = ["number", "hash", "parentHash", "mixHash", "nonce",
            "sha3Uncles", "logsBloom", "transactionsRoot", "stateRoot",
            "receiptsRoot", "miner", "difficulty", "totalDifficulty",
            "extraData", "size"]

t_key_list = ["hash", "nonce1", "blockHash", "blockNumber", "transactionIndex",
              "from1", "to1", "value1", "gas", "gasPrice", "INPUT1"]
while True:
    block_num = w3.eth.blockNumber
    print(block_num)
    if check < block_num:
        for i in range(check, block_num):
            block_data = w3.eth.getBlock(i)
            transaction_number = w3.eth.getBlockTransactionCount(i)

            d = {}
            for k in key_list:
                d.setdefault(k, "")
            d.update(block_data)
            d['hash'] = block_data.get("hash", "").hex()
            d['logsBloom'] = block_data.get("logsBloom", "").hex()
            d['mixHash'] = block_data.get("mixHash", "").hex()
            d['nonce'] = block_data.get("nonce", "").hex()
            d['parentHash'] = block_data.get("parentHash", "").hex()
            d['receiptsRoot'] = block_data.get("receiptsRoot", "").hex()
            d['stateRoot'] = block_data.get("stateRoot", "").hex()
            d['transactionsRoot'] = block_data.get("transactionsRoot", "").hex()
            d['sha3Uncles'] = block_data.get("sha3Uncles", "").hex()
            d['extraData'] = block_data.get("extraData", "").hex()

            SQL = """INSERT INTO eth_db
            VALUES(0,{number},'{hash}','{parentHash}','{mixHash}','{nonce}','{sha3Uncles}','{logsBloom}','{transactionsRoot}',
                    '{stateRoot}','{receiptsRoot}','{miner}','{difficulty}','{totalDifficulty}','{extraData}',{size})""".\
                format(**d)
            conn = get_conn()
            result = execute(conn, SQL)
            print("result: {}".format(result))
            # if have transaction write transaction data
            if transaction_number:
                transaction_data = w3.eth.getTransactionByBlock(i, 0)
                d_t = {}
                d_t['hash'] = transaction_data['hash'].hex()
                d_t['nonce1'] = transaction_data['nonce']
                d_t['blockHash'] = transaction_data['blockHash'].hex()
                d_t['blockNumber'] = transaction_data['blockNumber']
                d_t['transactionIndex'] = transaction_data['transactionIndex']
                d_t['from1'] = transaction_data['from']
                d_t['to1'] = transaction_data['to']
                d_t['value1'] = transaction_data['value']
                d_t['gas'] = transaction_data['gas']
                d_t['gasPrice'] = transaction_data['gasPrice']
                d_t['INPUT1'] = transaction_data['input']
                
                SQL_T = """INSERT INTO transaction_db
                            VALUES('{hash}',{nonce1},'{blockHash}',{blockNumber},{transactionIndex},'{from1}','{to1}',
                                    '{value1}','{gas}','{gasPrice}','{INPUT1}')""". \
                    format(**d_t)
                conn = get_conn()
                result_t = execute(conn, SQL_T)
                print("result_t: {}".format(result_t))
            else:
                pass

        check = block_num
        print("check: {}".format(check))
    else:
        print("...")
        time.sleep(0.5)



