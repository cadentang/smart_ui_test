# -*- coding: utf-8 -*-
import allure

@allure.epic("登录")
@allure.feature("登录")
class TestHaixueAppLogin:

    @allure.story("登录-手机号登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_app_login_phone_success(self, get_driver):
        # get_driver.login_page.login("19983271081", "123456")
        # print(get_driver)
        get_driver[1].login("19983271081", "123456")
        assert get_driver[1].is_login_success()

    @allure.story("登录-邮箱登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_app_login_email_success(self, get_driver):
        # get_driver.login_page.login("19983271081", "123456")
        # print(get_driver)
        get_driver[1].login("19983271081", "123456")
        assert get_driver[1].is_login_success()

    @allure.story("登录-学习卡登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_app_login_card_success(self, get_driver):
        # get_driver.login_page.login("19983271081", "123456")
        # print(get_driver)
        get_driver[1].login("19983271081", "123456")
        assert get_driver[1].is_login_success()