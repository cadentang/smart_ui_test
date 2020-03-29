# -*- coding: utf-8 -*-
from utils.config import ReadConfig
from utils.base_path import LOG_PATH, DRIVER_PATH, APP_PATH

# 如果是debug模式则会直接调用该配置，如需本地调试请直接修改globle_arg中的值
globle_arg = {
    "env": "test0",
    "user_port": "pc",
    "pattern": "local",
    "project": "main_station",
    "browser": "chrome",
    "version": "79",
    "log_path": LOG_PATH,
    "driver_path": DRIVER_PATH,
    "app_path": APP_PATH,
    }
debug_config_dict = ReadConfig(globle_arg).get_config()

def _init():
    """初始化一个全局变量字典"""
    global _global_dict
    _global_dict = {}
    return _global_dict

def set_value(key,value):
    """定义一个全局变量"""
    _global_dict[key] = value

def get_value(key=debug_config_dict,value=None):
    """ 得一个全局变量,不存在则返回默认值"""
    try:
        return _global_dict[key]
    except:
        return False

def judg_dicit():
    if get_value("get_arg"):
        return True
    else:
        return False
