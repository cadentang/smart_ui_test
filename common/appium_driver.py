# -*- coding: utf-8 -*-
import os
import threading

from appium import webdriver
from common.base_driver import BaseDriver
from utils.get_log import logger
from utils.base_path import DRIVER_PATH
from utils.get_desired_caps import get_desired_caps


class AppiumDriver(BaseDriver):
    """appium driver类"""
    def __init__(self, desired_caps:dict, selenium_grid_url, implicitly_wait=10, platform_type="andriod", version=None,
                 is_simulator=True):
        """
        :param desired_caps:配置项，是一个dict
        :param selenium_grid_url: appium服务地址或者selenium grid地址
        :param implicitly_wait:超时等待时间
        :param platform_type:平台andriod/iOS
        :param version:平台版本
        :param is_simulator:真机运行还是模拟器运行
        """

        self.desired_caps = desired_caps
        self.selenium_grid_url = selenium_grid_url
        self.implicitly_wait = implicitly_wait
        self.pattern = platform_type
        self.version = version
        self.is_simulator = is_simulator

        self.driver=webdriver.Remote(self.selenium_grid_url, self.desired_caps)
        self.driver.implicitly_wait(8)

    def driver(self):
        """实例化返回一个driver"""
        return self.driver

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()

    def get_driver(self):
        return self.driver()

    def install_app(self, app_path):
        """安装app"""
        self.driver.install_app(app_path)

    def remove_app(self, app_id):
        """删除应用"""
        self.driver.remove_app(app_id)

    def reset_app(self, app_id):
        """重置应用"""
        self.driver.reset()