# coding:utf-8
import json
import IPy
from my_dispatcher import api_add
from util.db_redis import redis_store
from util.log import rlog
from util.dbmanager import db_manager
from util.mysql_db import Apps
from cert.eth_checkout import check_conn
from flask import request
from cert.eth_checkout import delete_checkout_redis
from cert.eth_certs import EthCert
from util.errno import err_format
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
        return err_format(1, -10107)
    session = db_manager.master()
    appexist = session.query(Apps).filter(Apps.appid == origin['appid']).all()
    if appexist:
        return err_format(1, -10601)
    desc = origin.get("desc", "")
    ip = origin.get("ip")
    if not isinstance(ip, list):
        return err_format(1, -10104, "ip")
    try:
        for ipnet in ip:
            IPy.IP(ipnet)
    except Exception as e:
        return err_format(1, -10003, "ip")
    ns = origin.get("ns")
    if not isinstance(ns, list):
        return err_format(1, -10104)
    srv = origin.get("srv", [])
    if not isinstance(srv, list):
        return err_format(1, -10104, "ns")
    master_contract_address = origin.get("master_contract_address", [])
    if not isinstance(master_contract_address, list):
        return err_format(1, -10104, 'master_contract_address')
    wallet = origin.get("wallet", None)
    if wallet is None:
        return err_format(1, -10105, 'wallet')
    callback_url = origin.get("callback_url", None)
    status = origin.get("status")
    if not isinstance(status, int):
        return err_format(1, -10104, 'status')
    create_cli_keys = origin.get("create_cli_keys", True)
    create_srv_keys = origin.get("create_srv_keys", True)
    ec = EthCert()
    if create_cli_keys is True:
        cli_keys_length = origin.get("cli_keys_length", 4096)
        if cli_keys_length not in [1024, 2048, 4096]:
            return err_format(1, -10504, 'cli_keys_length')
        ec.generate(cli_keys_length)
        cli_privatekey = ec.get_privatekey()
        cli_publickey = ec.get_publickey()
    else:
        if "cli_keys" not in origin:
            return err_format(1, -10105, 'cli_keys')
        if "cli_publickey" not in origin['cli_keys']:   # 上传了客户端的公钥
            return err_format(1, -10105, 'cli_publickey')
        cli_publickey = origin['cli_keys']['cli_publickey']
        if not cli_publickey:
            return err_format(1, -10103, 'cli_publickey')
        if "cli_privatekey" in origin['cli_keys']:
            cli_privatekey = origin['cli_keys']['cli_privatekey']
        else:
            cli_privatekey = None
        ec.init_key(private_key_str=cli_privatekey, public_key_str=cli_publickey)
        if ec.serialization() is False:
            return err_format(1, -10505)
    if create_srv_keys is True:
        srv_keys_length = origin.get("srv_keys_length", 4096)
        if srv_keys_length not in [1024, 2048, 4096]:
            return err_format(1, -10504, 'srv_keys_length')
        ec.generate()
        srv_privatekey = ec.get_privatekey()
        srv_publickey = ec.get_publickey()
    else:
        if "srv_keys" not in origin:
            return err_format(1, -10105, 'srv_keys')
        if "srv_privatekey" not in origin['srv_keys']:  # 上传了服务端私钥
            return err_format(1, -10105, 'srv_privatekey')
        srv_privatekey = origin['srv_keys']['srv_privatekey']
        if not srv_privatekey:
            return err_format(1, -10103, 'srv_privatekey')
        if "srv_publickey" in origin['srv_keys']:
            srv_publickey = origin['srv_keys']['srv_publickey']
        else:
            srv_publickey = None
        ec.init_key(private_key_str=srv_privatekey, public_key_str=srv_publickey)
        if ec.serialization() is False:
            return err_format(1, -10505)
    app = Apps(
        appid=origin['appid'],
        parent_appid=kwargs['appid'],
        desc=desc,
        ip=ip,
        ns=ns,
        cli_publickey=cli_publickey,
        cli_privatekey=cli_privatekey,
        srv_publickey=srv_publickey,
        srv_privatekey=srv_privatekey,
        srv=srv,
        master_contract_address=master_contract_address,
        wallet=wallet,
        callback_url=callback_url,
        status=status
    )
    session.add(app)
    try:
        session.commit()
    except Exception as e:
        session.close()
        return err_format(1, -10201, e.args)
    result = {
        "appid": origin['appid'],
        "cli_privatekey": cli_privatekey,
        "srv_publickey": srv_publickey,
    }
    if "r_cli_publickey" in origin and origin['r_cli_publickey'] is True:
        result['cli_publickey'] = cli_publickey
    if "r_srv_privatekey" in origin and origin['r_srv_privatekey'] is True:
        result['srv_privatekey'] = srv_privatekey
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
        return err_format(1, -10101, 'appid')
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
        return err_format(1, -10101, 'appid')
    session = db_manager.master()
    try:
        app = session.query(Apps).filter(Apps.appid == origin['appid']).one()
    except MultipleResultsFound:
        return err_format(1, -10202, origin['appid'])
    except NoResultFound:
        return err_format(1, -10203, origin['appid'])
    except Exception as e:
        return err_format(1, -10201, origin['appid'])
    for key in origin.keys():
        if check_attr(key) is False:
            if key == "time":
                continue
            return err_format(1, -10204, key)
    if 'desc' in origin:
        app.desc = origin['desc']
    if 'ip' in origin and isinstance(origin['ip'], list):
        app.ip = origin['ip']
    if 'ns' in origin and isinstance(origin['ns'], list):
        app.ns = origin['ns']
    if 'master_contract_address' in origin and isinstance(origin['master_contract_address'], list):
        app.master_contract_address = origin['master_contract_address']
    if 'wallet' in origin:
        app.wallet = origin['wallet']
    if 'callback_url' in origin:
        app.callback_url = origin['callback_url']
    ec = EthCert()
    if 'cli_publickey' in origin and origin['cli_publickey']:
        ec.init_key(public_key_str=origin['cli_publickey'])
        if ec.serialization() is False:
            return err_format(1, -10505, 'cli_publickey')
        app.cli_publickey = origin['cli_publickey']
    if 'cli_privatekey' in origin and origin['cli_privatekey']:
        ec.init_key(private_key_str=origin['cli_privatekey'])
        if ec.serialization() is False:
            return err_format(1, -10505, 'cli_privatekey')
        app.cli_privatekey = origin['cli_privatekey']
    if 'srv_publickey' in origin and origin['srv_publickey']:
        ec.init_key(public_key_str=origin['srv_publickey'])
        if ec.serialization() is False:
            return err_format(1, -10505, 'srv_publickey')
        app.srv_publickey = origin['srv_publickey']
    if 'srv_privatekey' in origin and origin['srv_privatekey']:
        ec.init_key(private_key_str=origin['srv_privatekey'])
        if ec.serialization() is False:
            return err_format(1, -10505, 'srv_privatekey')
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
def bk_reset(*args, **kwargs):
    origin = kwargs['decrypt']
    if "appid" not in origin or not origin['appid'] and isinstance(origin['appid'], str):
        return err_format(1, -10101, 'appid')
    session = db_manager.master()
    try:
        app = session.query(Apps).filter(Apps.appid == origin['appid']).one()
        session.close()
    except MultipleResultsFound:
        return err_format(1, -10202, origin['appid'])
    except NoResultFound:
        return err_format(1, -10203, origin['appid'])
    except Exception as e:
        return err_format(1, -10201, origin['appid'])
    reset_cli_keys = origin.get("reset_cli_keys", False)
    reset_srv_keys = origin.get("reset_srv_keys", False)
    if reset_cli_keys is not True and reset_srv_keys is not True:
        return err_format(1, -10427)
    cli_keys_length = origin.get("cli_keys_length", 4096)
    if cli_keys_length not in [1024, 2048, 4096]:
        return err_format(1, -10504, 'cli_keys_length')
    srv_keys_length = origin.get("srv_keys_length", 4096)
    if srv_keys_length not in [1024, 2048, 4096]:
        return err_format(1, -10504, 'srv_keys_length')
    ec = EthCert()
    if reset_cli_keys is True:
        ec.generate(cli_keys_length)
        app.cli_privatekey = ec.get_privatekey()
        app.cli_publickey = ec.get_publickey()
    if reset_srv_keys is True:
        ec.generate(srv_keys_length)
        app.srv_privatekey = ec.get_privatekey()
        app.srv_publickey = ec.get_publickey()
    session.commit()
    session.close()
    delete_checkout_redis(origin['appid'])
    result = {
        "appid": origin['appid'],
        "cli_privatekey": app.cli_privatekey,
        "srv_publickey": app.srv_publickey,
    }
    if "r_cli_publickey" in origin and origin['r_cli_publickey'] is True:
        result['cli_publickey'] = app.cli_publickey
    if "r_srv_privatekey" in origin and origin['r_srv_privatekey'] is True:
        result['srv_privatekey'] = app.srv_privatekey
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
        return err_format(1, -10101, 'appid')
    if "field" not in origin or not isinstance(origin['field'], list):
        return err_format(1, -10107, 'field')
    session = db_manager.slave()
    try:
        app = session.query(Apps).filter(Apps.appid == origin['appid']).one()
        session.close()
    except MultipleResultsFound:
        return err_format(1, -10202, origin['appid'])
    except NoResultFound:
        return err_format(1, -10203, origin['appid'])
    except Exception as e:
        return err_format(1, -10201, origin['appid'])
    result = {"appid": origin['appid']}
    for key in origin['field']:
        if check_attr(key) is False:
            if key == "time":
                continue
            return err_format(1, -10204, key)
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
def bk_lists(*args, **kwargs):
    origin = kwargs['decrypt']
    parent_appid = origin.get("parent_appid", None)
    session = db_manager.slave()
    try:
        if isinstance(parent_appid, str):
            apps = session.query(Apps).filter(Apps.parent_appid == parent_appid)
        else:
            apps = session.query(Apps)
        session.close()
    except Exception as e:
        return err_format(1, -10201)
    r_apps = []
    for app in apps:
        result = {
            "appid": app.appid,
            "parent_appid": app.parent_appid,
            "desc": app.desc,
        }
        r_apps.append(result)
    result_str = json.dumps(r_apps, ensure_ascii=False)
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
        return err_format(1, -10101, 'appid')
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
        return err_format(1, -10101, 'appid')
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



