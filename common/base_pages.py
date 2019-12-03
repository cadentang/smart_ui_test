# -*- coding: utf-8 -*-
__author__ = 'caden'
import os
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from appium.webdriver.common.touch_action import TouchAction as MobileTouchAction

from utils.get_log import logger


class BasePages:

    def __init__(self, driver):
        self.time = 3
        self.t = 1
        self.driver = driver

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)




