# 钱包-创建账户接口
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "create_account",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "pwd": "密码",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后
```json
{
    "method": "create_account",
    "params": {
        "appid": "hyf_app",
        "sign": "签名",
        "data": "加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 下行
加密前
```json
{
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "mnemonic": "park impose pluck solid vague deer sort vessel regular aisle subject slender",
            "address": "0xC1F99048c0F3ea31E28dFF520b04f4774DA5b454",
            "keystore": {
                "address": "c1f99048c0f3ea31e28dff520b04f4774da5b454",
                "crypto": {
                    "cipher": "aes-128-ctr",
                    "cipherparams": {
                        "iv": "bdc5f1d7fccf11f5ebe1e6307f14b086"
                    },
                    "ciphertext": "ef83489a9c6e56407292ddf7326140a53514d0fd8cfd6c4fce6a82fb390ae17a",
                    "kdf": "pbkdf2",
                    "kdfparams": {
                        "c": 1000000,
                        "dklen": 32,
                        "prf": "hmac-sha256",
                        "salt": "a7c865cfff5dc03923dc086dd6394932"
                    },
                    "mac": "33350d3a24e385db092fa351201498733ad2ef7d7707b5fe2d90834f17b76e80"
                },
                "id": "8105bff0-3e59-43bc-ab39-ba5c63ab3e0c",
                "version": 3
            },
            "private_key": "93dba7452826bf91fd889f97ff26c127ba8a697854ddf1dded97ce9adec7342c"
        }
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
加密后
```json
{
    "result": {
        "code": "success",
        "sign": "50d3a24e385db092fa",
        "data": "50d3a24e385db092fa50d3a24e385db092fa"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
```
error
{"result": {"code": "fail", "error": "no password"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-获取余额
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "get_balance",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后
```json
{
    "method": "get_balance",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 下行
加密前
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "eth_balance": "100"
        }
    }
}
```
加密后
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code":"fail", "error": "no address"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-发送裸交易
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "send_transaction",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "to_address": "2c7fbb570d42f433a2b7c788b531c2b51633150f",
            "value": 10,
            "gas_limit": 200000,
            "gas_price": 3000,
            "pwd": "hyf",
            "keystore": {},
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后
```json
{
    "method": "send_transaction",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "tx_hash": "xxxxxx"
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code": "fail", "error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-导入私钥创建账户
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "import_private_key",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "private_key": "",
            "pwd": "",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后
```json
{
    "method": "import_private_key",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data":{
            "address": "xxxx",
            "keystore": {}
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code":"fail", "error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-导入Keystore创建账户
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "import_keystore",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "keystore": {},
            "pwd": "密码",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后
```json
{
    "method": "import_keystore",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
            "keystore": {
                "address": "bedc1e0341a85a571243990d7bc057a554966ce5",
                "crypto": {
                    "cipher": "aes-128-ctr",
                    "cipherparams": {
                        "iv": "29157429a03804a398abf33416e12e5e"
                    },
                    "ciphertext": "7a8a9b15543721f0e9d0a5f3dd58cd7a10c36f16e7230edd8f7c9a700ee23904",
                    "kdf": "pbkdf2",
                    "kdfparams": {
                        "c": 1000000,
                        "dklen": 32,
                        "prf": "hmac-sha256",
                        "salt": "4e00caf63638c4f5e77d56298e3ff86c"
                    },
                    "mac": "1e67f31a83a2266eb0454b0202cf922927d72ee1de6ccfcdd8b9324003b794f4"
                },
                "id": "baf8ccf3-7e68-4147-ab78-1e274a163f7b",
                "version": 3
            },
            "private_key": "0x1e6dba0c25e107e68c536b1705f0d91fd942769c2407b7752ea5e5eff396ba42"
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code":"fail", "error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```

# 钱包-导出私钥
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "export_private",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "keystore": {},
            "pwd": "hyf",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
加密后
```json
{
    "method": "export_private",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "private_key": ""
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-导出keystore
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "export_keystore",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "keystore": {},
            "pwd": "密码",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
加密后
```json
{
    "method": "export_keystore",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "keystore": {}
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```
# 钱包-获取交易列表
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "get_all_transaction",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
            "time": "时间戳"
        }
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
加密后
```json
{
    "method": "get_all_transaction",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": ""
    },
    "jsonrpc": "2.0",
    "id": ""
}
```
## 下行
加密前
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": {
            "transaction_list": [
                {
                    "tx_hash": "0x3ad42b1cf89d2a2d70677f4e757b9aba83c12e4717401cc0ff1246363605f145",
                    "from_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                    "to_address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
                    "value": "10"
                },
                {
                    "tx_hash": "0x3ad42b1cf89d2a2d70677f4e757b9aba83c12e4717401cc0ff1246363605f146",
                    "from_address": "122121",
                    "to_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                    "value": "10.0003"
                }
            ]
        }
    }
}
```
加密后
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
}
```
```
error
{"result": {"code": "fail", "error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```
# APP-创建
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "创建APP的名称",
    "desc": "app相关的描述信息",
    "create_cli_keys": false,
    "create_srv_keys": false,
    "cli_keys_length": 4096,
    "srv_keys_length": 4096,
    "r_cli_publickey": true,
    "r_srv_privatekey": true,
    "cli_keys": {
         "cli_publickey": "xxx",
         "cli_privatekey": "xxx"
    },
    "srv_keys": {
         "srv_publickey": "xxx",
         "srv_privatekey": "xxx"
    },
    "ip": ["ip1", "ip2", "ip3"],
    "ns": ["domain1", "domain2", "domain3"],
    "srv": ["srv1", "srv2", "srv3"],
    "status": 0,
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_create",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "appid": "创建成功的appid",
    "cli_keys": {
         "cli_publickey": "xxx",
         "cli_privatekey": "xxx"
    },
    "srv_keys": {
         "srv_publickey": "xxx",
         "srv_privatekey": "xxx"
    }
}
```
把以上回复内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-删除
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",  
    "time": "提交时间， 格式：Unix时间戳"      
}
```
把以上请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_remove",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "appid": "成功删除的appid"
}
```
把以上回复内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```
# APP-编辑
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",
    "ns": ["全部更新，不接受增量更新", "ns2"],
    "ip": ["全部更新，不接受增量更新", "ip2"],
    "srv": ["全部更新，不接受增量更新", "srv2"],
    "status": 1,
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_edit",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "appid": "成功编辑的appid"
}
```
把回复内容转换成字符串，再对字符串进行签名和加密后：
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-获取信息
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",
    "field": ["ip", "ns", "srv"],
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_info",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "appid": "成功编辑的appid",
    "ip": [],
    "ns": [],
    "srv": []
}
```
把回复内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-状态统计
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": ["appid列表", "appid2", "appid3"],
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_status",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "data": [
        {
            "appid": "appid1",
            "request_num": 100,
            "success": 80,
            "fail": 20,
            "other": "xxx"
        },
        {
            "appid": "appid2",
            "request_num": 100,
            "success": 80,
            "fail": 20,
            "other": "xxx"
        }
    ]
}
```
把回复内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```


