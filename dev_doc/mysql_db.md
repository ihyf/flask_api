定义mysql数据库表结构

* 类名：Apps，表名：apps

| 字段 | 类型 | 空 | 默认 | 属性 | 注释 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| id | int  | no| autoincrement| 自增键、主键| |
| appid| varchar(200)| 不为空| |主键 | appid |
| parent_appid| varchar(200)| 'unknow' | | | 所属父appid |
| desc | varchar(200)| 不为空 | | | APP描述信息 |
| ip | Json | 不为空 | | | ip地址白名单 |
| ns | Json | 不为空 | | | 域名白名单 |
| cli_publickey | text | 不为空 | | | 客户端公钥 |
| cli_privatekey | text | 不为空 | | | 客户端私钥 |
| srv_publickey | text | 不为空 | | | 服务端公钥 |
| srv_privatekey | text | 不为空 | | | 服务端私钥 |
| srv | Json | 不为空 | | | 开放的服务列表 |
| master_contract_address | Json | 不为空 | [] | | 合约地址 |
| wallet | varchar(200) | 不为空 | 'no set' | | 钱包地址 |
| callback_url | varchar(250) | 不为空 | | | 回调地址 |
| status | int | 不为空 | | | app状态 |
