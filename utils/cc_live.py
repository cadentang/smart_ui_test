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