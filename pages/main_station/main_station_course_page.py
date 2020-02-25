# -*- coding: utf-8 -*-
import allure
from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage


class MainStationCoursePage(MainStationBasePage):
    """课程页面"""
    _more_course_div = Element(xpath="//div[starts-with(@class, 'src-pages-center-Calendar-index__moreClass')]", describe="更多课程")
    _sign_button = Element(xpath="//div/button[contains(text(),'立即签到')]", describe="签到按钮")

    @allure.step("进入更多课程")
    def go_more_course(self):
        pass

    @allure.step("签到")
    def go_sign(self):
        pass

    @allure.step("进入看课记录页面")
    def go_learn_log(self):
        pass

    @allure.step("进入学习周报页面")
    def go_week_report(self):
        pass

    @allure.step("进入上次学习页面")
    def go_last_learn(self):
        pass

    @allure.step("选择一个或者多个商品显示")
    def choose_goods(self, goods_list):
        pass

    @allure.step("选择科目下的某个阶段的某个模块学习")
    def choose_learn_advice(self):
        pass

    @allure.step("通过全部课程进入模块学习")
    def go_all_course_module(self):
        pass
