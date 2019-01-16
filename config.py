# coding:utf-8
DEBUG = True

SQLALCHEMY_DATABASE_URI_SETTINGS = {
    'master': [
        'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.241/eth?charset=utf8',
    ],
    'slave': [
        'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.21/eth?charset=utf8',
        'mysql+pymysql://eth:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.22/eth?charset=utf8',
    ]
}
# 获取子合约路径
contract_url = "http://192.168.1.11:82/upload/"

REDIS_URL = "redis://:@192.168.1.20:6379/0?charset=utf8&decode_responses=true"

w3_url = "http://192.168.1.33:8101"
# w3_url = "http://127.0.0.1:8545"

