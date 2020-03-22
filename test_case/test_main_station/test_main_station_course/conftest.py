# -*- coding: utf-8 -*-
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage
from data.main_station.main_station_business_data import login_course_data


@pytest.fixture(scope="function", autouse=False)
def go_to_course_page(get_driver):
    """测试个人中心相关功能时每个用例执行前自动执行"""
    global course_page
    course_page = MainStationHomePage(get_driver).go_to_login_page().to_login(login_course_data["login_type"], login_course_data["phone"],
                                                    login_course_data["password"])

    yield course_page
    course_page.go_course_url()
    course_page.logout()
