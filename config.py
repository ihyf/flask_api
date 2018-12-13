# coding:utf-8
DEBUG = True
# SQLALCHEMY_BINDS = {
#     'users_write': 'mysql+pymysql://root:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.20/eth',
#     'users_readonly': 'mysql+pymysql://root:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.21/eth',
# }
# SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI_SETTINGS = {
    'master': [
        'mysql+pymysql://root:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.20/eth?charset=utf8'
    ],
    'slave': [
        'mysql+pymysql://root:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.21/eth?charset=utf8'
    ]
}

REDIS_URL = "redis://:@192.168.1.20:6379/0?charset=utf8&decode_responses=true"
# REDIS_URL = "unix://[:password]@/path/to/socket.sock?db=0"

