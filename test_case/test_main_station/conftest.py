# -*- coding: utf-8 -*-
import time
import pytest
import allure
from selenium import webdriver
from common.selenium_driver import SeleniumDriver
from utils.global_variable import get_value, judg_dicit

# 本地调试可设置该URL
MAIN_STATION_URL = "http://w0.highso.com.cn/v5"

@pytest.fixture(scope="function", autouse=True)
def get_driver():
    global driver
    with allure.step("启动浏览器"):
        # 如果全局变量字典为{}则代表使用调式模式，默认使用test0环境
        if judg_dicit():
            globle_arg = get_value("config_dict")
            driver = SeleniumDriver(browser_type=globle_arg["browser"], version=globle_arg["version"], implicitly_wait=globle_arg["time_out"],
                                    pattern=globle_arg["pattern"], platform=get_value("platform")).driver()
            driver.get(globle_arg["env_config"]["main_station_url"])
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
        time.sleep(5)
        driver.quit()
