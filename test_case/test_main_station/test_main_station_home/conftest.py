# -*- coding: utf-8 -*-
import time
import pytest
from utils.global_variable import get_value, judg_dicit
from pages.main_station.main_station_home_page import MainStationHomePage
MAIN_STATION_URL = "http://w2.highso.com.cn/v5"
driver = None

globle_arg = get_value("config_dict")


# @pytest.fixture(scope="function", autouse=True)
# def get_url(get_driver):
#     """浏览器输入url访问相应的网站"""
#     time.sleep(2)
#     if judg_dicit():
#         get_driver.get(globle_arg["env_config"]["main_station_url"])
#     else:
#         get_driver.get(MAIN_STATION_URL)