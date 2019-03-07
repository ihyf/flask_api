
*  SQLALCHEMY_DATABASE_URI_SETTINGS

``` python
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
```

数据库分库配置，Dict类型，对数据库进行分组，"default"是默认分组，每个组中包含'master'主数据库和'slave'从数据库，服务启动时，会连接好所有的数据库，要使用的时候，可以选择相应的连接对象，进行数据的操纵
* REDIS_URL

``` python
REDIS_URL = "redis://:@192.168.1.20:6379/0?charset=utf8&decode_responses=true"
```
redis的连接配置

* API_TRUST_DOMAIN

``` python
API_TRUST_DOMAIN = "dl.hyf.laotielian.cc"
```

设置API接口使用的域名，此域名进来的请求都视为合法正常的请求，在验证过程中得到信任

*  w3_url 
``` python
w3_url = "http://47.244.122.201:8101"
``` 
底层url
