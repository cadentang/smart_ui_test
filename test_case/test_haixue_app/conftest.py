# # -*- coding: utf-8 -*-
import os
import time
from datetime import datetime

import pytest
import allure

from common.appium_driver import AppiumDriver
from common.selenium_pages import PageScreenShot
from utils.base_path import ERROR_PICTURE_PATH
from utils.global_variable import get_value, judg_dicit
from pages.haixue_app.haixue_app_base_page import HaiXueBasePageFactory

# 本地调试可设置该URL
debug_desired_caps = {
    "platformName": "Android",
    "platformVersion": "10",
    "deviceName": "device",
    "appPackage": "com.haixue.app.android.HaixueAcademy.h4",
    "appActivity": "com.haixue.academy.main.WelcomeActivity",
    # "noReset": True,
    "unicodeKeyboard": True,
    "resetKeyboard": True
}

globle_arg = get_value("config_dict")

@pytest.fixture(scope="session", autouse=True)
def get_driver():
    global driver, login_page
    desired_caps = {}
    platform_type = "andriod"
    with allure.step("启动appium的driver"):
        # 如果全局变量字典为{}则代表使用调式模式
        if judg_dicit():
            if globle_arg["platform_type"] == "andriod":
                platform_type = "Andriod"
            elif globle_arg["platform_type"] == "ios":
                platform_type = "IOS"
            else:
                ValueError("platform_type类型错误")

            desired_caps = {
                "platformName": platform_type,
                "platformVersion": "10",
                "deviceName": "device",
                "appPackage": "com.haixue.app.android.HaixueAcademy.h4",
                "appActivity": "com.haixue.academy.main.WelcomeActivity",
                # "noReset": True,
                "unicodeKeyboard": True,
                "resetKeyboard": True
            }

            driver = AppiumDriver(url=get_value("selenium_grid"),
                                  platform_type=platform_type,
                                  implicitly_wait=globle_arg["time_out"],
                                  desired_caps=desired_caps).driver()
            # 切换环境，进入登录页面
            base_page = HaiXueBasePageFactory(driver, platform_type).page
            base_page.allow_perssion()
            login_page = base_page.to_login_page()
            login_page.switch_env(get_value("env"))

        else:
            driver = AppiumDriver(url="http://127.0.0.1:4723/wd/hub",
                                  platform_type="andriod",
                                  implicitly_wait=10,
                                  desired_caps=debug_desired_caps).driver()
            # 切换环境，进入登录页面
            base_page = HaiXueBasePageFactory(driver, platform_type).page
            base_page.allow_perssion()
            login_page = base_page.to_login_page().page
            login_page.switch_env("stage")
        # login_page.login("19983271081", "123456")
    yield driver, login_page

    with allure.step("关闭app"):
        time.sleep(1)
        driver.close_app()




# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """错误自动截图到报告中"""
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == 'call' or report.when == "setup":
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


