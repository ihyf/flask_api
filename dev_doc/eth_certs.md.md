类：EthCert，对公钥、私钥相关功能：

## 方法：init_dir
> 设置用户目录，以eth_certs.py文件为根目录，加上pems和用户名：
```
private => 以eth_certs.py所在目录/pems/用户名/private_key.pem
public  => 以eth_certs.py所在目录/pems/用户名/public_key.pem
```

## 方法：generate
> 生成公钥、私钥对，默认长度是2048

## 方法：load_key_from_file
> 从设置的用户目录中加载对应的公钥、私钥【从文件中读取】

## 方法：init_key
> 注册公钥、私钥【从参数中读取】

## 方法：serialization
> 序列化公钥、私钥【钥匙加载完，都需要经过序列化才能使用】

## 方法：convert
> 把转入的数据，转成byte类型，输出

## 方法：save_file
> 保存公钥或者私钥到设置的用户目录文件中

## 方法：sign2_str
> 对数据进行签名，输出str类型【正式环境中没有使用】，签名失败返回False

## 方法：sign2
> 对数据进行签名，输出byte类型【正式环境中没有使用】，签名失败返回False

## 方法：sign_str
> 对数据进行签名，输出str类型，使用SHA256算法，签名失败返回False

## 方法：sign
> 对数据进行签名，输出byte类型，使用SHA256算法，签名失败返回False

## 方法：verify2
> 对方法sign2和sign2_str签名的数据进行验证，验证失败返回False

## 方法：verify
> 对方法sign和sign_str签名的数据进行验证，验证失败返回False

## 方法：encrypt
> 对数据进行加密，输出byte类型，加密失败返回False

## 方法：encrypt_str
> 对数据进行加密，输出str类型，加密失败返回False

## 方法：decrypt
> 对数据进行解密，输出byte类型，解密失败返回False

## 方法：decrypt_str
> 对数据进行解密，输出str类型，解密失败返回False

## 方法：get_publickey
> 返回公钥

## 方法：get_privatekey
> 返回私钥
