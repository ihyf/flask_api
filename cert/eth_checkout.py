# coding:utf-8
import datetime
import functools
import hashlib
import json
from util.dbmanager import db_manager
from util.db_redis import redis_store
from util.mysql_db import Apps
from cert.eth_certs import EthCert
from util.check_fuc import bytes_str_to_dict
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def check_conn(request):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if "appid" not in kw or "data" not in kw or 'sign' not in kw:
                return {"code": "fail", "error": "data format error!"}
            # 哈希data数据，限制多次请求的问题
            sha1 = hashlib.sha1()
            sha1.update(kw['sign'].encode())
            this_hash = sha1.hexdigest()
            faster_rc = "rfaster_check_{0}".format(kw['appid'])
            try:
                if redis_store.exists(faster_rc) == 0:
                    redis_store.hset(faster_rc, this_hash, 1)
                    redis_store.expire(faster_rc, 60 * 60 * 12)
                else:
                    if redis_store.hexists(faster_rc, this_hash) is True:
                        return {"code": "fail", "error": "request faster"}
                redis_store.hset(faster_rc, this_hash, 1)
            except Exception as e:
                return {"code": "fail", "error": "redis server error!"}
            # 查询appid
            keys, ns, ip, srv = get_keys(kw['appid'])
            # 检查客户端IP地址
            if request.remote_addr not in ip:
                return {"code": "fail", "error": "illegal ip request"}
            # 检查客户端请求域名
            if ":" in request.host:
                real_host = ":".join(request.host.split(":")[:-1])
            else:
                real_host = request.host
            if real_host not in ns:
                return {"code": "fail", "error": "illegal domain request"}
            # 客户端
            ec_cli = EthCert()
            ec_cli.init_key(public_key_str=keys[0], private_key_str=keys[1])
            ec_cli.serialization()
            # 服务端
            ec_srv = EthCert()
            ec_srv.init_key(public_key_str=keys[2], private_key_str=keys[3])
            ec_srv.serialization()
            # 用自己的私钥解密
            decrypt_data = ec_srv.decrypt(kw['data'])
            if not decrypt_data:
                return {"code": "fail", "error": ec_srv.error}
            # 用app的公钥对解密数据进行验证签名
            if "sign" not in kw:
                return {"code": "fail", "error": "need sign data!"}
            if not ec_cli.verify(decrypt_data, kw['sign']):
                return {"code": "fail", "error": ec_cli.error}
            try:
                kw['decrypt'] = json.loads(decrypt_data.decode())
                # kw['decrypt'] = bytes_str_to_dict(decrypt_data)
            except Exception as e:
                return {"code": "fail", "error": f"need json or json error: {e}"}
            kw['verify'] = True
            kw['ec_cli'] = ec_cli
            kw['ec_srv'] = ec_srv
            return func(*args, **kw)
        return wrapper
    return decorator


def delete_checkout_redis(appid):
    checkout_keys = "checkout_{0}_keys".format(appid)
    checkout_ns = "checkout_{0}_ns".format(appid)
    checkout_ip = "checkout_{0}_ip".format(appid)
    checkout_srv = "checkout_{0}_srv".format(appid)
    redis_store.delete(checkout_keys, checkout_ns, checkout_ip, checkout_srv)


def get_keys(appid):
    checkout_keys = "checkout_{0}_keys".format(appid)
    checkout_ns = "checkout_{0}_ns".format(appid)
    checkout_ip = "checkout_{0}_ip".format(appid)
    checkout_srv = "checkout_{0}_srv".format(appid)
    checkout_update = "checkout_{0}_update".format(appid)
    if redis_store.exists(checkout_keys) == 0:
        session = db_manager.slave()
        try:
            app = session.query(Apps).filter(Apps.appid == appid).one()
            session.close()
        except MultipleResultsFound:
            return {"code": "fail", "error": "param error: fount many"}
        except NoResultFound:
            return {"code": "fail", "error": "param error: no found"}
        except Exception as e:
            return {"code": "fail", "error": f"param error: {e}"}
        keys = [
                app.cli_publickey,
                app.cli_privatekey,
                app.srv_publickey,
                app.srv_privatekey,
        ]
        redis_store.delete(checkout_keys, checkout_ns, checkout_ip, checkout_srv)
        redis_store.rpush(checkout_keys, keys[0], keys[1], keys[2], keys[3])
        ns = app.ns
        ip = app.ip
        srv = app.srv
        if ns:
            redis_store.rpush(checkout_ns, *ns)
        if ip:
            redis_store.rpush(checkout_ip, *ip)
        if srv:
            redis_store.rpush(checkout_srv, *srv)
        redis_store.set(checkout_update, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        keys = redis_store.lrange(checkout_keys, 0, 3)
        ns = redis_store.lrange(checkout_ns, 0, -1)
        ip = redis_store.lrange(checkout_ip, 0, -1)
        srv = redis_store.lrange(checkout_srv, 0, -1)
    return keys, ns, ip, srv



