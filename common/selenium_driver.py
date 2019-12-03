# -*- coding: utf-8 -*-
import os
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

from common.base_driver import BaseDriver
from utils.get_log import logger
from utils.base_path import DRIVER_PATH

CHROME_DRIVER_PATH = DRIVER_PATH + '\\chrome\\'
IEDRIVER_PATH = DRIVER_PATH + '\\ie\\'
FIREFOX_PATH = DRIVER_PATH + '\\firefox\\'


class SeleniumDriver(BaseDriver):

    def __init__(self, maximize_window=True, implicitly_wait=10, selenium_grid_url=None,
                 browser_type="chrome", version=None, pattern="local"):
        self.selenium_grid_url = selenium_grid_url
        self.maximize_window = maximize_window
        self.implicitly_wait = implicitly_wait
        self.browser_type = browser_type
        self.version = version
        self.pattern = pattern

    def driver(self):
        """实例化返回一个driver"""
        if self.pattern == "local":
            if self.browser_type == "chrome":
                self.driver = webdriver.Chrome(executable_path=self.get_driver_path(self.browser_type, self.version))
            elif self.browser_type == "firefox":
                self.driver = webdriver.Firefox(executable_path=self.get_driver_path(self.browser_type, self.version))
            elif self.browser_type == "ie":
                self.driver = webdriver.Ie(executable_path=self.get_driver_path(self.browser_type, self.version))
            else:
                logger.info("不支持该浏览器!")

        elif self.pattern == "distributed":
            if self.browser_type == "chrome":
                self.driver = webdriver.Remote(command_executor=self.selenium_grid_url,
                                               desired_capabilities=DesiredCapabilities.CHROME)
            elif self.browser_type == "firefox":
                self.driver = webdriver.Remote(command_executor=self.selenium_grid_url,
                                               desired_capabilities=DesiredCapabilities.FIREFOX)
            elif self.browser_type == "ie":
                self.driver = webdriver.Remote(command_executor=self.selenium_grid_url,
                                               desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
            else:
                logger.info(f"不支持{self.browser_type}浏览器!")
        else:
            logger.info(f"不支持{self.pattern}模式运行！")

        self.driver.implicitly_wait(self.implicitly_wait)

        if self.maximize_window:
            self.driver.maximize_window()

        return self.driver

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()

    def get_driver_path(self, browser_type="chrome", version=None):
        """根据浏览器类型及版本获取不同的driver路径"""

        if browser_type == "chrome" and version == None:
            driver_path = CHROME_DRIVER_PATH + "\chromedriver_win_78.0.3904.70.exe"
            return driver_path
        elif browser_type == "chrome" and version is not None:
            driver_path = self.judge_path(CHROME_DRIVER_PATH, version)
            return driver_path
        elif browser_type == "firefox" and version == None:
            driver_path = self.judge_path(FIREFOX_PATH, version)
            return driver_path
        elif browser_type == "firefox" and version is not None:
            driver_path = self.judge_path(FIREFOX_PATH, version)
            return driver_path
        elif browser_type == "ie" and version == None:
            driver_path = self.judge_path(FIREFOX_PATH, version)
            return driver_path
        elif browser_type == "ie" and version is not None:
            driver_path = self.judge_path(FIREFOX_PATH, version)
            return driver_path
        else:
            logger.error(f"目前暂不支持browser_type：{browser_type}浏览器")

    def judge_path(self, browser_path, version):
        """判断driver的path及版本"""
        if version is not None:
            if os.path.isdir(browser_path):
                driver_files = os.listdir(browser_path)
                if len(driver_files) != 0:
                    for driver_file in driver_files:
                        if driver_file == version:
                            driver_path = browser_path + "\\" + driver_file
                            return driver_path
                else:
                    logger.error("browser_path路径不存在或为空，请检查路径：{}下是否有相应driver".
                                 format(browser_path))
            else:
                logger.error("browser_path：{}不是目录".format(browser_path))
        else:
            if os.path.isdir(browser_path):
                driver_files = os.listdir(browser_path)
                if len(driver_files) != 0:
                    driver_version = max(driver_files)
                    driver_path = browser_path + "\\" + driver_version
                    return driver_path
                else:
                    logger.error("browser_path路径不存在或为空，请检查路径：{}下是否有相应driver".
                                 format(browser_path))
            else:
                logger.error("browser_path：{}不是目录".format(browser_path))

    def get_browser_and_diver_relation(self, browser, browser_version):
        """获取浏览器版本和driver版本的对应关系"""
        pass


# if __name__ == "__main__":
#     selenium_driver = SeleniumDriver().get_driver_path()
#     print(selenium_driver)
