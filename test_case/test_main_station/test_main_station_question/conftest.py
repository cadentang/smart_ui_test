# -*- coding: utf-8 -*-
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage
from data.main_station.main_station_business_data import login_course_data


@pytest.fixture(scope="class", autouse=True)
def go_to_question_page(get_driver):
    """测试问答中心相关功能时每个用例执行前自动执行"""
    global question_page
    course_page = MainStationHomePage(get_driver).go_to_login_page().to_login(login_course_data["login_type"],
                                                                login_course_data["phone"],
                                                                login_course_data["password"])
    question_page = course_page.go_question()

    yield question_page
    question_page.logout()


@pytest.fixture(scope="function", autouse=False)
def go_to_question(go_to_question_page):
    """测试问答中心相关功能时每个用例执行后自动执行, 回到问答中心"""

    yield go_to_question_page
    go_to_question_page.go_question()
