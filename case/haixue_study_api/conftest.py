# -*- coding: utf-8 -*-
import json
import pytest
import time
import requests
from utils.global_variable import get_value, judg_dicit
from utils.request_api import AppAPIUser


pc_domain = {"test0": "http://w0.highso.com.cn", "reg": "http://w1.highso.com.cn", "stage": "http://w2.highso.com.cn"}
app_domain = {"test0": "http://w0.highso.com.cn", "reg": "http://w1.highso.com.cn", "stage": "http://w2.highso.com.cn"}
globle_arg = get_value("config_dict")




@pytest.fixture(scope="class", autouse=False)
def get_pc_session():
    """pc端获取登录态"""
    if judg_dicit():
        if globle_arg["pattern"] == "local":
            pass
    pc_session = requests.session()

    pwd_header = {"Content-type":"application/json"}
    pwd_data = {
        "account": "19983271081",
        "password": "e10adc3949ba59abbe56e057f20f883e",
        "needServiceToken": "true",
        "systemCode": "haixue-upcore-api"
    }

    re = pc_session.post(url="http://w0.highso.com.cn/passport-api/auth/pwd", data=json.dumps(pwd_data), headers=pwd_header)

    service_token = json.loads(re.text)["data"]["serviceToken"]
    get_url = f"http://w0.highso.com.cn/upcore/serviceToken/validate?serviceToken={service_token}&deviceType=NORMAL&pageNum=0&bdVid"
    r = requests.get(url=get_url, headers=pwd_header, allow_redirects=False)
    print(r.content)


    # print(r.request)
    # print(r.headers)
    # print(r.request)
    # print(r.is_permanent_redirect)
    # print(r.is_redirect)
    print(r.url)
    print(r)
    print(r.history)
    #
    # red = r.history
    # print(red[0].headers)
    # print(red[0].text)
    # print(red[1].headers)
    # print(red[1].text)

    yield pc_session


@pytest.fixture(scope="class", autouse=False)
def get_app_session():
    """app端获取登录态"""
    if judg_dicit():
        if globle_arg["pattern"] == "local":
            pass
    app = AppAPIUser()
    url = 'http://a0.highso.com.cn:8130/customer/v1/login.do'
    data = app.sig_dict({'userName': '19983271081', 'password': '123456'}, 0, '')
    app_session = requests.session()
    re = app_session.post(url, data=data)

    uid = json.loads(re.text)["data"]["uid"]
    sk = json.loads(re.text)["data"]["sk"]

    yield app, app_session, uid, sk

