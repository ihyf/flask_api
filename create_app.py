# coding:utf-8
from flask import Flask
from flask_cors import CORS
import config
from api import *


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api.as_blueprint(url='/api'))
    # 跨域请求
    CORS(app, supports_credentials=True)
    app.config['DEBUG'] = config.DEBUG
    # app.config['SQLALCHEMY_BINDS'] = config.SQLALCHEMY_BINDS
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI_SETTINGS'] = config.SQLALCHEMY_DATABASE_URI_SETTINGS
    app.config['REDIS_URL'] = config.REDIS_URL
    return app
