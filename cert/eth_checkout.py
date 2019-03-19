# coding:utf-8
import datetime
import functools
import hashlib
import IPy
import re
import json
from util.dbmanager import db_manager
from util.db_redis import redis_store
from util.mysql_db import Apps
from cert.eth_certs import EthCert
from config import API_TRUST_DOMAIN
from util.errno import err_format
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def check_conn(request):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if "appid" not in kw or "data" not in kw or 'sign' not in kw:
                return err_format(0, -10107)
            # 哈希data数据，限制多次请求的问题
            sha1 = hashlib.sha1()
            try:
                sha1.update(kw['sign'].encode())
            except:
                return err_format(0, -10103, 'sign')
            this_hash = sha1.hexdigest()
            faster_rc = "checkout_{0}_rfaster".format(kw['appid'])
            try:
                if redis_store.exists(faster_rc) == 0:
                    redis_store.hset(faster_rc, this_hash, 1)
                    redis_store.expire(faster_rc, 60 * 60 * 12)
                else:
                    if redis_store.hexists(faster_rc, this_hash) is True:
                        return err_format(0, -10401)
                redis_store.hset(faster_rc, this_hash, 1)
            except Exception as e:
                return err_format(0, -10301)
            # 查询appid
            keystatus, res_kes = get_keys(kw['appid'])
            if keystatus is not True:
                return res_kes
            # status
            # 0启用  1停用  2未授权
            if res_kes['status'] != 0:
                return err_format(0, -10411)
            # srv
            if request.is_json is False:
                # 要求Content-Type为：application/json
                return err_format(0, -10420)
            if "method" not in request.json or not request.json['method']:
                return err_format(0, -10421)
            if request.json['method'] not in res_kes["srv"]:
                return err_format(0, -10422)
            # 检查客户端IP地址
            try:
                for ip_net in res_kes["ip"]:
                    if request.remote_addr in IPy.IP(ip_net):
                        break
                else:
                    return err_format(0, -10423, request.remote_addr)
            except Exception as e:
                return err_format(0, -10424)

            # 检查客户端请求域名
            if ":" in request.host:
                if request.host[-1] == ']':
                    real_host = request.host
                else:
                    real_host = request.host[:request.host.rfind(":")]
            else:
                real_host = request.host
            if real_host != API_TRUST_DOMAIN:
                # 可能会出现域名替换的问题
                ns_re = '(' + '|'.join(res_kes["ns"]) + ')$'
                ns_re = ns_re.replace(".", "\.").replace("*", ".*?").replace('[', '\[').replace(']', '\]')
                try:
                    if not re.match(ns_re, real_host, re.I):
                        return err_format(0, -10425, real_host)
                except Exception as e:
                    return err_format(0, -10426)
            # 客户端
            ec_cli = EthCert()
            ec_cli.init_key(public_key_str=res_kes["keys"][0], private_key_str=res_kes["keys"][1])
            ec_cli.serialization()
            # 服务端
            ec_srv = EthCert()
            ec_srv.init_key(public_key_str=res_kes["keys"][2], private_key_str=res_kes["keys"][3])
            ec_srv.serialization()
            if kw.get("no_decrypt", None) != "no_decrypt":
                # 用自己的私钥解密
                decrypt_data = ec_srv.decrypt(kw['data'])
                if not decrypt_data:
                    return err_format(0, -10501, ec_srv.error)
                # 用app的公钥对解密数据进行验证签名
                if "sign" not in kw:
                    return err_format(0, -10105, 'sign')
                if not ec_cli.verify(decrypt_data, kw['sign']):
                    return err_format(0, -10502)
                try:
                    kw['decrypt'] = json.loads(decrypt_data.decode())
                except Exception as e:
                    return err_format(0, -10004)
            else:
                # 用app的公钥对解密数据进行验证签名
                if "sign" not in kw:
                    return err_format(0, -10105, 'sign')
                if not ec_cli.verify(kw["data"], kw['sign']):
                    return err_format(0, -10502)
            kw['verify'] = True
            kw['ec_cli'] = ec_cli
            kw['ec_srv'] = ec_srv
            kw['callback_url'] = res_kes['callback_url']
            kw["master_contract_address"] = res_kes["master_contract_address"]
            kw["status"] = res_kes["status"]
            return func(*args, **kw)
        return wrapper
    return decorator


def delete_checkout_redis(appid):
    pkeys = product_keys(appid)
    # redis_store.delete(*pkeys.keys())
    redis_store.delete(
        pkeys["checkout_keys"],
        pkeys["checkout_ns"],
        pkeys["checkout_ip"],
        pkeys["checkout_srv"],
        pkeys["checkout_update"],
        pkeys["checkout_mc_address"],
        pkeys["checkout_wallet_addr"],
        pkeys["checkout_callback_url"],
        pkeys["checkout_status"],
    )


def product_keys(appid):
    pkeys = {
        "checkout_keys": "checkout_{0}_keys".format(appid),
        "checkout_ns": "checkout_{0}_ns".format(appid),
        "checkout_ip": "checkout_{0}_ip".format(appid),
        "checkout_srv": "checkout_{0}_srv".format(appid),
        # "checkout_rfaster": "checkout_{0}_rfaster".format(appid),
        "checkout_update": "checkout_{0}_update".format(appid),
        "checkout_mc_address": "checkout_{0}_mcaddress".format(appid),
        "checkout_wallet_addr": "checkout_{0}_waaddress".format(appid),
        "checkout_callback_url": "checkout_{0}_callback".format(appid),
        "checkout_status": "checkout_{0}_status".format(appid),
    }
    return pkeys


def get_keys(appid):
    pkeys = product_keys(appid)
    res_kes = {
        "keys": None,
        "ns": None,
        "ip": None,
        "srv": None,
        "master_contract_address": None,
        "wallet": None,
        "callback_url": None,
        "status": None,
    }
    if redis_store.exists(pkeys["checkout_keys"]) == 0:
        session = db_manager.slave()
        try:
            app = session.query(Apps).filter(Apps.appid == appid).one()
            session.close()
        except MultipleResultsFound:
            return err_format(0, -10202, appid)
        except NoResultFound:
            return err_format(0, -10203, appid)
        except Exception as e:
            return err_format(0, -10201, appid)
        res_kes["keys"] = [
                app.cli_publickey,
                app.cli_privatekey,
                app.srv_publickey,
                app.srv_privatekey,
        ]
        delete_checkout_redis(appid)
        redis_store.rpush(
            pkeys["checkout_keys"],
            res_kes["keys"][0],
            res_kes["keys"][1],
            res_kes["keys"][2],
            res_kes["keys"][3]
        )
        res_kes["ns"] = app.ns
        res_kes["ip"] = app.ip
        res_kes["srv"] = app.srv
        res_kes["master_contract_address"] = app.master_contract_address
        res_kes["wallet"] = app.wallet
        res_kes["callback_url"] = app.callback_url
        res_kes["status"] = app.status
        if res_kes["ns"]:
            redis_store.rpush(pkeys["checkout_ns"], *res_kes["ns"])
        if res_kes["ip"]:
            redis_store.rpush(pkeys["checkout_ip"], *res_kes["ip"])
        if res_kes["srv"]:
            redis_store.rpush(pkeys["checkout_srv"], *res_kes["srv"])
        if res_kes["master_contract_address"]:
            redis_store.rpush(pkeys["checkout_mc_address"], *res_kes["master_contract_address"])
        if res_kes["wallet"]:
            redis_store.set(pkeys["checkout_wallet_addr"], res_kes["wallet"])
        if res_kes["callback_url"]:
            redis_store.set(pkeys["checkout_callback_url"], res_kes["callback_url"])
        redis_store.set(pkeys["checkout_status"], res_kes["status"])
        redis_store.set(pkeys["checkout_update"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        res_kes["keys"] = redis_store.lrange(pkeys["checkout_keys"], 0, 3)
        res_kes["ns"] = redis_store.lrange(pkeys["checkout_ns"], 0, -1)
        res_kes["ip"] = redis_store.lrange(pkeys["checkout_ip"], 0, -1)
        res_kes["srv"] = redis_store.lrange(pkeys["checkout_srv"], 0, -1)
        res_kes["master_contract_address"] = redis_store.lrange(pkeys["checkout_mc_address"], 0, -1)
        res_kes["wallet"] = redis_store.get(pkeys["checkout_wallet_addr"])
        res_kes["callback_url"] = redis_store.get(pkeys["checkout_callback_url"])
        res_kes["status"] = int(redis_store.get(pkeys["checkout_status"]))
    return True, res_kes



