# # -*- coding: utf-8 -*-
import allure
import pytest

from pages.main_station.main_station_home_page import MainStationHomePage
from pages.main_station.main_station_register_page import MainStaionRegisterPage
from data.main_station.main_station_register_data import get_register_data
from utils.global_variable import get_value

# globle_arg = get_value("config_dict")
#
# @allure.feature("主站注册")
# class TestRegister:
#
#     @allure.story("注册成功")
#     @allure.title("用户选择sku")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_register_sku_success(self, get_driver):
#         regster_page = MainStationHomePage(get_driver).go_to_regster_page()
#         data = get_register_data(globle_arg["env_config"]["main_station_url"])
#         regster_page.register(data["email"], data["pwd"], data["phone"], regster_page.get_phone_auth_code(), data["sku"])
#         assert get_driver.url
#
#     @allure.story("注册失败-选择已注册的账号注册")
#     @allure.title("用户选择sku")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_register_sku_success(self, get_driver):
#         regster_page = MainStationHomePage(get_driver).go_to_regster_page()
#         data = get_register_data(globle_arg["env_config"]["main_station_url"])
#         regster_page.register(data["email"], data["pwd"], data["phone"], regster_page.get_phone_auth_code(), data["sku"])
#         assert is_exist