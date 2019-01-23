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
            "address": [
                "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1"
            ],
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
        "data": [
            {
                "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "eth_balance": "100"
            },
            {
                "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "eth_balance": "100"
            },
            {
                "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "eth_balance": "100"
            },
            {
                "address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                "eth_balance": "100"
            }
        ]
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
            "page": 1,
            "limit": 10,
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
                    "transaction_time": "2018-12-13 10:23:19",
                    "tx_hash": "0x3ad42b1cf89d2a2d70677f4e757b9aba83c12e4717401cc0ff1246363605f145",
                    "from_address": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
                    "to_address": "0xbEdc1e0341A85A571243990d7bc057a554966CE5",
                    "value": "10"
                },
                {
                    "transaction_time": "2018-12-13 10:23:19",
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
    "appid": "创建APP的名称",    // app名称
    "desc": "app相关的描述信息", // app的描述信息
    "create_cli_keys": false,   // [true/false]，如果为true，服务端会生成用于client的公钥和私钥， 
                                // 如果为false，需要上传公钥，私钥可选
    "create_srv_keys": false,   // [true/false]，如果为true，服务端会生成用于server的公钥和私钥，
                                // 如果为false，需要上传私钥，公钥可选
    "cli_keys_length": 4096,    // 生成用于client的钥匙长度
    "srv_keys_length": 4096,    // 生成用于server的钥匙长度
    "r_cli_publickey": true,    // 在返回结果中包含用于client中的公钥，默认不返回，只返回用于client的私钥
    "r_srv_privatekey": true,   // 在返回结果中包含用于server中的私钥，默认不返回，只返回用于server的公钥
    "cli_keys": {               // 用于client端的钥匙
         "cli_publickey": "xxx",     // 公钥
         "cli_privatekey": "xxx"     // 私钥
    },
    "srv_keys": {               // 用于server端的钥匙
         "srv_publickey": "xxx",     // 公钥
         "srv_privatekey": "xxx"     // 私钥
    },
    "ip": ["192.168.100.0/24", "192.168.100.1", "218.85.0.0/255.255.0.0"],     // 用于APP接入端，请求IP验证
    "ns": ["www.zzy.com", "*.zzy.com", "*zzy.com"],    // 用于APP接入端，请求域名验证
    "srv": ["srv1", "srv2", "srv3"],  // 用于APP开放服务的验证
    "master_contract_address": ["address1", "address2"],  // 传入合约地址
    "status": 0,                      // 表示APP所处状态，功能暂定
    "time": "提交时间， 格式：Unix时间戳"   // 每次提交都必须生成新的时间
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_create",             // 创建APP接口名称
    "params": {
        "appid": "syncapp",            // 后台APP名称
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "创建成功的appid", // 创建成功的APP
    "cli_publickey": "xxx",    // 用于client的公钥，默认不返回
    "cli_privatekey": "xxx",   // 用于client的私钥，默认返回
    "srv_publickey": "xxx",    // 用于server的公钥，默认返回
    "srv_privatekey": "xxx"    // 用于server的私钥，默认不返回
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
    "appid": "APP的名称",     // 要删除的APP名称
    "time": "提交时间， 格式：Unix时间戳"      
}
```
把以上请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_remove",   //删除APP接口
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功删除的appid"    // 返回成功删除的APP名称
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
    "appid": "APP的名称",    // 需要修改的APP名称
    // 以下字段，可以按需要进行添加
    "desc": "XXX",           // APP描述       
    "ip": ["ip1", "ip2"],    // 全部更新，不接受增量更新
    "ns": ["ns1", "ns2"],    // 全部更新，不接受增量更新
    "srv": ["srv1", "srv2"],  // 全部更新，不接受增量更新
    "cli_publickey": "xxxx",  // 用户client端的公钥
    "cli_privatekey": "xxxx", // 用户client端的私钥
    "srv_publickey": "xxxx", // 用户server端的公钥
    "srv_privatekey": "xxxx", // 用户server端的私钥
    "status": 1,              // 状态
    "time": "提交时间， 格式：Unix时间戳" 
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_edit",      // 编辑接口名称
    "params": {
        "appid": "syncapp",   // 后台APP名称
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功编辑的appid"
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
    "field": ["ip", "ns", "srv"],    // 字段列表，值参考编辑接口（不包含time字段）
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_info",       // 信息获取接口
    "params": {
        "appid": "syncapp",    // 后台APP名称
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功编辑的appid",
    "ip": [],
    "ns": [],
    "srv": []
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
    "appids": ["appid列表", "appid2", "appid3"],  // APP名称列表
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
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

# APP-清理Redis验证缓存
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "appid",  // APP名称
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_cleanup",
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
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "appid"  // APP名称
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
# 合约-新增主合约
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "add_master_contract",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "master_contract_name": "主合约名（不能重复，不能使用中文）",
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
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "code": "success",
        "sign": "",
        "data": ""
    }
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
            "code": "success",
            "data": {
                "master_contract_name": "主合约名",
                "tx_hash": "部署哈希",
                "contract_address": "合约地址"
            }
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
# 合约-部署子合约
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "deploy_contract",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "no_decrypt": "no_decrypt", 
        "data": {
            "contract_name": "子合约名",
            "url": "获取子合约文件的url",
            "master_contract_name": "该子合约所属主合约名",
            "master_contract_address": "该子合约所属主合约地址",
            "time": 1234
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
加密后

"no_decrypt": "no_decrypt"

带此参数 无需将data加密，只需要签名
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
            "code": "success",
            "data": {
                "contract_name": "",
                "tx_hash": "",
                "contract_address": ""
            }
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
# 合约-调用合约函数
---
URL:{baseurl}/api
## 上行
加密前
```json
{
    "method": "transfer_contract",
    "params": {
        "appid": "hyf_app",
        "sign": "",
        "data": {
            "account": "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1",
            "contract_name": "luckyNumber",
            "func_name": "getbonusMoney",
            "func_param": "",
            "value": 2,
            "time": 123000
        }
    },
    "jsonrpc": "2.0",
    "id": 11
}
```
加密后
```json
{
    "method": "transfer_contract",
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
            "code": "success",
            "data": {}
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


# 钱包后台--获取最新message
不加密
---
URL:{baseurl}/api
## 上行

```json
{
	"jsonrpc": "2.0",
	"id": 1,
	"method": "get_newest_message",
	"params": {
		"page": "1",
		"limit": "10"
	}
}
```
## 下行

```json
{
	"result": {
		"data": [{
			"id": 50,
			"msg_name": "1",
			"msg_content": "111",
			"edit_time": "2019-01-15 16:16:29"
		}, {
			"id": 49,
			"msg_name": "11",
			"msg_content": "1",
			"edit_time": "2019-01-15 16:04:54"
		}, {
			"id": 48,
			"msg_name": "1",
			"msg_content": "1",
			"edit_time": "2019-01-09 16:01:18"
		}]
	},
	"id": 1,
	"jsonrpc": "2.0"
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```

# 钱包后台--获取帮助信息
不加密
---
URL:{baseurl}/api
## 上行

```json
{
	"jsonrpc": "2.0",
	"id": 1,
	"method": "get_newest_help_information",
	"params": {
		"page": "1",
		"limit": "10"
	}
}

```
## 下行

```json
{
	"result": {
		"data": [{
			"id": 16,
			"question": "2",
			"answer": "2",
			"edit_time": "2019-01-15 11:21:11"
		}, {
			"id": 15,
			"question": "2",
			"answer": "2",
			"edit_time": "2019-01-15 11:21:08"
		}]
	},
	"id": 1,
	"jsonrpc": "2.0"
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```

# 钱包后台--新增新反馈
不加密
---
URL:{baseurl}/api
## 上行

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "add_newest_feedback",
    "params": {
        "feedback_name": "feedback_name",
        "feedback_content": "feedback_content"
    }
}
```
## 下行

```json
{
    "result": {
        "code": "success",
        "message": "feedback success"
    },
    "id": 1,
    "jsonrpc": "2.0"
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```

# 钱包后台--获取协议
不加密
---
URL:{baseurl}/api
## 上行

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "get_newest_protocol",
    "params": {}
}
```
## 下行

```json
{
    "result": {
        "data": [
            {
                "id": 4,
                "protocol_name": "协议名",
                "protocol_content": "协议内容",
                "edit_time": "2019-01-15 14:56:19"
            },
            {
                "id": 1,
                "protocol_name": "协议名",
                "protocol_content": "协议内容",
                "edit_time": "2019-01-15 09:47:14"
            }
        ]
    },
    "id": 1,
    "jsonrpc": "2.0"
}
```
```
error
{"result": {"code": "fail":,"error": "xx error"}, "id": 0, "jsonrpc": "2.0"}
```










