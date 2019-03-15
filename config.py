# coding:utf-8
DEBUG = True

SQLALCHEMY_DATABASE_URI_SETTINGS = {
    "default": {
        'master': [
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.241/eth?charset=utf8',
        ],
        'slave': [
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.21/eth?charset=utf8',
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.22/eth?charset=utf8',
        ]
    },
    # "other": {
    #     'master': [],
    #     'slave': []
    # }
}
# 获取子合约路径
contract_url = "http://192.168.1.11:82/upload/"

REDIS_URL = "redis://:@192.168.1.20:6379/0?charset=utf8&decode_responses=true"

w3_url_neiwang = "http://192.168.1.14:8101"
# w3_url = "http://47.244.122.201:8101"
w3_url = "http://47.52.166.23:8101"

# 服务器上用
SQLALCHEMY_DATABASE_URI_SETTINGS_bak = {
    "default": {
        'master': [
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@172.17.0.1/eth?charset=utf8',
        ],
        'slave': [
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@172.17.0.1/eth?charset=utf8',
            'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@172.17.0.1/eth?charset=utf8',
        ]
    },
    # "other": {
    #     'master': [],
    #     'slave': []
    # }
}

REDIS_URL_bak = "redis://:@172.17.0.1:6379/0?charset=utf8&decode_responses=true"

API_TRUST_DOMAIN = "dl.hyf.laotielian.cc"


