# # -*- coding: utf-8 -*-
import os
import time
import pytest
import allure

from common.appium_driver import AppiumDriver
from common.selenium_pages import PageScreenShot
from pages.haixue_app.haixue_app_base_page import HaiXueBasePageFactory


@pytest.fixture(scope="function", autouse=True)
def go_to_logout(get_appium_driver):
    """登录功能,用例执行后退出登录"""

    yield
    get_appium_driver[1].switch_my_page().page.go_set_page().page.logout()





