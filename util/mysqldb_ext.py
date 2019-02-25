# coding:utf-8
from sqlalchemy.schema import CreateTable
from util.dbmanager import db_manager


def mirror_tb_1db(origin_tname, new_tname, dbalias):
    """同一个数据库之间"""
    abobj = db_manager.get_autobase_obj(dbalias)
    engine = abobj['engine']
    autobase = abobj['autobase']
    table = autobase.metadata.tables[origin_tname]
    c = str(CreateTable(table))
    cn = c.replace("CREATE TABLE " + origin_tname, "CREATE TABLE if not exists " + new_tname).replace('"', '`')
    db_conn = engine.connect()
    db_conn.execute(cn)
    db_conn.close()
    db_manager.flush_autobase(dbalias)


def mirror_tb_db2db(origin_tname, fromalias, new_tname, todbalias):
    """不同的数据库之间"""
    abobj = db_manager.get_autobase_obj(fromalias)
    engine = abobj['engine']
    autobase = abobj['autobase']
    table = autobase.metadata.tables[origin_tname]
    c = str(CreateTable(table))
    cn = c.replace("CREATE TABLE " + origin_tname, "CREATE TABLE if not exists " + new_tname).replace('"', '`')
    abobj_to = db_manager.get_autobase_obj(todbalias)
    engine = abobj_to['engine']
    autobase = abobj['autobase']
    db_conn = engine.connect()
    db_conn.execute(cn)
    db_conn.close()
    db_manager.flush_autobase(todbalias)





