# -*- coding: utf-8 -*-
import allure
import pytest
import time

from data.main_station.main_station_login_data import main_station_login_data
from business.main_statin.main_station_login_business import MainStationLoginBusiness
from utils.get_log import logger


@allure.feature("主站登录测试用例")
class TestMainStationLogin:

    @allure.story("测试登录成功")
    @allure.title("测试手机号码登录成功")
    @allure.description_html("主站登录，手机号登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_phone_logion_success(self, get_driver):
        logger.info("=====开始运行登录=====")
        MainStationLoginBusiness(get_driver).login("19983271081", "123456")
        time.sleep(2)
        assert "/course/progressive/index.do" in get_driver.current_url
        logger.info("=====结束运行登录=====")

    def testcase_01(self):
        time.sleep(2)
        print('这里是testcase_01')

    def testcase_02(self):
        time.sleep(4)
        print('这里是testcase_02')

    def testcase_03(self):
        time.sleep(5)
        print('这里是testcase_03')

    def testcase_04(self):
        time.sleep(9)
        print('这里是testcase_04')






