# -*- coding: utf-8 -*-
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage


@pytest.fixture(scope="function", autouse=True)
def go_to_question_page(get_driver, login_for_class):
    """测试问答中心相关功能时每个用例执行前自动执行"""
    global question_page
    question_page = MainStationHomePage(get_driver).go_question()

    yield question_page

    MainStationHomePage(get_driver).go_course()
