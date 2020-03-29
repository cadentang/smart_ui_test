# -*- coding: utf-8 -*-
import os
import threading

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome import options

from common.base_driver import BaseDriver
from utils.get_log import logger
from utils.base_path import DRIVER_PATH, DOWNLOAD_LECTURE_PATH

CHROME_DRIVER_PATH = DRIVER_PATH + '\\chrome\\'
IEDRIVER_PATH = DRIVER_PATH + '\\ie\\'
FIREFOX_PATH = DRIVER_PATH + '\\firefox\\'
SAFARI_PATH = DRIVER_PATH + '\\safari\\'


class SeleniumDriver(BaseDriver):
    """selenium driver类"""
    def __init__(self, maximize_window=True, implicitly_wait=10,
                 selenium_grid_url=None,browser_type="chrome",
                 version=None, pattern="local", platform="win", user_port="win"):

        self.browser_type = browser_type
        self.platform = platform

        # 如果version为空，则给每个类型的浏览器设定一个默认版本
        if browser_type == "chrome" and version == None:
            self.version = "79"
        elif browser_type == "firefox" and version == None:
            self.version = "72"
        elif browser_type == "ie" and version == None:
            self.version = "11"
        elif browser_type == "safari" and version == None:
            self.version = "13"
        else:
            self.version = version

        self.selenium_grid_url = selenium_grid_url
        self.maximize_window = maximize_window
        self.implicitly_wait = implicitly_wait
        self.pattern = pattern
        self.user_port = user_port

    def driver(self):
        """实例化返回一个driver"""
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": DOWNLOAD_LECTURE_PATH}
        chromeOptions.add_experimental_option("prefs", prefs)
        # print(f"self.browser_type: {self.browser_type}")
        # print(f"self.version: {self.version}")
        # print(f"self.platform: {self.platform}")
        if self.pattern == "local":
            if self.browser_type == "chrome":
                self.driver = webdriver.Chrome(executable_path=self.get_driver_path(self.browser_type,
                                                                                    self.version, self.platform),
                                               chrome_options=chromeOptions)
            elif self.browser_type == "firefox":
                self.driver = webdriver.Firefox(executable_path=self.get_driver_path(self.browser_type,
                                                                                     self.version, self.platform))
            elif self.browser_type == "ie":
                self.driver = webdriver.Ie(executable_path=self.get_driver_path(self.browser_type,
                                                                                self.version, self.platform))
            elif self.browser_type == "safari":
                self.driver = webdriver.Safari(executable_path=self.get_driver_path(self.browser_type,
                                                                                    self.version, self.platform))
            else:
                raise ValueError(f"暂不支持{self.browser_type}该浏览器!")

        elif self.pattern == "distributed":
            self.driver = webdriver.Remote(command_executor=self.selenium_grid_url,
                                           desired_capabilities=self.get_selenium_desired_capabilities(
                                               self.browser_type, self.user_port))
        else:
            raise ValueError(f"暂不支持{self.pattern}该浏览器!")

        self.driver.implicitly_wait(self.implicitly_wait)

        if self.maximize_window:
            self.driver.maximize_window()

        return self.driver

    def get_driver_path(self, browser_type, version, platform):
        """根据浏览器类型及版本获取不同的driver路径"""

        if browser_type == "chrome":
            driver_path = self.judge_path(CHROME_DRIVER_PATH, version, platform)
            return driver_path
        elif browser_type == "firefox":
            driver_path = self.judge_path(FIREFOX_PATH, version, platform)
            return driver_path
        elif browser_type == "ie":
            driver_path = self.judge_path(IEDRIVER_PATH, version, platform)
            return driver_path
        elif browser_type == "safari":
            driver_path = self.judge_path(SAFARI_PATH, version, platform)
        else:
            raise ValueError(f"目前暂不支持browser_type：{browser_type}浏览器")

    def judge_path(self, browser_path, version, platform):
        """判断driver的path及版本"""
        if browser_path is None:
            raise ValueError(f"浏览器driver的路径{browser_path}不存在")

        if version is None:
            raise ValueError("浏览器版本不能为空")

        if platform not in ["win", "mac", "linux"]:
            raise ValueError(f"driver支持的平台{platform}错误")

        if os.path.isdir(browser_path):
            driver_files = os.listdir(browser_path)
            driver_path = None
            if len(driver_files) != 0:
                for driver_file in driver_files:
                    if platform in driver_file and version in driver_file:
                        driver_path = browser_path + "\\" + driver_file
                    else:
                        continue
                    if driver_path is not None:
                        return driver_path
                    else:
                        raise ValueError(f"在路径{browser_path}下找不到平台{platform}和版本{version}对应的driver")
            else:
                raise ValueError(f"browser_path路径为空，请检查路径：{browser_path}下是否有相应driver")
        else:
            raise ValueError(f"browser_path：{browser_path}不是目录")

    def set_chrome_option(self):
        """暂时不要使用此功能，有bug"""
        options = webdriver.ChromeOptions()
        prefs = {}
        # 避免密码提示框的弹出
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-infobars')  # 禁止策略化
        options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--incognito')  # 隐身模式（无痕模式）
        options.add_argument('--disable-javascript')  # 禁用javascript
        options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 手动指定使用的浏览器位置

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()

    def get_driver(self):
        return self.driver()
    # __instance = None  # 定义一个类属性
    # __instance_lock = threading.Lock()  # 加锁
    #
    # def get_driver(self):
    #     with self.__instance_lock:
    #         if not self.__instance:
    #             self.__instance = self.driver()
    #     return self.__instance

    def get_selenium_desired_capabilities(self, browser, platform, version=""):
        """获取selenium grid desired_capabilities"""
        if platform == "win":
            capabilities = {
                "browserName": browser, # 浏览器名称
                "version": version, # 浏览器版本
                "platform": "windows", # node节点所处在的平台
                "javascriptEnabled": True
            }
        elif platform == "mac":
            capabilities = {
                "browserName": browser, # 浏览器名称
                "version": version, # 浏览器版本
                "platform": "mac", # node节点所处在的平台
                "javascriptEnabled": True
            }
        else:
            logger.info("未知的平台信息")
            raise ValueError("未知的平台信息")
        return capabilities