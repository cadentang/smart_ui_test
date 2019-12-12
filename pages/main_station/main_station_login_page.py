# -*- coding: utf-8 -*-
from common.element import Element
from common.selenium_pages import SeleniumPages


class MainStationLoginPage(SeleniumPages):
    """主站登录页"""

    # 老主站
    # username_input = Element(css=".index-loginInput.index-loginInputUser", describe="用户名输入框")
    # password_input = Element(css=".index-loginInput.index-loginInputPwd", describe="密码输入框")
    # login_button = Element(css=".index-loginBtn.index-loginBtn--login", describe="登录按钮")
    # regster_button = Element(css=".index-loginBtn.index-loginBtn--pwd", describe="注册按钮")
    # error_message_p = Element(css="div.index-loginBox.index-loginBoxCheck>.index-loginHint", describe="错误信息标签")

    username_input = Element(xpath="//*[@id='j_username']", describe="用户名输入框")
    password_input = Element(xpath="//*[@id='j_password']", describe="密码输入框")
    login_button = Element(xpath="//div/div[2]/form/div[3]/div/div/span/button", describe="登录按钮")
    regster_button = Element(xpath="[//div/a[contains(text(),'注册')]", describe="注册按钮")
    error_message_p = Element(css="div.index-loginBox.index-loginBoxCheck>.index-loginHint", describe="错误信息标签")
    auto_login_input = Element(id_="autoLogon", describe="自动登录")
    forget_login_a = Element(xpath="//a[starts-with(@class,'loginFormForgot')]", describe="忘记密码")

    def to_course_page(self, username, password):
        """登录成功进入课程页面"""
        self.username_input = username
        self.password_input = password
        self.login_button.click()
        from pages.main_station.main_station_course_page import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    def to_login_failure(self, username, password):
        """登录失败"""
        self.username_input = username
        self.password_input = password
        self.login_button.click()
        return self


