# -*- coding: utf-8 -*-
from common.app import App

class MainStationLoginBusiness:
    """登录业务逻辑封装"""

    def __init__(self, driver):
        self.driver = driver

    def login(self,phone, pwd):
        """
        登录业务操作
        :param phone: 邮箱/手机号/学习卡
        :param pwd: 密码
        :return:
        """
        app = App(self.driver)
        app.main_station_login_page.username_input = phone
        app.main_station_login_page.password_input = pwd
        app.main_station_login_page.login_button.click()