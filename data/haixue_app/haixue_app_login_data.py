# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:
"""


login_data = {
    "admin_phone_data": [[("phone", "18780127566", "123456")], "管理员账号及密码"],
    "success_email_data": [[("email", "623260178@qq.com", "123456")], "邮箱账号密码正确"],
    "fail_data_phone_error": [[("phone", "19983271000", "457888")], "手机号不存在"],
    "not_input_password": [[("phone", "19983271081", "")], "不输入密码"],
    "not_input_username": [[("phone", "", "123456")], "不输入用户名"],
    "not_input_username_password": [[("phone", "", "")], "不输入用户名和密码"],
    "fail_data_password_error": [[("phone", "19983271081", "457999")], "手机号正确，密码错误"]
}