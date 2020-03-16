# -*- coding: utf-8 -*-
import random
import requests

sku_list = ['一级建造师', '二级建造师', '注册会计师', '一级消防工程师', '司法考试', '执业药师']

def check_is_register(host, mobile):
    """判断手机号是否注册"""
    url = host + "/customerRegister/checkForUniqueness.do"
    payload = {'mobileOrEmail': mobile,
               'random': '0.15100794747188084'}
    response = requests.post( url, data=payload)
    return response.text

def get_register_phone(host, phone="19900000000"):
    """获取可注册的手机号"""
    for i in range(99999999999):
        if check_is_register(host, phone) == "false":
            phone = str(int(phone) + 1)
            continue
        else:
            return phone

def get_register_data(host, sku=None):
    """获取注册数据"""
    register_data = {}
    phone = get_register_phone(host)
    register_data["email"] = phone + "@qq.com"
    register_data["pwd"] = "123456"
    register_data["phone"] = phone
    if sku:
        register_data["sku"] = sku
    else:
        register_data["sku"] = random.choice(sku_list)
    return register_data
