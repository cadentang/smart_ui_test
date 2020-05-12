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

        try:
            self.gd = self.locust.queueData.get()
        except:
            exit(0)

        self.gd['ucenter'] = 'http://ucenter1.highso.com.cn'
        self.gd['k2'] = 'http://api.k2.reg.highso.com.cn'
        self.gd['end'] = 'http://t1.highso.com.cn'
        self.gd['crm_cx'] = 'http://cx1.highso.com.cn'
        self.gd['www_web'] = 'http://w1.highso.com.cn'
        self.gd['antd'] = 'http://antd.k2.reg.highso.com.cn/redirect'
        self.gd['haixue_app_api'] = 'http://a1.highso.com.cn'
        self.gd['H5_api'] = 'http://api-marketing-activities.reg.highso.com.cn'
        self.gd['haxiue_app'] = 'http://a0.highso.com.cn'

        self.haixueAPPLogin()

    def haixueAPPLogin(self):
        url = self.gd['haxiue_app'] + '/customer/v1/login.do'
        data = app.sig_dict({'userName': self.gd.get['phone'], 'password': '123456'}, 0, '')
        with self.client.post(url, data=data, name='登录', catch_response=True) as res:
            if res.status_code == 200:
                resp = res.text
                res.success()
            else:
                res.failure('Failed!status_code:' + str(res.status_code))
                return
        # 全局变量
        try:
            self.gd['uid'] = res.json()['data']['uid']
            self.gd['sk'] = res.json()['data']['sk']
        except:
            self.gd['uid'] = ''
            self.gd['sk'] = ''

    # # web端登录
    # def web_login(self):
    #     header1 = {"Content-type": "application/json"}
    #     data1 = {"account": self.gd.get('phone'),
    #              "password": "e10adc3949ba59abbe56e057f20f883e",
    #              "needServiceToken": "true",
    #              "systemCode": "haixue-upcore-api"}
    #
    #     with self.client.post(url="http://w0.highso.com.cn/passport-api/auth/pwd", data=json.dumps(data1),
    #                           headers=header1, name='换取token', catch_response=True) as res:
    #         if res.status_code == 200:
    #             service_token = json.loads(res.text)["data"]["serviceToken"]
    #             get_cookie = requests.utils.dict_from_cookiejar(res.cookies)
    #             res.success()
    #
    #             header2 = {"Cookie": f"pass_sec={get_cookie['pass_sec']};deviceType=NORMAL; pageNum=0"}
    #             get_url = f"http://w0.highso.com.cn/upcore/serviceToken/validate?serviceToken={service_token}&deviceType=NORMAL&pageNum=0&bdVid"
    #             with self.client.get(get_url, name='获取登录态', catch_response=True) as res:
    #                 if res.status_code == 200:
    #                     res.success()
    #                 else:
    #                     res.failure('/upcore/serviceToken/validate接口Failed!status_code:' + str(res.status_code))
    #                     return
    #         else:
    #             res.failure('/passport-api/auth/pwd接口Failed!status_code:' + str(res.status_code))
    #             return

    # @task(4)
    # def get_study_plan(self):
    #     url = 'http://w0.highso.com.cn/study/pc/live/timeLimitLive?categoryId=9'
    #     with self.client.get(url=url, name='获取主站个人中心直播日历', catch_response=True) as res:
    #         if res.status_code == 200:
    #             print(res.text)
    #             res.success()
    #         else:
    #             res.failure('/study/pc/live/timeLimitLive接口Failed!status_code:' + str(res.status_code))
    #             return

    @task(6)
    def get_activity(self):
        url = 'http://api-wealth-activity.test0.highso.com.cn/h5/decennial/v1/getActivityDetail/182'
        with self.client.get(url=url, name='查询活动详情', catch_response=True) as res:
            if res.status_code == 200:
                print(res.text)
                res.success()
            else:
                res.failure('/h5/decennial/v1/getActivityDetail/182接口Failed!status_code:' + str(res.status_code))
                return

    @task(2)
    def get_user_prize(self):
        url = 'http://api-wealth-activity.test0.highso.com.cn/h5/decennial/v1/queryAcquiredPrize/182'
        with self.client.post(url=url, name="查询用户领取的奖品", catch_response=True) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure('/h5/decennial/v1/queryAcquiredPrize/182接口Failed!status_code:' + str(res.status_code))
                return

    @task(2)
    def get_user_prize(self):
        url = 'http://api-wealth-activity.test0.highso.com.cn/h5/decennial/v1/queryAcquiredPrize/182'
        with self.client.post(url=url, name="查询用户领取的奖品", catch_response=True) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure('/h5/decennial/v1/queryAcquiredPrize/182接口Failed!status_code:' + str(res.status_code))
                return


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    queueData = queue.Queue()

    with open('user_sql.txt') as f:
        user_data = f.readlines()

    queue_list = []
    for i in range(len(user_data)):
        tmp_dict = {}
        tmp_dict["phone"] = user_data[i].replace("\n", "")
        queue_list.append(tmp_dict)

    for i in queue_list:
        queueData.put_nowait(i)

    host = 'http://www.w0.highso.com.cn'
    wait_time = between(5, 15)


"""
locust -f locust_demo.py --host=!!!!! --no-web -c 300 -t 60s -r 1
locust -f locustfile.py --master --web-host=x.x.x.x
locust -f locustfile.py --slave --master-host=x.x.x.x
"""