# -*- coding: utf-8 -*-
import time
import pytest
from selenium import webdriver
from common.selenium_driver import SeleniumDriver
from utils import global_variable

MAIN_STATION_URL = "http://w2.highso.com.cn"

@pytest.fixture(scope="function", autouse=True)
def get_driver():
    global driver
    globle_arg = global_variable.get_value("config_dict")
    if globle_arg is not None:
        driver = SeleniumDriver(browser_type=globle_arg["browser"], implicitly_wait=globle_arg["time_out"],
                                pattern=globle_arg["pattern"]).driver()
        driver.get(globle_arg["env_config"]["main_station_url"])
    else:
        driver = SeleniumDriver().driver()
        driver.get(MAIN_STATION_URL)
    yield driver

    time.sleep(5)
    driver.quit()
