# -*- coding: utf-8 -*-
import logging
import allure
import pytest
from data.main_station.main_station_login_data import main_station_login_data
from business.main_statin.main_station_login_business import MainStationLoginBusiness

log = logging.getLogger(__name__)

@allure.feature("主站登录测试用例")
class TestMainStationLogin:

    @allure.story("测试登录成功")
    @allure.title("测试手机号码登录成功")
    @allure.description_html("主站登录，手机号登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_phone_logion_success(self, get_driver):
        log.info("=====开始运行登录=====")
        MainStationLoginBusiness(get_driver).login("19983271081", "123456")
        import time
        time.sleep(2)
        assert "/course/progressive/index.do" in get_driver.current_url
        log.info("=====结束运行登录=====")






