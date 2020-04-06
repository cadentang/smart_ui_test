# -*- coding: utf-8 -*-
import allure
from selenium.webdriver.common.by import By
from common.appium_pages import AppiumPages
from common.element import Element
from pages.haixue_app.haixue_app_base_page import HaiXueBasePage


# 嗨学课堂APP题库页
class HaiXueExamPage(HaiXueBasePage):

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type


class AndriodHaiXueExamPage(HaiXueExamPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class IOSHaiXueExamPage(HaiXueExamPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueExamPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueExamPage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueExamPage(self.driver, self.type)