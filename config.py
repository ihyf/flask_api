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

REDIS_URL = "redis://:@192.168.1.20:6379/0?charset=utf8&decode_responses=true"

