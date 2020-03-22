# -*- coding: utf-8 -*-
from time import sleep

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By

from common.selenium_pages import PageSwitchWindowOrFrame
from common.web_component import BaseWebComponents
from common.element import Element


class MainStationLiveListComponent(BaseWebComponents):
    """单条直播信息组件，适用于直播课表、查看更多课程及直播模块详情页处， 注意定位组件必须为单个"""

    # 直播的开始时间
    _live_start_time_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__time--')]")
    # 直播老师名字
    _live_teacher_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__teachers')]")
    # 直播标签
    _live_tag_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__tag')]")
    # 直播名称
    _live_name_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__title--')]")
    # 互动标签
    _live_interactive_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__interactive')]")
    # 科目
    _live_subject_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subTitle')]")
    # 直播关联的模块
    _live_module_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subject')]")
    # 无讲义
    _live_no_lecture_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveLecture-index__lectureStatus')]")
    # 有讲义
    _live_have_lecture_div = (By.XPATH, "//span[contains(text(), '讲义')]")
    # 是否未看
    _live_no_watched_span = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveStatus-index__')]")
    # 直播状态
    _live_status_div = (By.XPATH, "//div[starts-with(@class, 'src-components-MyCenter-LiveButton-index__actionBlock')]")
    # 直播回放按钮
    _live_playback_button = (By.XPATH, "//div/button[contains(text(),'直播回放')]")
    # 直播预约成功
    _live_subscribe_button = (By.XPATH, "//div/button[contains(text(),'直播预约')]")
    # 预约成功按钮
    _live_subscribe_success_button = (By.XPATH, "//div/button[contains(text(),'预约成功')]")
    # 进入直播间按钮
    _live_go_button = (By.XPATH, "//div/button[contains(text(),'进入直播')]")
    # 按钮
    _live_button = (By.XPATH, "//div/button")

    def __init__(self, driver: webdriver, component_location):
        """
        :param driver:
        :param live_id:直播ID
        :param component_location: 组件定位信息,为一个dict，如{"xpath": "*//div/a"]
        """
        # self.live_id = live_id
        self.component_location = component_location
        super().__init__(driver)
        self.component_element = self.driver.find_element(*self.component_location)

    def get_live_detail(self):
        """
        通过定位的组件获取直播详细信息
        直播时间：live_start_time
        直播名称：live_name
        直播老师：live_teacher
        直播模块：live_module
        直播标签：live_mark
        精进标签：interactive_mark
        直播科目：live_subject
        直播讲义：live_lecture
        直播状态：live_status
        观看状态：watch_status
        """
        live_date = self.component_element.get_attribute("data-date")
        live_start_time = self.component_element.find_element(*self._live_start_time_div).text
        live_name = self.component_element.find_element(*self._live_name_div).text
        live_teacher = self.component_element.find_element(*self._live_teacher_div).text
        live_module = self.component_element.find_element(*self._live_module_div).text
        live_mark = self.component_element.find_element(*self._live_tag_div).text
        interactive_mark = self.component_element.find_element(*self._live_interactive_div).text
        live_subject = self.component_element.find_element(*self._live_subject_div).text
        live_status = self.component_element.find_element(*self._live_button).text
        watch_status = self.component_element.find_element(*self._live_no_watched_span).text
        print(live_date)
        print(live_start_time)
        print(live_teacher)
        print(live_module)
        print(live_mark)
        print(interactive_mark)
        print(live_subject)
        print(live_status)
        print(watch_status)

    @allure.step("进入模块详情页")
    def go_to_model_detail_page(self):
        MainStationLiveListComponent._live_module_div.click()

        window_handle = PageSwitchWindowOrFrame(self.driver)
        handles = self.driver.window_handles
        sleep(1)
        for handle in handles:
            if window_handle.current_window != handle:
                window_handle.switch_handle(handle)
                sleep(1)
        from pages.main_station.main_station_live_video_module_page import MainStationLiveModulePage

        return MainStationLiveModulePage(self.driver)

    @allure.step("下载讲义")
    def download_lecture(self):
        MainStationLiveListComponent._live_lecture_div.click()

    @allure.step("判断讲义状态")
    def judge_lecture(self):
        pass

    @allure.step("进入直播间")
    def go_to_live_room(self):
        pass

    @allure.step("进入直播回放页面")
    def go_to_live_playback(self):
        pass

    @allure.step("获取直播是否为展示互动的直播, 如果是则点击按钮，关闭弹窗")
    def judge_hudong_live(self):
        pass



if __name__ == "__main__":
    driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("http://w2.highso.com.cn/v5")
    # driver.find_element_by_css_selector()
    sleep(3)
    from pages.main_station.main_station_home_page import MainStationHomePage

    aa = MainStationHomePage(driver)
    aa.go_to_login_page().to_login("haixue", "19983271083", "123456")
    sleep(2)
    location = (By.XPATH, "//div/section/main/div/main/div[1]/div[1]/div[3]/div/div/div[15]")
    com = MainStationLiveListComponent(aa.driver, (By.XPATH, "//div/section/main/div/main/div[1]/div[1]/div[3]/div/div/div[15]"))
    com.get_live_detail()
    # aa.get_bottom_list_navigations()
    # aa.logout()
