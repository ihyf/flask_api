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
# w3_url = "http://47.52.166.23:8101"
w3_url = "http://86.93.28.232:30303"

# 服务器上用
SQLALCHEMY_DATABASE_URI_SETTINGS_bak = {
    "default": {
        'master': [
            'mysql+pymysql://root:reinforcement_1000more_needed@47.244.167.66/eth?charset=utf8',
        ],
        'slave': [
            'mysql+pymysql://root:reinforcement_1000more_needed@47.244.167.66/eth?charset=utf8',
            'mysql+pymysql://root:reinforcement_1000more_needed@47.244.167.66/eth?charset=utf8',
        ]
    },
    # "other": {
    #     'master': [],
    #     'slave': []
    # }
}

REDIS_URL_bak = "redis://:@47.244.167.66:6379/0?charset=utf8&decode_responses=true"

API_TRUST_DOMAIN = "dl.hyf.laotielian.cc"

to_100_keystore = {"address":"b177b5a38825b9dff97cf9192b86a7bef60ea644","crypto":{"cipher":"aes-128-ctr","cipherparams":{"iv":"dafff80feb2f814ae098cdfb2f64166f"},"ciphertext":"a31ea99326f4ddaf0057c5b7a67cb9923c71cd66e2fc50b35d9b82fdb7c9cce2","kdf":"pbkdf2","kdfparams":{"c":1000000,"dklen":32,"prf":"hmac-sha256","salt":"78ee28bb6de6dc616fcf636394da1026"},"mac":"ff5fc3ed75d1a72dac8fd4fbafdf3714bf0d91c3350f16c3d5477464794ea380"},"id":"1ae741d2-10a2-42e1-8ecd-e19844937a9d","version":3}


