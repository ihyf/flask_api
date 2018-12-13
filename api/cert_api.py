# coding:utf-8
import json
from my_dispatcher import api_add
from util.db_redis import redis_store
from util.dbmanager import db_manager
from util.mysql_db import Apps
from cert.eth_checkout import check_conn
from flask import request
from cert.eth_checkout import delete_checkout_redis
from cert.eth_certs import EthCert


@api_add
@check_conn(request)
def token_test(*args, **kwargs):
    print(args, kwargs)
    return {"result": "ok"}


@api_add
def keys(*args, **kwargs):
    import hashlib
    # ec = EthCert()
    sha1 = hashlib.sha1()
    sha1.update(b"XXXXXXXXXXXXXXXXXXXX")
    hash = sha1.hexdigest()
    print(redis_store.lindex("Joy", hash))
    print(redis_store.lpush("Joy", sha1.hexdigest()))
    redis_store.set('potato', 'Not Set')
    username = kwargs.get('username', None)
    if username is None:
        return {"error": "username error!"}
    return {"result": "ok"}


@api_add
@check_conn(request)
def bk_create(*args, **kwargs):
    appid = kwargs.get("appid", "")
    if not appid:
        return {"code": "fail", "error": "appid error"}
    session = db_manager.master()
    appexist = session.query(Apps).filter(Apps.appid == appid).all()
    if appexist:
        return {"code": "fail", "error": "appid exist"}
    desc = kwargs.get("desc", "")
    ip = kwargs.get("ip", [])
    ns = kwargs.get("ns", [])
    srv = kwargs.get("srv", [])
    status = kwargs.get("status", 0)
    ec = EthCert()
    ec.generate(4096)
    cli_privatekey = ec.private_key_str
    cli_publickey = ec.public_key_str
    ec.generate(4096)
    srv_privatekey = ec.private_key_str
    srv_publickey = ec.public_key_str
    app = Apps(
        appid=appid,
        desc=desc,
        ip=ip,
        ns=ns,
        cli_publickey=cli_publickey,
        cli_privatekey=cli_privatekey,
        srv_publickey=srv_publickey,
        srv_privatekey=srv_privatekey,
        srv=srv,
        status=status
    )
    session.add(app)
    try:
        session.commit()
    except Exception as e:
        session.close()
        return {"code": "fail", "error": f"{e.args}"}
    return {"code": "success", "result": {
        "appid": appid,
        "cli_publickey": str(cli_publickey),
        "cli_privatekey": str(cli_privatekey),
        "srv_publickey": str(srv_publickey),
    }}


@api_add
@check_conn(request)
def bk_remove(*args, **kwargs):
    data = kwargs['decrypt']['params']
    if "appid" not in data:
        return {"code": "fail", "error": "miss appid"}
    session = db_manager.master()
    session.query(Apps).filter(Apps.appid == data['appid']).delete()
    session.commit()
    session.close()
    delete_checkout_redis(data['appid'])
    return {"code": "success", "result": {"appid": data['appid']}}


@api_add
def bk_edit(*args, **kwargs):
    pass


@api_add
def bk_func(*args, **kwargs):
    pass


@api_add
def bk_api_status(*args, **kwargs):
    pass






