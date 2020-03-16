# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime

import allure
from selenium import webdriver

from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage
from utils.operation_mysql import Mysql


class MainStaionRegisterPage(MainStationBasePage):
    """
    主站注册页面
    """
    _email_input = Element(css=".reg-input.emailautocomplete", describe="邮箱输入地址")
    _switch_password_span = Element(css="#togglePassword", describe="对密码输入框显示切换")
    _password_input = Element(css=".reg-input.reg-psw", describe="密码输入框")
    _phone_input = Element(css="#mobile", describe="手机号输入框")
    _phone_auth_input = Element(css=".reg-input.reg-mobAuth", describe="手机验证码输入框")
    _phone_auth_get_input = Element(css="#obtainMobileAuthCode", describe="获取手机验证码")
    _sku_focus_div = Element(css="#registerForm>div.reg-btns>div", describe="关注考试")
    _sku_agree_input = Element(css="#agreeBtn", describe="同意协议")
    _agreetment_a = Element(css="#registerForm>div:nth-child(16)>span>a:nth-child(1)", describe="嗨学网用户协议")
    _privacy_agreetment_a = Element(css="#registerForm>div:nth-child(16)>span>a:nth-child(2)", describe="嗨学网隐私协议")
    _done_button = Element(css="#doneBtn", describe="完成按钮")

    @allure.step("输入注册信息并完成")
    def register(self, email, password, phone, auth_code, sku):
        self._email_input = email
        self._password_input = password
        self._phone_input = phone
        self.chang_attr()
        self._phone_auth_input = auth_code
        self.get_focus_sku(sku)
        self._sku_agree_input.click()
        self._done_button.click()

    @allure.step("将手机验证码输入框变成可输入")
    def chang_attr(self):
        js = "$('#mobileAuthCode').removeAttr('disabled')"
        self.driver.execute_script(js)

    @allure.step("获取当日手机验证码")
    def get_phone_auth_code(self):
        now_date = str(datetime.now().strftime("%Y-%m-%d"))

        sql = f"""
        SELECT code from highso.universalcode WHERE openingdate={now_date};
        """
        my = Mysql()
        my.connect_db()
        code = my.execute_sql(sql)
        # print(code)
        return code

    @allure.step("根据SKU选择关注对应的考试项目")
    def get_focus_sku(self, sku):
        locate = self.driver.find_element_by_css_selector(self._sku_focus_div)
        locate.find_element_by_xpath(f"//a[text()='{sku}']").click


#
# if __name__ == "__main__":
#     driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
#     driver.maximize_window()
#
#     driver.get("http://w1.highso.com.cn/v5")
#     sleep(3)
#     from pages.main_station.main_station_home_page import MainStationHomePage
#
#     aa = MainStationHomePage(driver)
#     page = aa.go_to_regster_page()
#     page.get_phone_auth_code()
#     # page.register("3456712@qq.com", "123456", "19983279999", "123456", "sss")