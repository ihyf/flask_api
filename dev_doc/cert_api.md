此文件实现服务层与区块链后台的交互，内容主要是app相应功能

## 函数：check_attr
> 对数据库字段进行检测，在数据库表中，是否有定义这个字段【数据库表的定义，可以参考util目录下的mysql_db.py文件】

以下接口函数，遵循jsonrpc协议，具体的参数请参考目录cert/cert.md文件

## 接口函数：bk_create
> 创建app

## 接口函数：bk_remove
> 删除app

## 接口函数：bk_edit
> 编辑app，对app的各参数属性进行重新设置

## 接口函数：bk_reset
> 对app的公钥，私钥进行操作，重新生成或者重新赋值

## 接口函数：bk_info
> 获取app的相关信息

## 接口函数：bk_lists
> 获取app列表信息

## 接口函数：bk_status
> 获取app的统计信息

## 接口函数：bk_cleanup
> 清空redis中，app的缓存信息
