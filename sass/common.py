#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/23 上午11:06
# @Author : Caden
# @Site : 
# @File : common.py
# @Software: PyCharm

import json
import time
import hashlib
import requests
import paramiko
import re
import hmac
import random
from urllib.parse import quote

"""
签名分为两种：登录签名、网关签名
登录签名：
    appKey=(服务器给到客户端，客户端固定写死)
    version: 默认1.0，
    nonce:随机字符串,PC(36位)，小程序(68位)
    timestamp:请求时间,时间格式 yyyy-MM-dd HH:mm:ss
    appSecret：
    sign:签名值,签名参数:(appKey + nonce + timestamp + version), 签名秘钥:appSecret(服务器给到客户端，客户端固定写死)
    header头中增加 x-debug=true,会跳过签名认证，尽在测试环境生效
网关签名：
    appKey="userCenter"
    method="zhiyong.usercenter.tenant.invitecode.query"
    appSecret="userCenter8888"
    version="1.0

签名算法：
1.公共参数和业务参数,除去sign参数和byte[]类型的参数，根据参数名称的ASCII码表的顺序排序（按照key+values排序）
2.排好序的字符串utf-8编码
3.编码后的字符串通过HMAC_MD5加密
4.加密后的字符串统一转成大写
"""

def signature(AppSecret, **data):
    """
    签名算法
    :param AppSecret:加密的密钥
    :param data:签名数据
    :return:签名字符串
    """
    data_list = []
    for key, value in data["data"].items():
        data_list.append(key+value)
    data_list.sort()
    data_string = "".join(data_list)
    h = hmac.new(AppSecret.encode('utf-8'), data_string.encode('utf-8'), digestmod="MD5")
    return h.hexdigest().upper()

def generate_random_str(random_length=36):
    """
    生成一个指定长度的随机字符串
    :param random_length:
    :return:随机字符串
    """
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789-'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str

def login_add_param_url(data={},version="1.0",appKey="egohdzsbvhuwpb6m",appSecret="ZDcgQExDYS2kbueZYPQJHi/oYDNKMqERAOiUYa5qRgg="):
    """
    登录签名，业务参数加上公共参数再加上签名参数生成URL参数
    :param data:业务参数字典
    :return:url中的参数字符串
    """
    res = data
    timestamp = quote(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    res["version"] = quote(version)
    res["timestamp"] = timestamp
    res["appKey"] = quote(appKey)
    res["nonce"] = quote(generate_random_str())
    sign = signature(appSecret,data=res)
    res["sign"] = sign

    if res == {} or res == "":
        url_str = ""
    else:
        a = ""
        for key in res.keys():
            value = "%s=%s" % (key, res[key])
            a = a + "&" + value
        st = a
        url_str = "?" + st[1:]
    res.clear()
    return url_str

def gateway_add_param_url(appKey,method,appSecret,data={},version="1.0"):
    """
    网关签名，业务参数加上公共参数再加上签名参数生成URL参数
    :param data:业务参数字典
    :return:url中的参数字符串
    """
    res = data
    timestamp = quote(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    res["version"] = quote(version)
    res["timestamp"] = timestamp
    res["appKey"] = quote(appKey)
    res["method"] = quote(method)
    sign = signature(appSecret,data=res)
    res["sign"] = sign
    if res == {} or res == "":
        url_str = ""
    else:
        a = ""
        for key in res.keys():
            value = "%s=%s" % (key, res[key])
            a = a + "&" + value
        res = a
        url_str = "?" + res[1:]
    return url_str

# saas请求
class SaaS:
    def __init__(self, mobile):
        self.base_url = "http://passport.test.zhiyong.highso.com.cn"
        self.open_url = "http://open.test.zhiyong.highso.com.cn"
        self.picture_code = "8888"
        self.mobile_code = "888888"
        self.mobile = mobile
        self.password = "123456"
        self.run_session = requests.session()
        # self.headers = {"Content-Type": "application/json", "x-debug": True} # 加 "x-debug": True可以绕过登录签名
        self.headers = {"Content-Type": "application/json"}

    # 获取token验证，需签名
    def get_token(self):
        token_url = self.base_url + "/api/authcode/show" + login_add_param_url()
        token_result = self.run_session.post(url=token_url, headers=self.headers)
        print("获取toke后响应：" + token_result.text)

    # 获取图片验证码
    def get_image_code(self):
        passport_url = self.base_url + "/api/authcode/imgAuthCode"
        self.run_session.get(url=passport_url, headers=self.headers)

    # 获取手机短信验证码，需签名
    def get_mobile_code(self, sms_type, mobile, authCode="8888"):
        get_mobile_code_url = self.base_url + "/api/passport/sms/send" + login_add_param_url()
        mobile_data = {
            "smsType": sms_type,
            "mobile": mobile,
            "authCode": authCode
        }
        # print(token_url)
        mobile_result = self.run_session.post(url=get_mobile_code_url, json=mobile_data, headers=self.headers)
        # print("获取手机短信验证码响应：" + mobile_result.text)

    # web端短信登录, login_source登录来源， 1-APP, 2-PC, 3-MINI-PROGRAM;login_type登录类型，1-短信登录
    def web_mobile_login(self, version="1.0"):
        self.get_token()
        self.get_image_code()
        # self.get_token()
        self.get_mobile_code(sms_type=1, mobile=self.mobile)
        # self.get_token()
        login_url = self.base_url + "/api/passport/login" + login_add_param_url()
        login_data = {
            "loginSource": 2,
            "loginType": 1,
            "mobile": self.mobile,
            "smsCode": self.mobile_code
        }
        login_result = self.run_session.post(url=login_url, json=login_data, headers=self.headers)

        cookie = requests.utils.dict_from_cookiejar(login_result.cookies)
        # print("登录后响应：" + login_result.text)
        # print(login_result.cookies)
        # print(self.run_session.cookies)
        # print(cookie)
        # return login_result.text
        return self.run_session

    def request_business_api(self, req_method, appKey, method, appSecret, version="1.0", req_query_data={}, body_data={}):
        """
        对后台接口请求
        :param req_method: 请求方法
        :param appKey: 加密公钥
        :param method: dubbo接口方法
        :param appSecret: 加密私钥
        :param version:版本
        :param req_query_data:请求的query参数
        :param body_data:请求的body参数
        :return:响应结果
        """
        bus_url = self.open_url + "/router/rest/" + gateway_add_param_url(appKey=appKey,method=method, appSecret=appSecret,
                                                                          data=req_query_data,version=version)
        if req_method == "get":
            bus_result = self.run_session.get(url=bus_url, headers=self.headers)
        elif req_method == "post":
            bus_result = self.run_session.post(url=bus_url, headers=self.headers, json=body_data)
        else:
            return "不支持的请求方法"
        json_data = bus_result.json()
        return json_data


if __name__ == "__main__":
    se = SaaS(mobile="15889501911")
    se.web_mobile_login()
    # se.request_business_api(req_method="get",appKey="userCenter",method="zhiyong.usercenter.tenant.invitecode.query",
    #                                     appSecret="userCenter8888",version="1.0")
    # from urllib.parse import unquote
    # print(unquote("2020-12-29%2017%3A24%3A05"))

    # t_session：accessToken
    # t_rtu：refreshToken

    # run_session = requests.session()
    # data = {
    #     "accessToken":'qWmtLTQ85rzRx1eCO99PyoQDth3jhXSVP2HpxdRa5g/cr6xvERXSJXabOFedGyfRgIOcqAyPWklzyHxuSMkgAfw7mLEwDL9hNSSs6OseBCkujbnA/i7f+EitXL2tbfkEzbcXNSwxhQUbVe5EkXK+h9o/6uLn5uz5As5308mrG5DjqS/3REouyvAhwKBmlQXQGu+Ri/vEU2DVbFlqC1o+cA==',
    #     "refreshToken": 'G/Sd1u2sFsk+roXP673AhyVNmj12/tcUUNTamPlLE5sN0K1KRNThGllrT0fN2UzlR36jK9UH2ICvAnqlbdVeLZTQnjTt4haSTjSmTQCnWBVkh8EDQAJnIypHEWqMIsaLbdD+Fssj5wjYUrTDqucmpsyeqTi48c9bv+V9OlIpwZcVzOEied+r367OWEnOGPRVmoJvRCp1VoZXZE049F6kkr7LHWbm8mQ+dJCmGKXvYYI='
    # }
    # re = run_session.post(url="http://passport.test.zhiyong.highso.com.cn/api/session/getSession", json=data,
    #                  headers={"Content-Type": "application/json"})
    # print(re.text)



