# coding:utf-8
def check_kv(d1, necessary_keys):
    """校验接口传入的keys values和必要的参数差别"""
    error = ""
    for k in necessary_keys:
        if k not in d1.keys():
            error += str(k) + " key error"
            return error
        if not d1[k]:
            error += str(k) + " do not have value"
            return error
    if error:
        return error
    else:
        return "Success"


def to_byte32(s):
    len1 = len(s)
    if len1 > 32:
        print('input string length: ' + str(len1) + ' is too long')
        s = s[:32]
    else:
        print('input string length: ' + str(len1) + ' is too short')
        print('More characters needed: ' + str(32 - len1))
        s = bytes(s.ljust(32, '0'), 'utf-8')
    return s


def bytes_str_to_dict(b):
    return eval(str(b, encoding="utf-8"))


def get_srv_time():
    """获取服务器当前时间，并格式化成字符串"""
    import datetime
    t = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return t
