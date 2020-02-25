# -*- coding: utf-8 -*-
import allure
from pages.main_station.main_station_home_page import MainStationHomePage


@allure.feature("官网功能测试，导航栏、栏目及sku")
class TestMainStationHome:

    @allure.story("上导航未登录状态下点击及数据对比测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_top_nav_not_login(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        for i in home_page.get_not_login_home_top_navigation().values():
            home_page.traverse_page(i)

    @allure.story("下导航点击及数据对比测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_bottom_nav(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        for i in home_page.get_home_bottom_navigation().values():
            home_page.traverse_page(i)

    @allure.story("sku点击及数据对比测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_sku(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        for i in home_page.get_sku().values():
            home_page.traverse_page(i)