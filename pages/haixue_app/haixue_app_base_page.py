# -*- coding: utf-8 -*-
import time
import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.appium_pages import AppiumPages
from common.element import Element


# 嗨学课堂APP基础页面
class HaiXueBasePage(AppiumPages):
    """嗨学课堂基础页面基础类"""
    _allow_button = None  # 允许APP访问设备信息按钮
    _now_experience_button = None  # 立即体验按钮
    _disagree_button = None  # 不同意嗨学用户协议
    _agree_button = None  # 同意嗨学用户协议

    # 底部tab切换
    _found_tab_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/txt_tab_discover")  # 底部发现页tab
    _course_tab_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/txt_tab_lesson")  # 底部课程页tab
    _exam_tab_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/txt_tab_exam")  # 底部题库tab
    _my_tab_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/txt_tab_me")  # 底部我的tab

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @allure.step("允许APP访问设备信息")
    def allow_perssion(self):
        for i in range(5):
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(self._allow_button))
                e.click()
            except:
                pass

    def isElementPresent(self, driver, by, value):
        try:
            driver.find_element(by=by, value=value)
        except Exception as e:
            # 打印异常信息
            print(e)
            return False
        else:
            return True

    @allure.step("滑动欢迎页面, 进入登录页面")
    def to_login_page(self):

        for i in range(10):
            try:
                self.driver.implicitly_wait(1)
                now_button = self.driver.find_element(*self._now_experience_button)
                now_button.click()
                break
            except NoSuchElementException:
                self.swipe_left()
                continue

        self.driver.implicitly_wait(1)
        time.sleep(1)
        self.driver.find_element(*self._disagree_button).click()
        from pages.haixue_app.haixue_app_login_page import HaiXueLoginPageFactory
        return HaiXueLoginPageFactory(self.driver, self.type)

    @allure.step("进入发现页")
    def switch_found_page(self):
        ele = self.driver.find_element(*self._found_tab_textview)
        if ele.get_attribute("selected") == True:
            pass
        else:
            ele.click()
            from pages.haixue_app.haixue_app_found_page import HaiXueFoundPageFactory
            return HaiXueFoundPageFactory(self.driver, self.type)

    @allure.step("进入课程页")
    def switch_course_page(self):
        ele = self.driver.find_element(*self._course_tab_textview)
        if ele.get_attribute("selected") == True:
            pass
        else:
            ele.click()
            from pages.haixue_app.haixue_app_course_page import HaiXueCoursePageFactory
            return HaiXueCoursePageFactory(self.driver, self.type)

    @allure.step("进入题库页")
    def switch_exam_page(self):
        ele = self.driver.find_element(*self._exam_tab_textview)
        if ele.get_attribute("selected") == True:
            pass
        else:
            ele.click()
            from pages.haixue_app.haixue_app_exam_page import HaiXueExamPageFactory
            return HaiXueExamPageFactory(self.driver, self.type)

    @allure.step("进入我的页面")
    def switch_my_page(self):
        time.sleep(1)
        ele = self.driver.find_element(*self._my_tab_textview)
        if ele.get_attribute("selected") == True:
            pass
        else:
            ele.click()
            print("===进入我的页面===")
            from pages.haixue_app.haixue_app_my_page import HaiXueMyPageFactory
            return HaiXueMyPageFactory(self.driver, self.type)


class AndriodHaiXueBasePage(HaiXueBasePage):
    _allow_button = (By.XPATH, "//*[@text='始终允许']")
    _now_experience_button = (By.XPATH, "//*[@text='立即体验']")
    _disagree_button = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/btn_disagree")
    _agree_button = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/btn_agree")

    def __init__(self, driver, type):
        super().__init__(driver, type)


class IOSHaiXueBasePage(HaiXueBasePage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueBasePageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueBasePage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueBasePage(self.driver, self.type)
