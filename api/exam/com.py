# -*- coding: utf-8 -*-
import json
import time
import hashlib
import collections

from datetime import datetime

import requests
from bs4 import BeautifulSoup
from utils.operation_cmd import RunCmd
from utils.get_log import logger


def get(url, headers=None, params=None, timeout=10):
    try:
        resposnse = requests.get(url, headers=headers, params=params, timeout=float(timeout))
        return resposnse.text
    except TimeoutError:
        logger.error("Time out!")


def post(url, headers=None, params=None, data=None, timeout=10):
    try:
        response = requests.post(url, headers=headers,params=params, data=data, timeout=float(timeout))
        return response
    except TimeoutError:
        logger.error("Time out!")


class AppAPIUser:

    def __init__(self):
        self.app = {
            'app_key': 'ho2dxs9g',
            'encrypt_key': 'i2yrl3kj',
            'version': '5.0.4',
            'token': 'edad1f6c-735b-46ea-8176-18e9936aeb41',
            'device': 'SMARTISAN'
        }
        # self.app = {
        #     'app_key': 'ho2dxs9g',
        #     'encrypt_key': 'i2yrl3kj',
        #     'version': '5.0.4',
        #     # 'token': 'c8a61e8bd148081f',
        #     'token': '320216DB-4E9D-457C-832C-B7FB2FFFD781',
        #     'device': 'iPhoneX'
        # }
        self.uid = 0
        self.sk = ''
        self.account = ''

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

    def add_common_entry(self, data, uid, sk):
        ret = data
        ret['app_key'] = self.app['app_key']
        ret['v'] = '4.0'
        ret['token'] = self.app['token']
        ret['app_version'] = self.app['version']
        ret['device'] = self.app['device']
        if uid:
            ret['uid'] = uid
        if sk:
            ret['sk'] = sk
        return ret

    def sig_dict(self, query, uid, sk):
        data = self.add_common_entry(query, uid, sk)
        sig = self.signature(data)
        print(sig)
        data['sig'] = sig
        return data

    def sig_post_json(self, body, query, uid, sk):
        # 将body组装成临时字典
        bodystr = json.dumps(body)
        tm = int(time.time() * 1000)

        tempbody = {}
        tempbody['x-hx-timestamp'] = str(tm)
        tempbody['x-hx-app-key'] = self.app['app_key']
        tempbody['x-hx-token'] = self.app['token']
        tempbody['x-hx-app-version'] = self.app['version']
        tempbody['x-hx-device'] = self.app['device']
        tempbody['x-hx-sk'] = sk
        tempbody['body'] = bodystr
        tempbody = self.add_common_entry(tempbody, uid, sk)
        sig = self.signature(tempbody)
        headers = {
            'x-hx-timestamp': tempbody['x-hx-timestamp'],
            'x-hx-app-key': tempbody['x-hx-app-key'],
            'x-hx-token': tempbody['x-hx-token'],
            'x-hx-app-version': tempbody['x-hx-app-version'],
            'x-hx-device': tempbody['x-hx-device'],
            'x-hx-sk': tempbody['x-hx-sk'],
            'x-hx-sig': sig
        }
        retquery = self.add_common_entry(query, uid, sk)
        retquery['sig'] = self.signature(retquery)
        return retquery, headers

def pc_login():
    base_url = "http://w1.highso.com.cn"
    passport_url = base_url + "/passport-api/auth/pwd"
    se = requests.session()
    passport_data = {
        "account": 19983271043,
        "password": 123456,
        "needServiceToken": True,
        "systemCode": "haixue-upcore-api"
    }
    passport_result = se.post(url=passport_url, json=passport_data, headers={"Content-Type": "application/json"})
    # print(json.loads(passport_result.text))
    serviceToken = json.loads(passport_result.text)["data"]["serviceToken"]
    customerId = json.loads(passport_result.text)["data"]["customerId"]
    upcore_url = base_url + "/upcore/serviceToken/validate?csrf_token=deviceType=NORMAL&pageNum=0&bdVid=&serviceToken=" + serviceToken
    upcore_result = se.get(url=upcore_url, headers={"Content-Type": "application/json"}, allow_redirects=False)
    # print(upcore_result.cookies)
    cookie = requests.utils.dict_from_cookiejar(upcore_result.cookies)
    # print(cookie)
    # print(type(cookie))
    csrf_token = cookie["csrf_token"]
    # print(csrf_token)
    return {"se":se, "csrf_token":csrf_token, "base_url": base_url}

def app_login():
    app = AppAPIUser()
    se = requests.session()

    app_passport_url = "http://api-passport.reg.highso.com.cn"
    app_base_url = "http://a1.highso.com.cn"
    url = app_passport_url + '/auth/pwd'
    data = app.sig_dict({"account": 19983271081, "password": hashlib.md5(b"123456").hexdigest(),
                         "needAuthToken": True, "registerPlace": "10", "rememberMe": "REMEMBER_30_DAY"}, 0, "")
    print(data)
    passport_result = se.post(url=url, json=data, headers={"Content-Type": "application/json"})
    passport_result_dict = json.loads(passport_result.text)
    # if passport_result_dict["code"] == 200:
    #     sig =
    print(passport_result.text)
    uid = passport_result_dict["data"]["customerId"]

    data1={}
    url1 = app_base_url + "/exam/v2/getsByOutlineId.do"

    query = {'categoryId': 5, 'outlineId': 171021}
    # query = {}
    params = app.sig_dict(query, uid, "")
    re = se.get(url=url1, params=params)
    print(re.text)


if __name__ == "__main__":

    se = app_login()

    # print(se)
    # url = 'http://a1.highso.com.cn/outline/v1/showOutlinePage.do'
    # data = '["420429","128813"]'
    # data = tryJson(data)
    # query, headers = app.sig_post_json(data, {}, self.gd.get('uid'), self.gd.get('sk'))
    # headers['Accept'] = 'application/json'
    # headers['Content-Type'] = 'application/json'
    # with self.client.post(url=url, json=data, params=query, name='app-/outline/v1/showOutlinePage.do',
    #                       headers=headers, catch_response=True) as res:

