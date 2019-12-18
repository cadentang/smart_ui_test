# -*- coding: utf-8 -*-
from time import sleep
import allure
from common.element import Element
from common.selenium_pages import SeleniumPages


class MainStationLoginPage(SeleniumPages):
    """主站登录页"""
    _username_input = Element(xpath="//*[@id='j_username']",
                              describe="用户名输入框")
    _password_input = Element(xpath="//*[@id='j_password']",
                              describe="密码输入框")
    _login_button = Element(xpath="//div/div[2]/form/div[3]/div/div/span/button",
                            describe="登录按钮")
    _regster_button = Element(xpath="[//div/a[contains(text(),'注册')]",
                              describe="注册按钮")
    _error_message_p = Element(css="div.index-loginBox.index-loginBoxCheck>.index-loginHint",
                               describe="错误信息标签")
    _auto_login_input = Element(id_="autoLogon", describe="自动登录")
    _forget_login_a = Element(xpath="//a[starts-with(@class,'loginFormForgot')]",
                              describe="忘记密码")

    @allure.step("登录成功")
    def to_course_page(self, username, password):
        self._username_input = username
        self._password_input = password
        self._login_button.click()
        from pages.main_station.main_station_course_page import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    @allure.step("登录失败")
    def to_login_failure(self, username, password):
        self._username_input = username
        self._password_input = password
        self._login_button.click()
        return self

    @allure.step("登录")
    def to_login(self, user_type, username, password):
        self._username_input = username
        self._password_input = password
        self._login_button.click()
        sleep(2)
        if user_type == "jj":
            from pages.main_station.main_station_jj_page import MainStationJJPage
            return MainStationJJPage(self.driver)
        else:
            from pages.main_station.main_station_course_page import MainStationCoursePage
            return MainStationCoursePage(self.driver)

    # 老主站
    # username_input = Element(css=".index-loginInput.index-loginInputUser", describe="用户名输入框")
    # password_input = Element(css=".index-loginInput.index-loginInputPwd", describe="密码输入框")
    # login_button = Element(css=".index-loginBtn.index-loginBtn--login", describe="登录按钮")
    # regster_button = Element(css=".index-loginBtn.index-loginBtn--pwd", describe="注册按钮")
    # error_message_p = Element(css="div.index-loginBox.index-loginBoxCheck>.index-loginHint", describe="错误信息标签")
