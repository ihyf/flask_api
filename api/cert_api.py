# coding:utf-8
import json
import IPy
from my_dispatcher import api_add
from util.db_redis import redis_store
from util.dbmanager import db_manager
from util.mysql_db import Apps
from cert.eth_checkout import check_conn
from flask import request
from cert.eth_checkout import delete_checkout_redis
from cert.eth_certs import EthCert
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def check_attr(name):
    try:
        if isinstance(eval(f"Apps.{name}"), InstrumentedAttribute):
            return True
        else:
            return False
    except:
        return False


@api_add
@check_conn(request)
def bk_create(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return {"code": "fail", "error": "appid error"}
    session = db_manager.master()
    appexist = session.query(Apps).filter(Apps.appid == origin['appid']).all()
    if appexist:
        return {"code": "fail", "error": "appid exist"}
    desc = origin.get("desc", "")
    ip = origin.get("ip")
    if not isinstance(ip, list):
        return {"code": "fail", "error": "ip filed error"}
    try:
        for ipnet in ip:
            IPy.IP(ipnet)
    except Exception as e:
        return {"code": "fail", "error": "ip filed error"}
    ns = origin.get("ns")
    if not isinstance(ns, list):
        return {"code": "fail", "error": "ns filed error"}
    srv = origin.get("srv", [])
    if not isinstance(srv, list):
        return {"code": "fail", "error": "srv filed error"}
    status = origin.get("status")
    if not isinstance(status, int):
        return {"code": "fail", "error": "status filed error"}
    create_cli_keys = origin.get("create_cli_keys", True)
    create_srv_keys = origin.get("create_srv_keys", True)
    ec = EthCert()
    if create_cli_keys is True:
        cli_keys_length = origin.get("cli_keys_length", 4096)
        if cli_keys_length not in [1024, 2048, 4096]:
            return {"code": "fail", "error": "cli_keys_length must in [1024, 2048, 4096]"}
        ec.generate(cli_keys_length)
        cli_privatekey = ec.get_privatekey()
        cli_publickey = ec.get_publickey()
    else:
        if "cli_keys" not in origin:
            return {"code": "fail", "error": "miss cli_keys filed"}
        if "cli_publickey" not in origin['cli_keys']:   # 上传了客户端的公钥
            return {"code": "fail", "error": "cli_keys error"}
        cli_publickey = origin['cli_keys']['cli_publickey']
        if not cli_publickey:
            return {"code": "fail", "error": "cli_keys error"}
        if "cli_privatekey" in origin['cli_keys']:
            cli_privatekey = origin['cli_keys']['cli_privatekey']
        else:
            cli_privatekey = None
        ec.init_key(private_key_str=cli_privatekey, public_key_str=cli_publickey)
        if ec.serialization() is False:
            return {"code": "fail", "error": "cli_keys error, serialization fail"}
    if create_srv_keys is True:
        srv_keys_length = origin.get("srv_keys_length", 4096)
        if srv_keys_length not in [1024, 2048, 4096]:
            return {"code": "fail", "error": "srv_keys_length must in [1024, 2048, 4096]"}
        ec.generate()
        srv_privatekey = ec.get_privatekey()
        srv_publickey = ec.get_publickey()
    else:
        if "srv_keys" not in origin:
            return {"code": "fail", "error": "miss srv_keys filed"}
        if "srv_privatekey" not in origin['srv_keys']:  # 上传了服务端私钥
            return {"code": "fail", "error": "srv_keys error"}
        srv_privatekey = origin['srv_keys']['srv_privatekey']
        if not srv_privatekey:
            return {"code": "fail", "error": "srv_keys error"}
        if "srv_publickey" in origin['srv_keys']:
            srv_publickey = origin['srv_keys']['srv_publickey']
        else:
            srv_publickey = None
        ec.init_key(private_key_str=srv_privatekey, public_key_str=srv_publickey)
        if ec.serialization() is False:
            return {"code": "fail", "error": "srv_keys error, serialization fail"}
    app = Apps(
        appid=origin['appid'],
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
    result = {
        "appid": origin['appid'],
        "cli_privatekey": cli_privatekey,
        "srv_publickey": srv_publickey,
    }
    if "r_cli_publickey" in origin and origin['r_cli_publickey'] is True:
        result['cli_publickey'] = cli_publickey
    if "r_srv_privatekey" in origin and origin['r_srv_privatekey'] is True:
        result['r_srv_privatekey'] = srv_privatekey
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response


@api_add
@check_conn(request)
def bk_remove(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return {"code": "fail", "error": "appid error"}
    session = db_manager.master()
    session.query(Apps).filter(Apps.appid == origin['appid']).delete()
    session.commit()
    session.close()
    delete_checkout_redis(origin['appid'])
    result = {"appid": origin['appid']}
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response


@api_add
@check_conn(request)
def bk_edit(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return {"code": "fail", "error": "appid error"}
    session = db_manager.master()
    try:
        app = session.query(Apps).filter(Apps.appid == origin['appid']).one()
    except MultipleResultsFound:
        return {"code": "fail", "error": "appid fount many"}
    except NoResultFound:
        return {"code": "fail", "error": "appid no found"}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}
    for key in origin.keys():
        if check_attr(key) is False:
            if key == "time":
                continue
            return {"code": "fail", "error": f"filed {key} error"}
    if 'desc' in origin:
        app.desc = origin['desc']
    if 'ip' in origin and isinstance(origin['ip'], list):
        app.ip = origin['ip']
    if 'ns' in origin and isinstance(origin['ns'], list):
        app.ns = origin['ns']
    ec = EthCert()
    if 'cli_publickey' in origin and origin['cli_publickey']:
        ec.init_key(public_key_str=origin['cli_publickey'])
        if ec.serialization() is False:
            return {"code": "fail", "error": f"cli_publickey: {ec.error}"}
        app.cli_publickey = origin['cli_publickey']
    if 'cli_privatekey' in origin and origin['cli_privatekey']:
        ec.init_key(private_key_str=origin['cli_privatekey'])
        if ec.serialization() is False:
            return {"code": "fail", "error": f"cli_privatekey: {ec.error}"}
        app.cli_privatekey = origin['cli_privatekey']
    if 'srv_publickey' in origin and origin['srv_publickey']:
        ec.init_key(public_key_str=origin['srv_publickey'])
        if ec.serialization() is False:
            return {"code": "fail", "error": f"srv_publickey: {ec.error}"}
        app.srv_publickey = origin['srv_publickey']
    if 'srv_privatekey' in origin and origin['srv_privatekey']:
        ec.init_key(private_key_str=origin['srv_privatekey'])
        if ec.serialization() is False:
            return {"code": "fail", "error": f"srv_privatekey: {ec.error}"}
        app.srv_privatekey = origin['srv_privatekey']
    if 'srv' in origin and isinstance(origin['srv'], list):
        app.srv = origin['srv']
    if 'status' in origin and isinstance(origin['status'], int):
        app.status = origin['status']
    session.commit()
    session.close()
    delete_checkout_redis(origin['appid'])
    result = {"appid": origin['appid']}
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response


@api_add
@check_conn(request)
def bk_info(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return {"code": "fail", "error": "appid error"}
    if "field" not in origin or not isinstance(origin['field'], list):
        return {"code": "fail", "error": "field error"}
    session = db_manager.master()
    try:
        app = session.query(Apps).filter(Apps.appid == origin['appid']).one()
        session.close()
    except MultipleResultsFound:
        return {"code": "fail", "error": "appid fount many"}
    except NoResultFound:
        return {"code": "fail", "error": "appid no found"}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}
    result = {"appid": origin['appid']}
    for key in origin['field']:
        if check_attr(key) is False:
            if key == "time":
                continue
            return {"code": "fail", "error": f"filed {key} error"}
        else:
            result[key] = eval(f"app.{key}")
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response

@api_add
@check_conn(request)
def bk_status(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appids" not in origin or not origin['appids'] and isinstance(origin['appids'], list):
        return {"code": "fail", "error": "appids error"}
    """
    ####
    还没有实现
    ####
    """
    result = {"appids": origin['appids'], "mess": "还没有实现"}
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response


@api_add
@check_conn(request)
def bk_cleanup(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return {"code": "fail", "error": "appid error"}
    delete_checkout_redis(origin['appid'])
    result = {"appid": origin['appid']}
    result_str = json.dumps(result, ensure_ascii=False)
    sign = kwargs['ec_srv'].sign(result_str)
    encrypt = kwargs['ec_cli'].encrypt(result_str)
    response = {
        "code": "success",
        "sign": sign.decode(),
        "data": encrypt.decode()
    }
    return response



