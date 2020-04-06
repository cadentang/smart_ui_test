# -*- coding: utf-8 -*-
import os
import time
import threading

import allure
from appium import webdriver
from selenium.webdriver.common.by import By


from common.base_driver import BaseDriver
from utils.get_log import logger
from utils.get_desired_caps import get_desired_caps


class AppiumDriver(BaseDriver):
    """appium driver类"""
    def __init__(self, url, platform_type, desired_caps, implicitly_wait=10):
        """
        :param desired_caps:配置项，是一个dict
        :param url: appium服务地址或者selenium grid地址
        :param implicitly_wait:超时等待时间
        :param platform_type:平台andriod/iOS
        """
        # desired_caps = {
        #     "platformName": "",
        #     "platformVersion": "",
        #     "deviceName": "",
        #     "app": "",
        #     "appPackage": "",
        #     "appActivity": "",
        #     "noReset": False,
        #     "udid": "",
        #     "unicodeKeyboard": True,
        #     "resetKeyboard": True
        # }
        self.url = url
        self.implicitly_wait = implicitly_wait
        self.pattern = platform_type
        self.desired_caps = desired_caps
        self.appium_driver=webdriver.Remote(self.url, self.desired_caps)
        self.appium_driver.implicitly_wait(10)

    def driver(self):
        """实例化返回一个driver"""
        return self.appium_driver

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()

    def get_driver(self):
        return self.driver()

    def check(self, package_name):
        """
        j检查设备是否安装了APP
        :package_name: 包名
        :return:True/False
        """
        return self.appium_driver.is_app_installed(package_name)

    @allure.step("为设备安装APP")
    def install(self, app_path):
        """
        :param app_path: APP安装包路径
        :return:
        """
        if self.check() == False:
            self.appium_driver.install_app(app_path)
            logger.info(f"安装app成功，安装路径{app_path}")
        else:
            ValueError("APP已经安装，请检查")

    @allure.step("为设备卸载APP")
    def remove(self, package_name):
        """
        :param package_name:
        :return:
        """
        if self.check():
            self.appium_driver.remove_app(package_name)
            logger.info("卸载APP成功")
        else:
            ValueError("该设备未安装该APP，请检查")

    def reset(self, app_id):
        """重置应用"""
        self.driver.reset()


