# coding:utf-8
from my_dispatcher import api_add, api


@api_add
def my_method(*args, **kwargs):
    d = {"ihyf": 111}
    return d
