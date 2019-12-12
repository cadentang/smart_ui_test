# -*- coding: utf-8 -*-
import time
import pytest
from selenium import webdriver
from common.selenium_driver import SeleniumDriver
from utils.global_variable import get_value

# 本地调试可设置该URL
MAIN_STATION_URL = "http://w2.highso.com.cn"

@pytest.fixture(scope="function", autouse=True)
def get_driver():
    global driver

    globle_arg = get_value("config_dict")
    if globle_arg is not None:
        driver = SeleniumDriver(browser_type=globle_arg["browser"], version=globle_arg["version"], implicitly_wait=globle_arg["time_out"],
                                pattern=globle_arg["pattern"]).driver()
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

    time.sleep(5)
    driver.quit()
