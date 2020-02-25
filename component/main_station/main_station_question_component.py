# -*- coding: utf-8 -*-
from time import sleep

import allure
from selenium import webdriver

from common.selenium_pages import PageSwitchWindowOrFrame
from common.web_component import BaseWebComponents
from common.element import Element


class MainStationQuestionComponent(BaseWebComponents):
    """
    问题组件，适用于问答中心-我的问题列表、问答精华列表、提问问题关联列表，
    题库-题目解析关联的问答列表
    """
    _dianzan_svg = Element(css="#iconwenda-dianzan", describe="点赞")
    _collect_svg = Element(css="iconwenda-shoucang", describe="收藏")
    _question_content_span = Element(css="h3>div>span:nth-child(2)", describe="提问的内容")
    _question_button_span = Element(css="h3>div>span:nth-child(3)", describe="显示详情和收起按钮")
    _question_content_span = Element(css="h3>div>span:nth-child(2)", describe="老师回答的内容")
    _question_content_li = Element(css="div>ul>li.ant-rate-star.ant-rate-star-zero", describe="评分的星星")
    _question_rate_content_span = Element(css="h3>div>span:nth-child(2)", describe="评分标签")
    _question_content_input = Element(css="h3>div>span:nth-child(2)", describe="评分内容输入框")
    _question_content_button = Element(css="div>button", describe="提交按钮")

    def __init__(self, driver: webdriver, component_location):
        """
        :param driver:
        :param component_location: 组件定位信息,为一个dict，如{"xpath": "*//div/a"]
        """
        self.component_location = component_location
        super().__init__(driver)
        self.component_element = self.driver.find_element(*self.component_location)
        # self.component_element = self.driver.find_element(*self.component_location)

    @allure.step("点赞")
    def dianzan(self):
        self.component_element.find_element(*self._dianzan_svg).click()

    @allure.step("收藏")
    def collect(self):
        self.component_element.find_element(*self._collect_svg).click()

    @allure.step("评分, 根据分数及评价内容评分")
    def score(self, score, content):
        self.component_element.find_element(self._question_content_li).click()
        self.component_element.find_element(self._question_content_input).send_keys(content)
        self.component_element.find_element(self._question_content_button).click()

    @allure.step("查看问答详情")
    def question_detail(self):
        pass


    def judge_is_answer(self):
        """判断问题老师是否回答"""
        pass



# if __name__ == "__main__":
#     driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
#     driver.maximize_window()
#
#     driver.get("http://w1.highso.com.cn/v5")
#     # driver.find_element_by_css_selector()
#     sleep(3)
#     from pages.main_station.main_station_home_page import MainStationHomePage
#
#     aa = MainStationHomePage(driver)
#     aa.go_to_login_page().to_login("haixue", "19983271083", "123456")
#     # aa.get_bottom_list_navigations()
#     # aa.logout()
