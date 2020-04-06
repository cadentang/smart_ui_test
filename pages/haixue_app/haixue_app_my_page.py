# -*- coding: utf-8 -*-
import allure
import time
from selenium.webdriver.common.by import By
from common.element import Element
from pages.haixue_app.haixue_app_base_page import HaiXueBasePage


# 嗨学课堂APP我的页面
class HaiXueMyPage(HaiXueBasePage):
    _set_imageview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/iv_set")

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @allure.step("我的页面_进入设置页面")
    def go_set_page(self):
        self.driver.find_element(*self._set_imageview).click()
        print("===进入我的设置页面===")
        time.sleep(1)
        from pages.haixue_app.haixue_app_set_page import HaiXueSetPageFactory
        return HaiXueSetPageFactory(self.driver, self.type)


class AndriodHaiXueMyPage(HaiXueMyPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class IOSHaiXueMyPage(HaiXueMyPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueMyPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueMyPage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueMyPage(self.driver, self.type)