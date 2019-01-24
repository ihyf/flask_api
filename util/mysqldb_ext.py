# coding:utf-8
from sqlalchemy.orm import mapper
from wallet.util.mysqldb import Base
from sqlalchemy.schema import CreateTable
from wallet.util.mysqldb import db_manager


def create_table_base_table(name, tablename):
    try:
        engine = db_manager.get_engine_master()
        Base.metadata.reflect(engine)
        table = Base.metadata.tables[tablename]
        c = str(CreateTable(table))
        c = c.replace("CREATE TABLE " + tablename, "CREATE TABLE if not exists " + name)
        db_conn = engine.connect()
        db_conn.execute(c)
        db_conn.close()
        Base.metadata.clear()
        db_manager.flush_autobase()
        return True
    except:
        return False


