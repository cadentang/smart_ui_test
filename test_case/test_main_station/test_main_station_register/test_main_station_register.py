# # -*- coding: utf-8 -*-
# import allure
# import pytest
#
# from pages.test_main_station.base_page import BasePage
# from pages.test_main_station.home_page import HomePage
# from pages.test_main_station.register_page import RegisterPage
# from pages.test_main_station.personal_center_page import PersonalCenterPage
# from common.selenium_page import SeleniumPage
# from data.test_main_station.register_data import get_register_data
#
#
# @allure.feature("主站注册")
# class TestRegister:
#
#     @allure.story("注册成功")
#     @allure.title("用户选择sku")
#     @allure.description_html("主站注册，注册信息：{}".format(get_register_data()))
#     @allure.severity(allure.severity_level.CRITICAL)
#     # @pytest.mark.parametrize("register_data", get_register_data())
#     def test_register_sku_success(self):
#         # print(get_register_data())
#         self.driver = BasePage.get_driver()
#         self.operation_element = SeleniumPage(self.driver)
#         RegisterPage.register(self.driver, get_register_data())
#         is_exist = self.operation_element.find_element(PersonalCenterPage.name_strong)
#         assert is_exist
#
#     def teardown_method(self):
#         self.driver.close()
#
#
#
