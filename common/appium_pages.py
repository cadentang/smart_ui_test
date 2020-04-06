# -*- coding: utf-8 -*-
import os

import allure
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium import webdriver

from common.base_pages import BasePages
from utils.get_log import logger


class AppiumPages(BasePages):
    """封装常用操作"""

    def __init__(self, driver):
        super().__init__(driver)

    def get_size(self):
        """获取屏幕尺寸"""
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    @allure.step("两点滑动，向左滑")
    def swipe_left(self):
        l = self.get_size()
        x1 = int(l[0] * 0.9)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.1)
        logger.info("两点滑动，向左滑")
        self.driver.swipe(x1, y1, x2, y1, 1000)

    @allure.step("两点滑动，向右滑")
    def swipe_right(self):
        l = self.get_size()
        x1 = int(l[0] * 0.9)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.1)
        logger.info("两点滑动，向右滑")
        self.driver.swipe(x1, y1, x2, y1, 1000)


    @allure.step("两点滑动，向上滑")
    def swipe_up(self):
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.8)
        y2 = int(l[1] * 0.2)
        logger.info("两点滑动，向上滑")
        self.swipe(x1, y1, x1, y2, 1000)

    def touch_action(self, num, **point):
        """多点连续滑动,3点以上"
        for i in range(num):
            TouchAction(self.driver).press(x=262, y=385).wait(2000) \
                .move_to(x=451, y=388).wait(1000) \
                .move_to(x=650, y=589).wait(1000) \
                .move_to(x=649, y=785).wait(1000) \
                .release().perform()
        """
        len = len(point)

    @allure.step("两点滑动，向下滑")
    def swipe_down(self):
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.2)
        y2 = int(l[1] * 0.8)
        logger.info("两点滑动，向下滑")
        self.swipe(x1, y1, x1, y2, 1000)

    @allure.step("两点滑动，随意两点滑动")
    def swipe_random(self, x1, y1, x2, y2):
        logger.info("两点滑动，随意两点滑动")
        # l = self.get_size()
        self.swipe(x1, y1, x2, y2, 1000)

    @allure.step("缩小屏幕")
    def pinch(self):
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        pinch_action = MultiAction(self.driver)
        l = self.get_size()
        action1.press(x=l[0] * 0.2, y=l[1] * 0.2).wait(1000).move_to(x=l[0] * 0.4, y=l[1] * 0.4).wait(1000).release()
        action2.press(x=l[0] * 0.8, y=l[1] * 0.8).wait(1000).move_to(x=l[0] * 0.6, y=l[1] * 0.6).wait(1000).release()

        pinch_action.add(action1, action2)
        logger.info("缩小屏幕")
        pinch_action.perform()

    @allure.step("放大屏幕")
    def zoom(self):
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        zoom_action = MultiAction(self.driver)
        l = self.get_size()

        action1.press(x=l[0] * 0.4, y=l[1] * 0.4).wait(1000).move_to(x=l[0] * 0.2, y=l[1] * 0.2).wait(1000).release()
        action2.press(x=l[0] * 0.6, y=l[1] * 0.6).wait(1000).move_to(x=l[0] * 0.8, y=l[1] * 0.8).wait(1000).release()

        zoom_action.add(action1, action2)
        logger.info("放大屏幕")
        zoom_action.perform()

    def get_contexts(self):
        """获取当前页面的所有的环境,为一个list"""
        return self.appium_driver.contexts

    @allure.step("切换到h5上下文")
    def switch_h5(self, target_context):
        # 获取当前context
        now_context = self.appium_driver.current_context
        if now_context != target_context and target_context in self.get_contexts():
            self.appium_driver.switch_to.context(target_context)
        elif target_context not in self.get_contexts():
            logger.info("目标环境不存在")
        else:
            logger("当前环境为目标环境")

    @allure.step("切换到原生APP上下文")
    def switch_native(self):
        self.appium_driver.switch_to.context("NATIVE_APP")


