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

    return app
