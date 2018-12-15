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
    "ip": ["ip1", "ip2", "ip3"],     // 用于APP接入端，请求IP验证，只支持完全匹配，不支持泛匹配
    "ns": ["domain1", "domain2", "domain3"],    // 用于APP接入端，请求域名验证，只支持完全匹配，不支持泛匹配
    "srv": ["srv1", "srv2", "srv3"],  // 用于APP开放服务的验证
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
    "appid": "创建成功的appid",
    "cli_publickey": "xxx",    // 用于client的私钥，默认返回
    "cli_privatekey": "xxx",   // 用于client的公钥，默认不返回
    "srv_publickey": "xxx",    // 用于server的私钥，默认返回
    "srv_privatekey": "xxx"    // 用于server的公钥，默认不返回
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


