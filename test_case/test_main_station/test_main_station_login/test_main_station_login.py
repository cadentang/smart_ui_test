# -*- coding: utf-8 -*-
import time
import allure
import pytest

from data.main_station.main_station_login_data import login_data
from pages.main_station.main_station_home_page import MainStationHomePage
from pages.main_station.main_station_login_page import MainStationLoginPage
from common.selenium_pages import PageScreenShot
from utils.get_log import logger
from utils.global_variable import get_value


@allure.feature("主站登录测试")
class TestMainStationLogin:

    @allure.story("测试登录成功")
    @allure.title("测试手机号码登录成功")
    @allure.description("主站登录，手机号登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("data", login_data["success_phone_data"][0])
    @allure.testcase("https://www.tapd.cn/21492081/sparrow/tcase/view/1121492081001060614?url_cache_key=8662d02ef87d3c98ec427ad7967c7c2b", "正确账号+正确密码登录")
    @allure.link("https://www.tapd.cn/21492081/prong/stories/view/1121492081001051127?url_cache_key=99f5c5016553580e8040b1bc2b0d5cb5&action_entry_type=story_tree_list", "link需求问题链接")
    @allure.issue("https://www.tapd.cn/21492081/sparrow/tcase/view/1121492081001060614?url_cache_key=8662d02ef87d3c98ec427ad7967c7c2b", "bug问题链接")
    def test_phone_logion_success(self, get_driver, data):
        home_page = MainStationHomePage(get_driver)
        page = home_page.go_to_login_page().to_login(data[0], data[1], data[2])
        with allure.step("截图"):
            PageScreenShot(login_data["success_phone_data"][1], get_driver)
        get_driver.get("http://w1.highso.com.cn/v5/my")
        assert "/v5/my" in get_driver.current_url
        page.logout()

    @allure.story("测试登录成功")
    @allure.title("邮箱账号密码正确")
    @allure.description("主站登录，邮箱账号登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", login_data["success_email_data"][0])
    def test_email_logion_success(self, get_driver, data):
        home_page = MainStationHomePage(get_driver)
        page = home_page.go_to_login_page().to_login(data[0], data[1], data[2])
        PageScreenShot(login_data["success_email_data"][1], get_driver)
        get_driver.get("http://w1.highso.com.cn/v5/my")
        assert "/v5/my" in get_driver.current_url
        page.logout()

    @allure.story("测试登录失败")
    @allure.title("测试手机号码不存在登录失败")
    @allure.description("主站登录，测试手机号码不存在登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", login_data["fail_data_phone_error"][0])
    def test_phone_logion_phone_error(self, get_driver, data):
        page = MainStationHomePage(get_driver).go_to_login_page().to_login_failure(data[1], data[2])
        PageScreenShot(login_data["fail_data_phone_error"][1], get_driver)
        assert page._password_message_p.text == "账号或密码错误，请重新输入"

    @allure.story("测试登录失败")
    @allure.title("测试不输入密码登录")
    @allure.description("主站登录，测试不输入密码登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", login_data["not_input_password"][0])
    def test_phone_not_input_password(self, get_driver, data):
        page = MainStationHomePage(get_driver).go_to_login_page().to_login_failure(data[1], data[2])
        PageScreenShot(login_data["not_input_password"][1], get_driver)
        assert page._password_message_p.text == "密码不能为空"

    @allure.story("测试登录失败")
    @allure.title("测试不输入用户名登录")
    @allure.description("主站登录，测试不输入用户名，输入密码")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", login_data["not_input_username"][0])
    def test_phone_not_input_username(self, get_driver, data):
        page = MainStationHomePage(get_driver).go_to_login_page().to_login_failure(data[1], data[2])
        PageScreenShot(login_data["not_input_username"][1], get_driver)
        assert page._username_error_message_p.text == "用户名不能为空"

    @allure.story("测试登录失败")
    @allure.title("测试不输入用户名和密码登录")
    @allure.description("主站登录，测试不输入用户名和密码登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", login_data["not_input_username_password"][0])
    def test_phone_not_input(self, get_driver, data):
        page = MainStationHomePage(get_driver).go_to_login_page().to_login_failure(data[1], data[2])
        PageScreenShot(login_data["not_input_username_password"][1], get_driver)
        assert page._username_error_message_p.text == "用户名不能为空"
        assert page._password_message_p.text == "密码不能为空"

    @allure.story("测试登录失败")
    @allure.title("测试密码错误登录失败")
    @allure.description("主站登录，手机号正确，密码错误,登录失败")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("data", login_data["fail_data_password_error"][0])
    def test_phone_logion_password_error(self, get_driver, data):
        page = MainStationHomePage(get_driver).go_to_login_page().to_login_failure(data[1], data[2])
        PageScreenShot(login_data["fail_data_password_error"][1], get_driver)
        assert page._password_message_p == "账号或密码错误，请重新输入"






