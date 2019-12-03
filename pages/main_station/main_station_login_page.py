# -*- coding: utf-8 -*-
from common.element import Element
from common.selenium_pages import SeleniumPages


class MainStationLoginPage(SeleniumPages):
    """主站登录页"""

    username_input = Element(css=".index-loginInput.index-loginInputUser", describe="用户名输入框")
    password_input = Element(css=".index-loginInput.index-loginInputPwd", describe="密码输入框")
    login_button = Element(css=".index-loginBtn.index-loginBtn--login", describe="登录按钮")
    regster_button = Element(css=".index-loginBtn.index-loginBtn--pwd", describe="注册按钮")
    error_message_p = Element(css="div.index-loginBox.index-loginBoxCheck>.index-loginHint", describe="错误信息标签")



