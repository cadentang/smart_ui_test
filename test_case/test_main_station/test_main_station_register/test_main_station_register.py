# # -*- coding: utf-8 -*-
import allure
import pytest

from pages.main_station.main_station_home_page import MainStationHomePage
from pages.main_station.main_station_register_page import MainStaionRegisterPage


@allure.feature("主站注册")
class TestRegister:

    @allure.story("注册成功")
    @allure.title("用户选择sku")
    @allure.description_html("主站注册，注册信息：{}".format(get_register_data()))
    @allure.severity(allure.severity_level.CRITICAL)
    # @pytest.mark.parametrize("register_data", get_register_data())
    def test_register_sku_success(self):
        # print(get_register_data())
        self.driver = BasePage.get_driver()
        self.operation_element = SeleniumPage(self.driver)
        RegisterPage.register(self.driver, get_register_data())
        is_exist = self.operation_element.find_element(PersonalCenterPage.name_strong)
        assert is_exist
