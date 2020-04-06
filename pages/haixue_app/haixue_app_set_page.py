# -*- coding: utf-8 -*-
import time

import allure
from selenium.webdriver.common.by import By
from common.element import Element
from pages.haixue_app.haixue_app_base_page import HaiXueBasePage


# 嗨学课堂APP设置页面
class HaiXueSetPage(HaiXueBasePage):
    _safe_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/txt_change_psw")
    _notify_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/rl_notify")
    _clear_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/rl_clear_cache")
    _dev_tools_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/dev_tools")  # 开发工具
    _safe_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/rl_privacy")
    _about_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/rl_about")
    _privacy_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/rl_privacy")
    _logout_button = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/bt_login")  # 退出登录
    _logout_ok_btuuon = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/btn_ok")  # 任性退出

    # 开发工具设置页面
    _now_env_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/change_env")  # 当前环境
    _debug_checkbox = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/debug_mode_checked")  # debug模式


    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @allure.step("设置页面_进入开发工具设置页面")
    def go_dev_tools_page(self):
        self.driver.find_element(*self._dev_tools_textview).click()
        print("===进入开发工具设置页面===")
        time.sleep(1)

    @allure.step("设置debug模式")
    def set_debug(self):
        time.sleep(1)
        print(self.driver.find_element(*self._debug_checkbox).get_attribute("checked"))
        if self.driver.find_element(*self._debug_checkbox).get_attribute("checked") == "false":
            self.driver.find_element(*self._debug_checkbox).click()
            return 1
        else:
            return 1

    @allure.step("退出登录")
    def logout(self):
        self.driver.find_element(*self._logout_button).click()
        time.sleep(1)
        self.driver.find_element(*self._logout_ok_btuuon).click()
        time.sleep(1)
        from pages.haixue_app.haixue_app_login_page import HaiXueLoginPageFactory
        return HaiXueLoginPageFactory(self.driver, self.type)


class AndriodHaiXueSetPage(HaiXueSetPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)



class IOSHaiXueSetPage(HaiXueSetPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueSetPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueSetPage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueSetPage(self.driver, self.type)