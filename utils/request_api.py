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

def get_sql():
    """生成用户sql插入文件，生成用户手机号文件"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registerDate = now
    createDate = now
    updateDate = now
    sql_list = []
    mobile_list = []
    for i in range(1000,1100):
        mobile = "1998327" + str(i)
        email = mobile + "@qq.com"
        s = f"INSERT INTO `customer` (`birthday`, `cityId`, `customerLevel`, `customerStatus`, `customerType`, `education`, `createBy`, `email`, `headImage`, `major`, `mobile`, `msn`, `nickName`, `password`, `position`, `provinceId`, `qq`, `flowSource`, `realName`, `registerDate`, `registerPlace`, `registerUrl`, `school`, `sex`, `sign`, `telephone`, `trade`, `createByName`, `customerGroup`, `createDate`, `registerStep`, `address`, `vip`, `townId`, `createType`, `password2`, `pageNum`, `isOfficial`, `corporation`, `accountType`, `customerActivate`, `childCategoryIdString`, `testArea`, `idCard`, `insuranceInfoFinishTime`, `currentCategoryId`, `updateDate`) VALUES (NULL, NULL, 1, 0, 1, NULL, NULL, {email}, -1, NULL, {mobile}, NULL, '12', 'e10adc3949ba59abbe56e057f20f883e', NULL, NULL, NULL, '', '唐锟', {registerDate}, '21', '/customerRegister/showRegister.do', NULL, NULL, NULL, NULL, NULL, NULL, 3, {createDate}, 3, NULL, 1, NULL, 1, NULL, '0', 0, NULL, 'Normal', NULL, NULL, NULL, '511024198809027274', NULL, 9, {updateDate});"
        sql_list.append(s)
        mobile_list.append(mobile)

    filename1 = 'user_data.txt'
    with open(filename1, 'w') as f:
        for i in mobile_list:
            f.write(i)
            f.write("\n")

    filename2 = 'user_sql.txt'
    with open(filename2, 'w') as f:
        for i in sql_list:
            f.write(i)
            f.write("\n")

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

if __name__ == "__main__":
    app = AppAPIUser()
    url =  'http://a0.highso.com.cn:8130/customer/v1/login.do'
    data = app.sig_dict({'userName': '19983271081', 'password': '123456'}, 0, '')
    se = requests.session()
    re = se.post(url, data=data)

    uid = json.loads(re.text)["data"]["uid"]
    sk = json.loads(re.text)["data"]["sk"]

    query = {'categoryId': 9}
    params = app.sig_dict(query, uid, sk)

    r1 =  se.get(url="http://w0.highso.com.cn/study/app/customerGoods/v1/goods", params=params, headers={"Content-Type":"application/json"})
    print(r1.text)

    query = {'categoryId': 9}
    params = app.sig_dict(query, uid, sk)

    post_data = {"mediaId":62529,"downloadType":3,"goodsModuleId":11393,"downloadUrl":"http://down.highso.com.cn/pdf/2018/ij/26_yz_wxb_2018_01_yjjzs_jsgcjj_sjjjtg_1Z102000_gccbdqrhjsff_5.pdf"}
    # post_data = json.dumps(post_data)
    query, headers = app.sig_post_json(post_data, {}, uid, sk)
    headers['Accept'] = 'application/json'
    headers['Content-Type'] = 'application/json'

    r2 = se.post(url="http://w0.highso.com.cn/study/app/download/v1/record", params=query, json=post_data, headers=headers)
    print(r2.text)