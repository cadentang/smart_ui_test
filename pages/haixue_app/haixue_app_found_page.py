# -*- coding: utf-8 -*-
import allure
from selenium.webdriver.common.by import By
from common.element import Element
from pages.haixue_app.haixue_app_base_page import HaiXueBasePage


class HaiXueFoundPage(HaiXueBasePage):
    _close_button = None  #  精进弹窗关闭按钮
    _live_calendar_textview = None # 直播日历
    _trail_class_textview = None # 体验课
    _punch_card_textview = None # 打开营
    _chapter_refined_textview = None  # 章节精炼
    _daliy_topic_textview = None  # 每日一题
    _look_more_textview = None  # 查看更多

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @allure.step("关闭精进弹窗")
    def close_popup_windows(self):
        self.driver.find_element(*self._close_button).click()

    @allure.step("进入直播日历")
    def go_live_calendar(self):
        self.driver.find_element(*self._live_calendar_textview).click()

    @allure.step("进入体验课")
    def go_trail_class(self):
        self.driver.find_element(*self._trail_class_textview).click()

    @allure.step("进入打卡营")
    def go_punch_card(self):
        self.driver.find_element(*self._punch_card_textview).click()

    @allure.step("进入章节精炼")
    def go_chapter_refined(self):
        self.driver.find_element(*self._chapter_refined_textview).click()

    @allure.step("进入每日一题")
    def go_daliy_topic(self):
        self.driver.find_element(*self._daliy_topic_textview).click()

    @allure.step("查看更多进入直播日历页面")
    def go_more_live(self):
        self.driver.find_element(*self._look_more_textview).click()

    @allure.step("切换sku")
    def switch_sku(self, sku):
        pass

class AndriodHaiXueFoundPage(HaiXueFoundPage):
    _close_button = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/iv_close")
    _live_calendar_textview = (By.XPATH, "//*[@text='直播日历']")
    _trail_class_textview = (By.XPATH, "//*[@text='体验课']")
    _punch_card_textview = (By.XPATH, "//*[@text='打卡营']")
    _chapter_refined_textview = (By.XPATH, "//*[@text='章节精炼']")
    _daliy_topic_textview = (By.XPATH, "//*[@text='每日一题']")
    _look_more_textview = (By.XPATH, "//*[@text='查看更多']")

    def __init__(self, driver, type):
        super().__init__(driver, type)


class IOSHaiXueFoundPage(HaiXueFoundPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueFoundPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueFoundPage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueFoundPage(self.driver, self.type)