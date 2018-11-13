# coding:utf-8
def check_kv(d1, necessary_keys):
    """校验接口传入的keys values和必要的参数差别"""
    error = ""
    for k in necessary_keys:
        if k not in d1.keys():
            error += str(k) + " error"
            return error
        if not d1[k]:
            error += str(k) + " do not have value"
            return error
    if error:
        return error
    else:
        return "Success"

