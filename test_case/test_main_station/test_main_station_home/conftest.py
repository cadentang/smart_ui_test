# -*- coding: utf-8 -*-
import time
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage


@pytest.fixture(scope="function", autouse=True)
def home_page(get_driver):
    """浏览器输入url访问相应的网站"""
    time.sleep(2)
    get_home_page = MainStationHomePage(get_driver)
    yield get_home_page