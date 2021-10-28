#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/17 下午2:26
# @Author : Caden
# @Site : 
# @File : zhiyong_request_common.py
# @Software: PyCharm

import json
import time
import hashlib
import requests
import paramiko
import re


def get(url, headers=None, params=None, timeout=10):
    try:
        resposnse = requests.get(url, headers=headers, params=params, timeout=float(timeout))
        return resposnse.text
    except TimeoutError:
        print("Time out!")

def post(url, headers=None, params=None, data=None, timeout=10):
    try:
        response = requests.post(url, headers=headers,params=params, data=data, timeout=float(timeout))
        return response
    except TimeoutError:
        print("Time out!")

class SaaSLogin:
    def __init__(self, mobile, password="123456"):
        self.base_url = "http://passport.test.zhiyong.highso.com.cn"
        self.picture_code = "8888"
        self.mobile_code = "888888"
        self.mobile = mobile
        self.password = password
        self.run_session = requests.session()

    # 获取token验证
    def get_token(self):
        token_url = self.base_url + "/authcode/show"
        self.run_session.post(url=token_url, headers={"Content-Type": "application/json"})

    # 获取图片验证码
    def get_image_code(self):
        passport_url = self.base_url + "/authcode/imgAuthCode"
        self.run_session.get(url=passport_url, headers={"Content-Type": "application/json"})

    # 获取手机短信验证码
    def get_mobile_code(self, sms_type, mobile):
        token_url = self.base_url + "/passport/sms/send"
        mobile_data = {
            "smsType": sms_type,
            "mobile": mobile
        }
        self.run_session.post(url=token_url, json=mobile_data, headers={"Content-Type": "application/json"})

    # web端短信登录, login_source登录来源， 1-APP, 2-PC, 3-MINI-PROGRAM;login_type登录类型，1-短信登录
    def web_mobile_login(self):
        login_url = self.base_url + "/passport/login"
        login_data = {
            "loginSource": 2,
            "loginType": 1,
            "mobile": self.mobile,
            "smsCode": self.mobile_code
        }
        login_result = self.run_session.post(url=login_url, json=login_data, headers={"Content-Type": "application/json"})
        print(json.loads(login_result.text))
        print(login_result.cookies)
        print(self.run_session.cookies)
        cookie = requests.utils.dict_from_cookiejar(login_result.cookies)
        print(cookie)

    # 小程序端登录
    def mini_program_login(self):
        wx_login_url = self.base_url + "/passport/miniProgramLogin"
        login_data = {
            "jsCode": 2,
            "iv": 1,
            "encryptMobile": self.mobile
        }

    # web端密码登录
    def web_password_login(self):
        pass

    # app端短信登录
    def app_mobile_login(self):
        pass

    # app端密码登录
    def app_password_login(self):
        pass

if __name__ == "__main__":
    SaaSLogin(mobile="19983271081").web_mobile_login()
