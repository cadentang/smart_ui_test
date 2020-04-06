# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from common.appium_pages import AppiumPages
from common.element import Element


class HaiXueForgetPage(AppiumPages):
    pass


class AndriodHaiXueForgetPage(HaiXueForgetPage):
    pass


class IOSHaiXueForgetPage(HaiXueForgetPage):
    pass


class HaiXueForgetPageFactory:

    def __init__(self, driver):
        self.driver = driver

    def page(self, type):
        if type == "andriod":
            return AndriodHaiXueForgetPage(self.driver)
        if type == "ios":
            return IOSHaiXueForgetPage(self.driver)