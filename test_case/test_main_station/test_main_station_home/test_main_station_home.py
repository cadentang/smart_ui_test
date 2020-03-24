# -*- coding: utf-8 -*-
import allure
from pages.main_station.main_station_home_page import MainStationHomePage

@allure.epic("官网")
@allure.feature("官网首页")
class TestMainStationHomePage:

    @allure.story("官网首页-上导航")
    @allure.title("官网首页-上导航-未登录状态-点击遍历测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_station_home_top_nav_not_login(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        result = home_page.traverse_top_dav(home_page.get_not_login_home_top_navigation())
        assert len(result) > 0

    @allure.story("官网首页-下导航")
    @allure.title("官网首页-下导航-点击遍历测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_station_home_bottom_nav(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        result = home_page.traverse_page(home_page.get_home_bottom_navigation())
        assert len(result) > 0

    @allure.story("官网首页-sku")
    @allure.title("官网首页-sku-点击遍历测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_statione_home_sku(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        result = home_page.traverse_page(home_page.get_sku())
        assert len(result) > 0


@allure.epic("官网")
@allure.feature("sku详情页测试")
class TestMainStationHomeSkuDetail:
    pass


@allure.epic("官网")
@allure.feature("官网首页上导航详情")
class TestMainStationHomeTopNavDetail:
    pass


@allure.epic("官网")
@allure.feature("官网首页下导航详情")
class TestMainStationHomeBottomNavDetail:
    pass