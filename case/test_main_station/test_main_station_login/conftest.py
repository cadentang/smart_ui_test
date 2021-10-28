# -*- coding: utf-8 -*-
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage


@pytest.fixture(scope="function", autouse=False)
def go_to_logout_fixture(get_driver):
    """登录功能用例执行前进入登录页面， 用例执行后退出登录"""

    yield
    now_url = get_driver.current_url
    if "/course/progressive/index.do" in now_url:
        get_driver.get(now_url.split("course")[0] + "/v5/my/course")
    MainStationHomePage(get_driver).logout()
