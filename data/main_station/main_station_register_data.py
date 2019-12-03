# -*- coding: utf-8 -*-
import random
from utils.operation_mysql import Mysql

sku_list = ['一级建造师', '二级建造师', '注册会计师', '一级消防工程师', '司法考试', '执业药师']


def get_phone_code():
    """
    获取注册手机的通用验证码
    :return:
    """
    mysql = Mysql()
    sql = '''
    SELECT code from highso.universalcode WHERE openingdate='2019-10-12';
    '''
    code = mysql.executeSQL(sql)[0][0]
    mysql.closeDB()
    return code

def get_register_phone():
    phone = "19900000000"
    return phone

def get_register_email():
    email = get_register_phone() + "@qq.com"
    return email

def get_pwd():
    pwd = "123456"
    return pwd

def get_register_data(sku=None):
    register_data = {}
    register_data["email"] = get_register_email()
    register_data["pwd"] = get_pwd()
    register_data["phone"] = get_register_phone()
    register_data["code"] = get_phone_code()
    if sku:
        register_data["sku"] = sku
    else:
        register_data["sku"] = random.choice(sku_list)

    return register_data

