# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:
网关rest方式：需要客户端和前端 封装统一请求的方法，
以后请求参数变化的部分：就是method、version、sign、session、appkey、业务参数，其它都是通用的
"""


ENV = "test"
BASE_URL = "http://open.test.zhiyong.highso.com.cn/router/rest"
REQUEST_METHOD = ""
appkey = "userCenter"
DUBBO_METHOD = ""
VERSION = ""
session = ""
timestamp = ""
sign = ""
tenantId = ""

query_params = {
    "appKey": appKey,
    "session": session,
    "method": DUBBO_METHOD,
    "timestamp": "11",
    "version": "1.0",
    "sign": sign,
    "tenantId": tenantId
}



def api_detail(api_name: string) -> dict:
    """
    获取单个API详情
    :param api_name: string,API名称
    :return: dict，返回详情的dict
    """
    api_detail_dict = {}

    return api_detail_dict


def saas_rest_sign():
    """
    加密
    :return: sign，返回加密后的签名
    """
    sign = ""
    return sign


def signature(self, data):
    ret = collections.OrderedDict(sorted(data.items()))
    str_value = ""
    for k, v in ret.items():
        str_value += str(k)
        str_value += str(v)
    str_value += self.app['encrypt_key']
    print(str_value)
    m = hashlib.md5()
    m.update(str_value.encode('utf-8'))
    md5value = m.hexdigest()
    return md5value


def get_session():
    """
    登录态保持
    :return: session->object
    """
    session = ""
    # 登录


    return session



def send_quest():
    """
    发送请求
    :return:
    """




