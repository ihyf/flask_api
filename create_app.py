# coding:utf-8
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import config
from api import *


def create_app():
    global db
    app = Flask(__name__)
    app.register_blueprint(api.as_blueprint(url='/api'))
    # 跨域请求
    CORS(app, supports_credentials=True)
    app.config['DEBUG'] = config.DEBUG
    app.config['SQLALCHEMY_BINDS'] = config.SQLALCHEMY_BINDS
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    return app
