# -*- coding: utf-8 -*-
import random
from time import sleep
import allure
from selenium import webdriver
from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage
from common.selenium_pages import PageSwitchWindowOrFrame


class MainStationHomePage(MainStationBasePage):
    """主站首页，包括登录及未登录的页面"""
    _first_navigation_div = "//section/main/header/div/div[2]"  # 未登录顶导航定位
    _sku_li = "*//ul[starts-with(@class, 'src-pages-homepage-index__skuList')]/li"  # 定位一级sku的li标签

    _learn_center_a = Element(xpath="//a[contains(text(),'学习中心')]", describe="学习中心进入登录链接")
    _login_a = Element(xpath="//a[contains(text(),'登录')]", describe="首页登录链接")
    _regster_a = Element(xpath="//div/a[contains(text(),'注册')]", describe="首页注册链接")

    @allure.step("获取顶部导航栏目的活动栏目，包括登录注册")
    def get_not_login_home_top_navigation(self):
        """
        动态获取顶部导航栏的配置, 学习中心为固定栏位
        :return:返回一个dict
        {
            '新闻中心':
                {
                '新闻中心': 'http://w1.highso.com.cn/v5/template/3/5/newslist',
                'location': "//section/main/header/div/div[2]//a[text()='新闻中心']"
                }
        }
        """
        lis = self.driver.find_elements_by_xpath(self._first_navigation_div + "/a")
        top_navigations_dict = {}
        for i in lis:
            tmp_dict = {}
            if "src-components-Wrap-HomeHeader__linkTemplate" in i.get_attribute("class"):
                tmp_dict["url"] = i.get_attribute("href")
            elif "src-components-Wrap-HomeHeader__linkCenter" in i.get_attribute("class"):
                tmp_dict["url"] = i.get_attribute("href")
            else:
                continue
            tmp_dict["location"] = self._first_navigation_div + f"//a[text()='{i.text}']"
            top_navigations_dict[i.text] = tmp_dict
        return top_navigations_dict

    @allure.step("获取底部导航的动态栏目")
    def get_home_bottom_navigation(self):
        lis = self.driver.find_elements_by_xpath(self._bottom_config_li)
        bottom_navigations_dict = {}
        for i in lis:
            d = i.find_element_by_css_selector("h3")
            tmp_dict = {}
            f = i.find_elements_by_css_selector("p>a")
            for i in range(len(f)):
                tmp_dict[f[i].text] = {"url": f[i].get_attribute("href"), "location": self._bottom_config_li + f"//a[text()='{f[i].text}']"}
                bottom_navigations_dict[d.text] = tmp_dict
        return bottom_navigations_dict

    @allure.step("获取sku详情及链接")
    def get_sku(self):
        lis = self.driver.find_elements_by_xpath(self._sku_li)
        sku_dict = {}
        for i in lis:
            d = i.find_element_by_css_selector("h3")
            tmp_dict = {}
            f = i.find_elements_by_css_selector("div>span>a")
            for i in range(len(f)):
                if f[i].text != '':
                    tmp_dict[f[i].text] = {"url": f[i].get_attribute("href"), "location": self._sku_li + f"//a[text()='{f[i].text}']"}
                if d.text != '':
                    sku_dict[d.text] = tmp_dict
        return sku_dict

    @allure.step("遍历上导航")
    def traverse_top_dav(self, target_page_ele_dict):
        """本方法适合上导航遍历"""
        for i in target_page_ele_dict.values():
            # print(i)
            window_handle = PageSwitchWindowOrFrame(self.driver)
            first_handle = window_handle.current_window
            Element(xpath=i["location"]).find(self.driver).click()
            handles = self.driver.window_handles
            sleep(1)
            if len(handles) == 1:
                i["result_url"] = self.driver.current_url
                self.driver.back()
                sleep(1)
            elif len(handles) > 1:
                for handle in handles:
                    if window_handle.current_window !=handle:
                        window_handle.switch_handle(handle)
                        i["result_url"] = self.driver.current_url
                        self.driver.close()
                        window_handle.switch_handle(first_handle)
                        sleep(1)
        return target_page_ele_dict

    @allure.step("根据dict遍历所有的链接, 返回跳转链接的URL")
    def traverse_page(self, target_page_ele_dict):
        """本方法适合sku和下导航遍历"""
        for i in target_page_ele_dict.values():
            # print(i)
            for j in i.values():
                window_handle = PageSwitchWindowOrFrame(self.driver)
                first_handle = window_handle.current_window
                Element(xpath=j["location"]).find(self.driver).click()
                handles = self.driver.window_handles
                sleep(1)
                if len(handles) == 1:
                    j["result_url"] = self.driver.current_url
                    self.driver.back()
                    sleep(1)
                elif len(handles) > 1:
                    for handle in handles:
                        if window_handle.current_window !=handle:
                            window_handle.switch_handle(handle)
                            j["result_url"] = self.driver.current_url
                            self.driver.close()
                            window_handle.switch_handle(first_handle)
                            sleep(1)
        return target_page_ele_dict

    @allure.step("首页进入登录页面")
    def go_to_login_page(self):
        self._login_a.click()
        from pages.main_station.main_station_login_page import MainStationLoginPage
        return MainStationLoginPage(self.driver)

    @allure.step("登录后首页进入课程页面")
    def go_to_course_page(self):
        self._learn_center_a.click()
        from pages.main_station.main_station_course_page  import MainStationCoursePage
        return MainStationCoursePage(self.driver)

    @allure.step("首页进入注册页面")
    def go_to_regster_page(self):
        self._regster_a.click()
        from pages.main_station.main_station_register_page import MainStaionRegisterPage
        return MainStaionRegisterPage(self.driver)


if __name__ == "__main__":
    driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
    driver.maximize_window()
    driver.get("http://w2.highso.com.cn/v5")
    sleep(3)
    from pages.main_station.main_station_home_page import MainStationHomePage
    aa = MainStationHomePage(driver)
    bb = aa.get_sku()
    print(bb)
    print(aa.traverse_page(bb))
    sleep(3)


