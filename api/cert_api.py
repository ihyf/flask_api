# coding:utf-8
from my_dispatcher import api_add
from flask import request
from util.ext import db
from util.mysql_db import Apps
from cert.eth_certs import EthCert


@api_add
def token_test(*args, **kwargs):
    print(args, kwargs)
    return {"result": "ok"}


@api_add
def keys(*args, **kwargs):
    # ec = EthCert()
    username = kwargs.get('username', None)
    if username is None:
        return {"error": "username error!"}
    return {"result": "ok"}


@api_add
def bk_app_create(*args, **kwargs):
    """
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(200))
    app_desc = db.Column(db.String(200))
    app_ip = db.Column(db.JSON)
    app_ns = db.Column(db.JSON)
    app_publickey = db.Column(db.VARCHAR)
    app_privateKey = db.Column(db.VARCHAR)
    app_function = db.Column(db.JSON)
    app_status = db.Column(db.Integer)

    :param args:
    :param kwargs:
    :return:
    """
    app = Apps(
        app_name=kwargs.get("app_name", ""),
        app_desc=kwargs.get("app_desc", ""),
        app_ip=kwargs.get("app_ip", []),
        app_ns=kwargs.get("app_ns", []),
        app_publickey=kwargs.get("app_publickey", ""),
        app_privateKey=kwargs.get("app_privateKey", ""),
        app_function=kwargs.get("app_function", []),
        app_status=kwargs.get("app_status", 0)
    )
    db.session.add(app)
    db.session.commit()
    return {"result": "ok"}


@api_add
def bk_app_remove(*args, **kwargs):
    pass


@api_add
def bk_app_edit(*args, **kwargs):
    pass


@api_add
def bk_app_func(*args, **kwargs):
    pass


@api_add
def bk_api_status(*args, **kwargs):
    pass






