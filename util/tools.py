# coding:utf-8
from util.dbmanager import db_manager
from util.errno import err_format
from util.mysql_db import TransactionRecord


def add_to_transaction(from_address="", to_address="", value="", tx_hash="", tr_appid=""):
    from util.check_fuc import get_srv_time
    transaction_time = get_srv_time()
    session = db_manager.master()
    try:
        new_tr = TransactionRecord(from_address=from_address, to_address=to_address,
                                   value=value, transaction_time=transaction_time,
                                   tx_hash=tx_hash.hex(), type=1, tr_appid=tr_appid)
        session.add(new_tr)
        session.commit()
        session.close()
    except Exception as e:
        return err_format(errno_n=-11104)
