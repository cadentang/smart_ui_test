# -*- coding: utf-8 -*-
from time import sleep
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from common.element import Element, Elements
from common.selenium_pages import SeleniumPages, PageMouse
from utils.global_variable import get_value


class MainStationBasePage(SeleniumPages):
    """登录后的公共元素"""
    # 顶导航
    _haixue_logo_image = Element(css="a>img[alt='logo']", describe="嗨学logo")
    # _categoryid_a = Element(xpath="*//div[starts-with(@class,'src-components-Wrap-UserHeader')]/a/strong",
    #                         describe="当前类别")
    _categoryid_a = (By.XPATH, "*//div[starts-with(@class,'src-components-Wrap-UserHeader')]/a/strong")
    _categoryids_ul = Elements(xpath=" *//div[starts-with(@class,'src-components-Wrap-UserHeader')]/ul",
                              describe="该用户拥有的所有类别")
    _message_svg = Element(css="div>a>span>svg", describe="消息中心")
    # _user_icon_a = Element(css="div>a[href='/v5/setting/user']", describe="用户信息")
    _user_icon_a = (By.CSS_SELECTOR, "div>a[href='/v5/setting/user")
    _user_account_a = Element(css="a[href='/customerInfo/findCustomerById.do']", describe="账号设置")
    _user_help_a = Element(css="a[href='/v5/help-center']", describe="帮助中心")
    _user_back_haixue_a = Element(css="a[href='/v5']", describe="返回官网")
    _user_logout_a = Element(css="a[href='/logout.do']", describe="退出登录")

    # 左导航
    _jj_a = Element(css="a[href='/course/progressive/index.do']", describe="精进页面")
    _course_a = Element(css="a[href='/v5/my/course']", describe="课程")
    _exam_data_a = Element(css="a[href='/v5/my/exam-data']", describe="资料")
    _exam_a = Element(css="a[href='/exam/home/index.do']", describe="题库")
    _question_a = Element(css="a[href='/v5/my/question']", describe="问答")
    _message_a = Element(css="a[href='/v5/my/message']", describe="资讯")
    _order_a = Element(css="a[href='/order/myOrder/findOrderListForCustomer.do']", describe="订单")
    _purchase_a = Element(css="a[href='/v5/my/purchase']", describe="选购")
    # _question_no_read_span = Element(css="a[href='/v5/my/question']>span:nth-child(3)", describe="问答未读数量")
    _question_no_read_span = (By.CSS_SELECTOR, "a[href='/v5/my/question']>span:nth-child(3)")


    # 右侧快捷键
    _connection_head_teacher_a = Element(css="#root>div>section>main>aside>a", describe="联系班主任")
    _back_old_version_a = Element(css="main>div>main>aside>a:nth-child(1)", describe="返回旧版")
    _feedback_a = Element(css="main>div>main>aside>a:nth-child(2)", describe="产品吐槽")
    _zhuanfu_a = Element(css=".specific-teacher-wrap", describe="专辅")

    # 底导航
    _bottom_config_li = "//*[@id='root']/div/section/div/footer/div/div[1]/ul/li" # 获取底部的一级导航
    _bottom_first_h3 = "//*[@id='root']/div/section/div/footer/div/div[1]/ul/li/h3" # 获取底部的一级导航标题
    _bottom_second_a = "//*[@id='root']/div/section/div/footer/div/div[1]/ul/li/h3/p/a" # 获取底部二级导航

    @allure.step("切换类别")
    def switch_category(self, category_name):
        mouse = PageMouse(self.driver)
        mouse.move_to_element(self._categoryid_a)
        category_location = f"//a[text()='{category_name}']"
        self.driver.find_element_by_xpath(category_location).click()

    @allure.step("进入消息中心")
    def go_message_center(self):
        PageMouse(self.driver).move_to_element(self._user_icon_a)
        self._message_svg.click()
        from pages.main_station.main_station_home_page import MainStationHomePage
        return MainStationHomePage(self.driver)

    @allure.step("进入帮助中心")
    def go_help_center(self):
        PageMouse(self.driver).move_to_element(self._user_icon_a)
        self._user_help_a.click()
        from pages.main_station.main_station_home_page import MainStationHomePage
        return MainStationHomePage(self.driver)

    @allure.step("进入官网")
    def go_official_website(self):
        PageMouse(self.driver).move_to_element(self._user_icon_a)
        self._user_back_haixue_a.click()
        from pages.main_station.main_station_home_page import MainStationHomePage
        return MainStationHomePage(self.driver)

    @allure.step("退出登录")
    def logout(self):
        PageMouse(self.driver).move_to_element(self._user_icon_a)
        sleep(2)
        self._user_logout_a.click()
        # # 目前推出登录后还是调的老接口，返回的是老页面，先通过直接输入URL返回登录页，V5重构完成后去掉此部分代码
        # now_url = self.driver.current_url
        # # aa = "http://w1.highso.com.cn/indexCourse/indexLogin.do?logout=true"
        # target_url = now_url.split("indexCourse")[0] + 'v5'
        # self.driver.get(target_url)

        from pages.main_station.main_station_home_page import MainStationHomePage
        return MainStationHomePage(self.driver)

    @allure.step("进入个人中心页面")
    def go_course(self):
        # try:
        #     sleep(2)
        #     self._course_a.click()
        # except:
        #     self.driver.get(self.driver.current_url.spilt("course")[0] + "v5/my/course")
        sleep(2)
        self._course_a.click()
        from pages.main_station.main_station_course_page import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    def go_course_url(self):
        """通过URL进入个人中心页"""
        sleep(3)
        self.driver.get(self.driver.current_url.split("course")[0] + "v5/my/course")
        from pages.main_station.main_station_course_page import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    @allure.step("进入资料下载页面")
    def go_material(self):
        self._exam_data_a.click()
        from pages.main_station.main_station_exam_data import MainStationExamDataPage
        return MainStationExamDataPage(self.driver)

    @allure.step("进入题库页面")
    def go_exam(self):
        self._exam_a.click()
        from pages.main_station.main_station_exam_page import MainStationExamPage
        return MainStationExamPage(self.driver)

    @allure.step("进入问答页面")
    def go_question(self):
        self._question_a.click()
        from pages.main_station.main_station_question_page import MainStationQuestionPage
        return MainStationQuestionPage(self.driver)

    @allure.step("进入资讯页面")
    def go_message(self):
        self._message_a.click()
        from pages.main_station.main_station_message_page import MainStationMessagePage
        return MainStationMessagePage(self.driver)

    @allure.step("进入订单页面")
    def go_order(self):
        self._order_a.click()
        from pages.main_station.main_station_order_page import MainStationOrderPage
        return MainStationOrderPage(self.driver)

    @allure.step("进入选购页面")
    def go_purchase(self):
        self._purchase_a.click()
        from pages.main_station.main_station_purchase_page import MainStationPurchasePage
        return MainStationPurchasePage(self.driver)

    @allure.step("进入精进页面")
    def go_jj_page(self):
        self._jj_a.click()
        from pages.main_station.main_station_jj_page import MainStationJJPage
        return MainStationJJPage(self.driver)

    def get_bottom_list_navigations(self):
        """获取底部一级和二级导航"""
        lis = self.driver.find_elements_by_xpath(self._bottom_config_li)
        navigations_dict = {}
        for i in lis:
            d = i.find_element_by_css_selector("h3")
            tmp_list = []
            f = i.find_elements_by_css_selector("p>a")
            for i in range(len(f)):
                tmp_list.append({f[i].text, f[i].get_attribute("href")})
            navigations_dict[d.text] = tmp_list
        return navigations_dict

    def get_no_read_question(self):
        """获取未读数量"""
        return self.driver.find_element(*self._question_no_read_span).text

# if __name__ == "__main__":
#     driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
#     driver.maximize_window()
#     driver.get("http://w2.highso.com.cn/v5")
#     print(driver.current_url)
#     # driver.find_element_by_css_selector()
#     sleep(3)
#     from pages.main_station.main_station_home_page import MainStationHomePage
#
#     aa = MainStationHomePage(driver)
#     aa.go_to_login_page().to_login("haixue", "19983271083", "123456")
#     # aa.get_bottom_list_navigations()
#     sleep(1)
#     # aa.switch_category("二级建造师")
#     sleep(1)
#     aa.logout()

