## DBManager
创建`SQLALCHEMY_DATABASE_URI_SETTINGS`配置中所有数据库的engine和session，把创建的结果存储到数据结果中

### 方法：init_app
> 注册app

### 方法：create_sessions
> 遍历`SQLALCHEMY_DATABASE_URI_SETTINGS`，用于创建engine和session，并存储到数据结构中

### 方法：create_single_session
> 创建engine和session，并把生成的实例存储到数据结构中

### 方法：get_session
> 从指定的数据库组中随机返回一个session实例

### 方法：get_engine_master
> 从指定的数据库组中随机返回一个master的session实例

### 方法：get_autobase_obj
> 从指定的数据库组中，随机返回一个master的base实例

### 方法：master
> 从指定的数据库组中，随机返回一个master的session实例

### 方法：slave
> 从指定的数据库组中，随机返回一个slave的session实例

### 方法：autobase
> 返回所有base实例

### 方法：get_table
> 从指定数据库组中，返回一张表的结构数据

### 方法： test_table
> 测试指定的表在指定的数据库组中是否存在

### 方法：flush_autobase
> 刷新所有的base实例的数据信息，重新进行同步


## DBProxy
未用
