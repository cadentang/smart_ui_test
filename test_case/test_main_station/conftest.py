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
from utils.get_parser import get_arg
from utils.get_log import logger
from pages.main_station.main_station_home_page import MainStationHomePage
from data.main_station.main_station_business_data import login_study_data

# # 本地调试可设置该URL
MAIN_STATION_URL = "http://w2.highso.com.cn/v5"
driver = None

globle_arg = get_value("config_dict")
logger.info(f"platform: {get_value('platform')}")
logger.info(globle_arg)


@pytest.fixture(scope="session", autouse=True)
def get_driver():
    """启动相应的浏览器，获得一个driver实例"""
    global driver
    with allure.step("启动浏览器"):
        # 如果全局变量字典为{}则代表使用调式模式，默认使用MAIN_STATION_URL环境
        # local模式代表selenium服务器和浏览器在本地运行
        # distributed模式代表selenium-grid方式运行
        if judg_dicit():
            if globle_arg["pattern"] == "local":
                driver = SeleniumDriver(browser_type=globle_arg["browser"],
                                        version=globle_arg["version"],
                                        implicitly_wait=globle_arg["time_out"],
                                        pattern=globle_arg["pattern"],
                                        platform=get_value("platform")).driver()
            elif globle_arg["pattern"] == "distributed":
                # selenium_grid方式运行
                print("===========:" + str(get_arg()))
                print("===========:" + get_arg()["user_port"])
                driver = SeleniumDriver(browser_type=globle_arg["browser"],
                                        version=globle_arg["version"],
                                        implicitly_wait=globle_arg["time_out"],
                                        pattern="distributed",
                                        platform=get_value("platform"),
                                        selenium_grid_url=get_value("selenium_grid"),
                                        user_port=get_arg()["user_port"]).driver()
        else:
            driver = SeleniumDriver().driver()
            # driver.get(MAIN_STATION_URL)
        if judg_dicit():
            driver.get(globle_arg["env_config"]["main_station_url"])
        else:
            driver.get(MAIN_STATION_URL)
        globle_driver = driver

    yield driver
    with allure.step("关闭浏览器"):
        time.sleep(1)
        driver.quit()

# @pytest.fixture(scope="function", autouse=True)
# def get_url():
#     """浏览器输入url访问相应的网站"""
#     time.sleep(2)
#     if judg_dicit():
#         driver.get(globle_arg["env_config"]["main_station_url"])
#     else:
#         driver.get(MAIN_STATION_URL)

@pytest.fixture(scope="function", autouse=False)
def login_for_function(get_driver):
    """在每个函数执行前登录，需主动调用"""
    MainStationHomePage(get_driver).go_to_login_page().to_login(login_study_data["login_type"], login_study_data["phone"],
                                                                login_study_data["password"])
    # 登录之后如果是精进用户则重新定向到新的V5个人中心页，待精进页面迁移后调整这里
    time.sleep(1)
    if "/course/progressive/index.do" in get_driver.current_url:
        if judg_dicit():
            get_driver.get(globle_arg["env_config"]["main_station_url"] + "/my/course")
        else:
            get_driver.get(MAIN_STATION_URL + "/my/course")
    yield login_for_function
    MainStationHomePage(get_driver).logout()

@pytest.fixture(scope="class", autouse=False)
def login_for_class(get_driver):
    """在每个class执行前登录，执行后登出，需主动调用"""
    time.sleep(1)
    if "/course/progressive/index.do" in get_driver.current_url:
        if judg_dicit():
            get_driver.get(globle_arg["env_config"]["main_station_url"] + "/my/course")
        else:
            get_driver.get(MAIN_STATION_URL + "/my/course")
    MainStationHomePage(get_driver).go_to_login_page().to_login(login_study_data["login_type"], login_study_data["phone"],
                                                                login_study_data["password"])
    yield login_for_class
    MainStationHomePage(get_driver).logout()

@pytest.fixture(scope="module", autouse=False)
def login_for_module(get_driver):
    """在每个py文件执行前登录，执行后登出，需主动调用"""
    time.sleep(1)
    if "/course/progressive/index.do" in get_driver.current_url:
        if judg_dicit():
            get_driver.get(globle_arg["env_config"]["main_station_url"] + "/my/course")
        else:
            get_driver.get(MAIN_STATION_URL + "/my/course")
    MainStationHomePage(get_driver).go_to_login_page().to_login(login_study_data["login_type"], login_study_data["phone"],
                                                                login_study_data["password"])
    yield login_for_module
    MainStationHomePage(get_driver).logout()

@pytest.fixture(scope="session", autouse=False)
def login_for_session(get_driver):
    """在每个测试session执行前登录, 执行后登出，需主动调用"""
    time.sleep(1)
    if "/course/progressive/index.do" in get_driver.current_url:
        if judg_dicit():
            get_driver.get(globle_arg["env_config"]["main_station_url"] + "/my/course")
        else:
            get_driver.get(MAIN_STATION_URL + "/my/course")
    MainStationHomePage(get_driver).go_to_login_page().to_login(login_study_data["login_type"], login_study_data["phone"],
                                                                login_study_data["password"])
    yield login_for_session
    MainStationHomePage(get_driver).logout()


# @pytest.mark.hookwrapper
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item):
#     """错误自动截图到报告中"""
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == 'call' or report.failed:
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             screen_shot_path = os.path.join(ERROR_PICTURE_PATH, str(datetime.now().strftime("%Y%m%d")))
#             if not os.path.exists(screen_shot_path):
#                 os.makedirs(screen_shot_path)
#             file_name = screen_shot_path + report.nodeid.replace(":", "_").replace("/", "_") + ".png"
#             driver.get_screenshot_as_file(file_name)
#             with open(file_name, mode='rb') as f:
#                 file = f.read()
#             allure.attach(file, "错误截图", allure.attachment_type.PNG)
