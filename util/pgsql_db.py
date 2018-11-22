# coding:utf-8
# !/usr/bin/python3
import psycopg2
import psycopg2.pool
db_param = {
    "database": "postgres",
    "host": "127.0.0.1",
    "user": "postgres",
    "password": "123456",
    "port": "5432"
}

sql_eth_db = """CREATE TABLE eth_db(number integer,hash TEXT,parentHash TEXT,mixHash TEXT ,
                nonce TEXT ,sha3Uncles TEXT ,logsBloom TEXT ,transactionsRoot TEXT ,stateRoot TEXT ,
                receiptsRoot TEXT ,miner TEXT ,difficulty TEXT ,totalDifficulty TEXT ,extraData TEXT,
                size integer );"""

sql_transaction_db = """CREATE TABLE transaction_db (
                        hash TEXT,
                        nonce1 INTEGER,
                        blockHash TEXT,
                        blockNumber INTEGER,
                        transactionIndex INTEGER,
                        from1 TEXT,
                        to1 TEXT,
                        value1 TEXT,
                        gas TEXT,
                        gasPrice TEXT,
                        INPUT1 TEXT
                    );"""


# 创建连接对象
def get_conn():
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="123456", host="localhost", port="5432")
    return conn


def fetchall(conn, sql):
    try:
        cur = conn.cursor()  # 创建指针对象
        cur.execute(sql)
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        return "Fail"


def fetchone(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        return "Fail"
    

def execute(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        result = "Success"
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        return "Fail"



