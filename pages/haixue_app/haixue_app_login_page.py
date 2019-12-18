# -*- coding: utf-8 -*-
from common.appium_pages import AppiumPages
from common.element import Element

class HaiXueLoginPage(AppiumPages):
    _phone_input = None
    _password_input = None
    _login_button = None
    def login(self):
        self._login_button = "19983271081"
        self._password_input = "123"
        self._login_button.click()
    def register(self):
        pass

class AndriodHaiXueLoginPage(HaiXueLoginPage):
    _phone_input = Element(accessibility_id="xxxxxx",
                           describe="手机号/邮箱/学习卡输入框")
    _password_input = Element(accessibility_id="yyyyyy",
                              describe="密码输入框")
    _login_button = Element(accessibility_id="zzzzzz",
                            describe="登录按钮")

class IOSHaiXueLoginPage(HaiXueLoginPage):
    _phone_input = Element(ios_uiautomation="xxxxxx",
                           describe="手机号/邮箱/学习卡输入框")
    _password_input = Element(ios_uiautomation="yyyyyy",
                              describe="密码输入框")
    _login_button = Element(ios_uiautomation="zzzzzz",
                            describe="登录按钮")

class HaiXueHomePageFactory:
    def page(self, type):
        if type == "andriod":
            return AndriodHaiXueLoginPage()
        if type == "ios":
            return IOSHaiXueLoginPage()
