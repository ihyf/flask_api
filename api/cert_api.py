# coding:utf-8
from my_dispatcher import api_add


@api_add
def token_test(*args, **kwargs):
    print(args, kwargs)
    return {"result": "ok"}





