# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import collections
import sys

import re
import time
import datetime
import csv
import json
import os
import platform
import hashlib
from locust import HttpLocust, TaskSet, task, between, seq_task, TaskSequence
from locust.clients import HttpSession

import requests
from urllib3.exceptions import InsecureRequestWarning
import random
import queue

requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告

class AppAPIUser:

    def __init__(self):
        self.app = {
            'app_key': 'ho2dxs9g',
            'encrypt_key': 'i2yrl3kj',
            'version': '5.0.4',
            'token': 'edad1f6c-735b-46ea-8176-18e9936aeb41',
            'device': 'SMARTISAN'
        }
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
        # print(str_value)
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
        data['sig'] = sig
        return data

    def sig_post_json(self, body, query, uid, sk):
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

app = AppAPIUser()

class WebsiteTasks(TaskSet):

    def on_start(self):
        # try:
        #     self.gd = self.locust.queueData.get()
        # except:
        #     exit(0)


        try:
            self.gd = self.locust.user_data_queue.get()
        except:
            exit(0)

        self.gd['H5_api'] = "http://api-wealth-activity.test0.highso.com.cn"
        self.gd['haxiue_app'] = 'http://a0.highso.com.cn:8130'
        self.gd['haxiue_app_h5'] = 'http://api-wealth-discount.test0.highso.com.cn'
        self.haixue_app_h5_login()

    # app端h5内获取登录态
    def haixue_app_h5_login(self):
        # app内登录
        url = self.gd['haxiue_app'] + '/customer/v1/login.do'
        # data = app.sig_dict({'userName': self.gd.get("phone"), 'password': '123456'}, 0, '')
        data = app.sig_dict({'userName': self.gd.get("phone"), 'password': '123456'}, 0, '')
        # 设置sesssion
        self.session = HttpSession(self.gd['haxiue_app'])
        # 使用 session 来登录
        # 登录成功之后，就可以直接使用了
        with self.session.post(url, data=data, name='APP内登录', catch_response=True) as res:
            if res.status_code == 200:
                print(res.text)
                # if json.loads(res.text)["m"] == "ok" and json.loads(res.text)["m"] == 1:
                res.success()
            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return
        try:
            self.gd['uid'] = res.json()['data']['uid']
            self.gd['sk'] = res.json()['data']['sk']
        except:
            self.gd['uid'] = ''
            self.gd['sk'] = ''

        # 换取h5内的登录态
        h5_url = self.gd['haxiue_app_h5'] + f'/security/v1/login?customerId={self.gd["uid"]}'
        with self.session.post(url=h5_url, name='换取h5内的登录态', catch_response=True) as res:
            if res.status_code == 200:
                print(res.text)
                # if json.loads(res.text)["m"] == "ok" and json.loads(res.text)["m"] == 1:
                res.success()
            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return

    @task(6)
    def get_activity(self):
        url = self.gd['H5_api'] + '/h5/decennial/v1/getActivityDetail/182'
        with self.session.get(url=url, name='查询活动详情', catch_response=True) as res:
            if res.status_code == 200:
                # if json.loads(res.text)["msg"] == "true":
                res.success()
            else:
                res.failure('/h5/decennial/v1/getActivityDetail/182接口Failed!status_code:' + str(res.status_code))
                return

    @task(2)
    def get_user_prize(self):
        url = self.gd['H5_api'] + '/h5/decennial/v1/queryAcquiredPrize/182'
        with self.session.get(url=url, name="查询用户领取的奖品", catch_response=True) as res:
            if res.status_code == 200:
                # if json.loads(res.text)["success"] == "true":
                print(res.text)
                res.success()
            else:
                res.failure('/h5/decennial/v1/queryAcquiredPrize/182接口Failed!status_code:' + str(res.status_code))
                return

    @task(2)
    def get_prize(self):
        url = self.gd['H5_api'] + '/h5/decennial/v1/acquireAward/182'
        data = {"platform":1,"prizeIdList":[185]}
        headers = {"Content-Type": "application/json"}
        with self.session.post(url=url, json=data, headers=headers, name="用户领取优惠券", catch_response=True) as res:
            print(res.text)
            if res.status_code == 200:
                # if json.loads(res.text)["msg"] == "已经领取成功" or json.loads(res.text)["msg"] == "您已领取过优惠券":
                #     print(res.text)
                #     res.success()
                res.success()
            else:
                res.failure('/h5/decennial/v1/acquireAward/182接口Failed!status_code:' + str(res.status_code))
                return

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    # queueData = queue.Queue()

    # with open('user_sql.txt') as f:
    #     user_data = f.readlines()
    # queue_list = []
    # for i in range(len(user_data)):
    #     tmp_dict = {}
    #     tmp_dict["phone"] = user_data[i].replace("\n", "")
    #     queue_list.append(tmp_dict)
    queue_list = ["19983271081", "19983271082"]
    # for i in queue_list:
    #     queueData.put_nowait(i)

    user_data_queue = queue.Queue()
    for index in queue_list:
        data = {
            "phone": index,
        }
        user_data_queue.put_nowait(data)
    print(user_data_queue)
    host = 'http://a0.highso.com.cn'
    wait_time = between(0.5, 1)


"""
locust -f locust_demo.py --host=!!!!! --no-web -c 300 -t 60s -r 1
locust -f locustfile.py --master --web-host=x.x.x.x
locust -f locustfile.py --slave --master-host=x.x.x.x
"""