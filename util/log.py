# coding: utf-8
from util.mysql_db import RecodeLogs
from util.dbmanager import db_manager


level = [
    'OFF',  # 关闭日志
    'FATAL',   # 致命错误
    'ERROR',   # 错误
    'WARN',    # 警告
    'INFO',    # 信息
    'DEBUG',   # 调试
    'TRACE',   # 细化调试
    'ALL'      # 打开所有日志
]


def rlog(alias="default", level_name="", message="", func_name="", stack_info=""):
    session = db_manager.master(alias)
    rd = RecodeLogs(
        level_name=level_name,
        message=message,
        func_name=func_name,
        stack_info=stack_info
    )
    session.add(rd)
    session.commit()
    return True


