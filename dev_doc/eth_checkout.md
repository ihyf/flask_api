定义check_conn装饰器，用来对接入请求进行第一步验证
输入格式：
```json
{
    "method": "bk_create",
    "params": {
        "appid": "syncapp",
        "sign": "sign",
        "data": "data"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
* method: 对应于函数入口

* params.appid: app名称

* params.sign: params.data的解密的原始数据的签名数据

* params.data: 原始数据的加密数据

* jsonrpc: 固定值

* id: 固定值


验证内容及步骤：
1. 检查数据格式是否正确
2. 对sign的数据计算sha1，计算的值，在redis缓存中是否已经存在此值，如果存在，返回频繁请求的错误，如果不存在，把值加入缓存，执行下一步验证
3. 从redis缓存中读取app相关信息
 * 如果在redis中已经存在app对应的`checkout_{appid}_keys`，则所有信息从缓存中读取
 * 如果在redis中不存在`checkout_{appid}_keys`，则所有信息从mysql中读取，并把结果存入redis缓存
4. 验证app状态，不允许app访问，则返回错误
5. 验证接口的`method`是否在允许的列表中，不在，则返回错误
6. 验证接入请求的IP地址是否在允许的列表中，不在，则返回错误
7. 验证接入请求的域名是否合法：
 * 验证域名是否是开放api的域名本身，如果是，转到第8步
 * 如果不是开放api的域名本身，验证此域名是否在此app的允许列表中，如果不在则返回错误，如果在，转到第8步
8. 加载此app的客户端公钥和服务器的私钥，并且序列化
9. 对`data`进行解密和验证签名
 * 如果含有字段`no_decrypt`，并且值为`no_decrypt`，只对数据进行签名验证
 * 如果不含有字段`no_decrypt`，先对数据进行解密，再对解密数据进行签名验证
 * 以上两步出现错误，则返回对应错误
10. 把原始数据和其它有用数据赋值到参数对象kw中，把第8步生成的对象赋值给kw，以供后面的处理过程使用


## 函数： delete_checkout_redis
> 清空redis中app的缓存信息

## 函数： product_keys
> 生成app相关的redis中的key值

## 函数： get_keys
> 从数据库或者缓存中获取app的相关信息
