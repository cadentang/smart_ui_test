# -*- coding: utf-8 -*-

def _init():
    """初始化一个全局变量字典"""
    global _global_dict
    _global_dict = {}
    return _global_dict

def set_value(key,value):
    """定义一个全局变量"""
    _global_dict[key] = value

def get_value(key,value=None):
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
