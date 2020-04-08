# -*- coding: utf-8 -*-
import time
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from common.appium_pages import AppiumPages
from pages.haixue_app.haixue_app_base_page import HaiXueBasePage
from common.element import Element
from data.haixue_app.haixue_app_login_data import login_data


# 嗨学课堂APP登录页面
class HaiXueLoginPage(HaiXueBasePage):
    _phone_input = None  # 用户名输入框
    _password_input = None # 密码输入框
    _login_button = None  # 登录按钮
    _register_textview = None  # 注册按钮
    _forget_textview = None  # 忘记密码按钮

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @allure.step("登录")
    def login(self, phone, password):
        # self.driver.find_element(*self._phone_input).click()
        # qk = self.driver.find_element(*self._phone_input).text
        # print("qk===:" + qk)
        # if len(qk) >0:
        #     self.driver.keyevent(123)
        #     for i in range(0, len(qk)):
        #         # 67退格键
        #         self.driver.keyevent(67)
        # phone = self.driver.find_element(*self._phone_input)
        # phone.clear()
        # phone.send_keys(phone)
        self.driver.find_element(*self._phone_input).clear()
        self.driver.find_element(*self._phone_input).send_keys(phone)
        self.driver.find_element(*self._password_input).send_keys(password)
        self.driver.find_element(*self._login_textview).click()
        time.sleep(1)
        from pages.haixue_app.haixue_app_found_page import HaiXueFoundPageFactory
        return HaiXueFoundPageFactory(self.driver, self.type)

    @allure.step("去注册密码页面")
    def to_register_page(self):
        self.driver.find_element(*self._register_textview).click()
        from pages.haixue_app.haixue_app_register_page import HaiXueRegisterPageFactory
        return HaiXueRegisterPageFactory(self.driver, self.type)

    @allure.step("去忘记密码页面")
    def to_forget_page(self):
        self.driver.find_element(*self._forget_textview).click()
        from pages.haixue_app.haixue_app_forget_page import HaiXueForgetPageFactory
        return HaiXueForgetPageFactory(self.driver, self.type)

    @allure.step("判断是否登录成功")
    def is_login_success(self):
        try:
            self.driver.find_element(*self._login_textview)
            return False
        except NoSuchElementException:
            return True


class AndriodHaiXueLoginPage(HaiXueLoginPage):
    _phone_input = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/et_username")
    _password_input = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/et_password")
    _register_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/tv_register")
    _forget_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/tv_forget_password")
    _login_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/btn_login")
    _env_textview = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/tv_host")  # 登录页环境信息


    # 环境信息切换页面
    _test0_text_view = (By.XPATH, "//*[@text='测试环境W0']")
    _reg_text_view = (By.XPATH, "//*[@text='测试环境W1']")
    _stage_text_view = (By.XPATH, "//*[@text='测试环境W2']")
    _prod_text_view = (By.XPATH, "//*[@text='正式环境']")
    _swicth_env_text_view = (By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/tv_change")  # 切换环境

    def __init__(self, driver, type):
        super().__init__(driver, type)

    @allure.step("切换测试环境")
    def switch_env(self, env):
        if env == "test0":
            traget_env = "测试环境W0"
        elif env == "reg":
            traget_env = "测试环境W1"
        elif env == "stage":
            traget_env = "测试环境W2"
        elif env == "prod":
            traget_env = "正式环境"
        else:
            ValueError(f"环境参数{env}错误！")

        try:
            if self.driver.find_element(*self._env_textview).get_attribute("text") == traget_env:
                return self
            else:
                self.driver.find_element(*self._env_textview).click()
                time.sleep(1)
                self.driver.find_element(*(By.ID, f"//*[@text={traget_env}]")).click()
                time.sleep(3)
                return self
        except NoSuchElementException:
            print("====开始切换环境====")
            time.sleep(3)
            set_page = self.login("18780127566", "123456").page.switch_my_page().page.go_set_page().page
            set_page.go_dev_tools_page()
            set_page.set_debug()
            self.driver.back()
            time.sleep(1)
            set_page.logout()
            self.driver.close_app()
            self.driver.start_activity('com.haixue.app.android.HaixueAcademy.h4', 'com.haixue.academy.main.WelcomeActivity')

            time.sleep(3)
            if self.driver.find_element(*self._env_textview).get_attribute("text") == traget_env:
                return self
            else:
                self.driver.find_element(*self._env_textview).click()
                time.sleep(1)
                traget_env_element = (By.XPATH, f"//*[@text='{traget_env}']")
                self.driver.find_element(*traget_env_element).click()
                self.driver.find_element(*self._swicth_env_text_view).click()
                time.sleep(3)
                return self


class IOSHaiXueLoginPage(HaiXueLoginPage):

    def __init__(self, driver, type):
        super().__init__(driver, type)


class HaiXueLoginPageFactory:

    def __init__(self, driver, type):
        self.driver = driver
        self.type = type

    @property
    def page(self):
        if self.type == "andriod":
            return AndriodHaiXueLoginPage(self.driver, self.type)
        if self.type == "ios":
            return IOSHaiXueLoginPage(self.driver, self.type)


def aaa():
    # from appium import webdriver
    # from pages.haixue_app.haixue_app_base_page import HaiXueBasePageFactory
    # desired_caps = {}
    # desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
    # desired_caps['platformVersion'] = '10' #android系统的版本号
    # desired_caps['deviceName'] = 'device' #手机设备名称，通过adb devices 查看
    # desired_caps['appPackage'] = 'com.haixue.app.android.HaixueAcademy.h4' #apk的包名
    # desired_caps['appActivity'] = 'com.haixue.academy.main.WelcomeActivity' #apk的launcherActivity
    # desired_caps['unicodeKeyboard'] = True # 使用unicodeKeyboard的编码方式来发送字符串
    # desired_caps['resetKeyboard'] = True  # # 将键盘给隐藏起来
    # desired_caps['reset'] = True  # # 将键盘给隐藏起来
    # driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    # # driver.find_element().get_attribute()
    # # driver.back()
    # andriod_page = HaiXueBasePageFactory(driver, "andriod").page
    # andriod_page.allow_perssion()
    # time.sleep(1)
    # login_page = andriod_page.to_login_page().page
    # time.sleep(1)
    # # cc = login_page.switch_env("stage")
    #
    # time.sleep(3)
    # # driver.find_element(*(By.ID, "com.haixue.app.android.HaixueAcademy.h4:id/et_username")).clear()

    # cc.login("19983271081", "123456")
    # found_page = login_page.login("19983271081", "123456").page
    # time.sleep(1)
    # found_page.close_popup_windows()
    # time.sleep(1)
    # found_page.go_live_calendar()
    import json
    ac = '{"platformName": "Android","platformVersion": "10"}'
    print(json.loads(ac))


if __name__ == "__main__":
    aaa()