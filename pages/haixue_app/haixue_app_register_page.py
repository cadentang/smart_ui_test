# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from common.appium_pages import AppiumPages
from common.element import Element


class HaiXueRegisterPage(AppiumPages):
    pass


class AndriodHaiXueRegisterPage(HaiXueRegisterPage):
    pass


class IOSHaiXueRegisterPage(HaiXueRegisterPage):
    pass


class HaiXueRegisterPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueRegisterPage(self.driver)
        if self.type == "ios":
            return IOSHaiXueRegisterPage(self.driver)
