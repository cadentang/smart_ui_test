# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime

import pytest
import allure
from selenium import webdriver

from common.selenium_driver import SeleniumDriver
from common.selenium_pages import PageScreenShot
from utils.base_path import ERROR_PICTURE_PATH
from utils.global_variable import get_value, judg_dicit

# # 本地调试可设置该URL
MAIN_STATION_URL = "http://w0.highso.com.cn/v5"
driver = None

globle_arg = get_value("config_dict")


@pytest.fixture(scope="module", autouse=True)
def get_driver():
    global driver
    with allure.step("启动浏览器"):
        # 如果全局变量字典为{}则代表使用调式模式，默认使用test0环境
        if judg_dicit():
            driver = SeleniumDriver(browser_type=globle_arg["browser"],
                                    version=globle_arg["version"],
                                    implicitly_wait=globle_arg["time_out"],
                                    pattern=globle_arg["pattern"],
                                    platform=get_value("platform")).driver()
        else:
            driver = SeleniumDriver().driver()
            driver.get(MAIN_STATION_URL)
    # webdriver.Remote(command_executor="http://39.107.127.90:9999/wd/hub", desired_capabilities={
    #                               'platform': 'windows',
    #                               'browserName': 'chrome',
    #                               'version': '',
    #                               'javascriptEnabled': True,
    #                               'webdriver.chrome.driver': 'D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_78.exe'
    #                           })
    yield driver

    with allure.step("关闭浏览器"):
        time.sleep(1)
        driver.quit()

@pytest.fixture(scope="function", autouse=True)
def get_url():
    """浏览器输入url"""
    time.sleep(2)
    if judg_dicit():
        driver.get(globle_arg["env_config"]["main_station_url"])
    else:
        driver.get(MAIN_STATION_URL)

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """错误自动截图到报告中"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_shot_path = os.path.join(ERROR_PICTURE_PATH, str(datetime.now().strftime("%Y%m%d")))
            if not os.path.exists(screen_shot_path):
                os.makedirs(screen_shot_path)
            file_name = screen_shot_path + report.nodeid.replace(":", "_").replace("/", "_") + ".png"
            driver.get_screenshot_as_file(file_name)
            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, "错误截图", allure.attachment_type.PNG)
