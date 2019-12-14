# -*- coding: utf-8 -*-
import allure
from selenium import webdriver

from common.element import Element
from common.selenium_pages import SeleniumPages


class MainStationHomePage(SeleniumPages):
    """主站首页"""
    learn_center_a = Element(xpath="//a[contains(text(),'学习中心')]", describe="学习中心进入登录链接")
    login_a = Element(xpath="//a[contains(text(),'登录')]", describe="首页登录链接")
    regster_a = Element(xpath="//div/a[contains(text(),'注册')]", describe="首页注册链接")

    @allure.step("首页进入登录页面")
    def go_to_login_page(self):
        self.login_a.click()
        from pages.main_station.main_station_login_page import MainStationLoginPage
        return MainStationLoginPage(self.driver)

    @allure.step("登录后首页进入课程页面")
    def go_to_course_page(self):
        self.learn_center_a.click()
        from pages.main_station.main_station_course_page  import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    @allure.step("首页进入注册页面")
    def go_to_regster_page(self):
        self.regster_a.click()
        from pages.main_station.main_station_register_page import MainStaionRegisterPage
        return MainStaionRegisterPage(self.driver)




