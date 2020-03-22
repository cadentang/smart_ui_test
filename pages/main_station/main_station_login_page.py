# -*- coding: utf-8 -*-
from time import sleep
import allure
from selenium.webdriver.common.by import By
from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage


class MainStationLoginPage(MainStationBasePage):
    """主站登录页"""
    _login_form = (By.XPATH, "//div/form")  # 登录的form

    # 密码登录方式
    _passwprd_login_div = Element(xpath="//div/div[contains(text(), '密码登录')]", describe="密码登录方式切换")
    # _username_input = Element(xpath="//*[@id='tab1.account']", describe="用户名输入框")
    # _password_input = Element(xpath="//*[@id='tab1.password']", describe="密码输入框")

    _username_input = Element(xpath="//*[@id='j_username']", describe="用户名输入框")
    _password_input = Element(xpath="//*[@id='j_password']", describe="密码输入框")

    # 短信登录方式
    _message_login_div = Element(xpath="//div/div[contains(text(), '短信登录')]", describe="短信登录方式切换")
    _phone_input = Element(xpath="//*[@id='tab2.account']", describe="手机号输入框")
    _get_code_div = Element(xpath="//span/div[contains(text(), '获取验证码')]", describe="获取验证码")
    _phone_code_input = Element(xpath="//input[@id='tab2.smsCode']", describe="短信验证码输入框")

    # _login_button = Element(xpath="//div/span/button", describe="登录按钮")
    _login_button = Element(xpath="//div/div[1]/div/div[2]/form/div[4]/div/div/span/button", describe="登录按钮")
    _regster_button = Element(xpath="//div/a[contains(text(),'注册')]", describe="注册按钮")
    _password_message_p = Element(xpath="//*[@id='root']/div/div[1]/div/div[2]/form/div[2]/div/div/div",
                               describe="密码框错误提示标签")
    _username_error_message_p = Element(xpath='//*[@id="root"]/div/div[1]/div/div[2]/form/div[1]/div/div/div',
                                  describe="用户名错误提示标签")
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
        sleep(2)
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

    @allure.step("进入嗨学网用户协议")
    def go_useragreement(self):
        pass

    @allure.step("进入用户隐私协议")
    def go_privacy(self):
        pass
