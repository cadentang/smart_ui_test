# -*- coding: utf-8 -*-
from selenium.webdriver.remote.webdriver import WebDriver
from common.component import Components


class BaseAppComponents:
    """app基础组件"""
    def __init__(self, driver: WebDriver):
        self.driver = driver