# -*- coding: utf-8 -*-
from time import sleep

import allure
from selenium import webdriver

from common.selenium_pages import PageSwitchWindowOrFrame
from common.web_component import BaseWebComponents
from common.element import Element


class MainStationLiveListComponent(BaseWebComponents):
    """单条直播信息组件，适用于直播课表、查看更多课程及直播模块详情页处， 注意定位组件必须为单个"""

    # _live_start_time_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__time--')]",
    #                            describe="直播的开始时间")
    # _live_teacher_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__teachers')]",
    #                         describe="直播老师名称")
    # _live_tag_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__tag')]",
    #                         describe="直播标签")
    # _live_name_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__title')]",
    #                         describe="直播名称")
    # _live_interactive_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__interactive')]",
    #                         describe="互动标签")
    # _live_subject_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subTitle')]",
    #                         describe="科目")
    # _live_module_div_location = Element(xpath="//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subTitle')]",
    #                         describe="直播关联的模块")
    # _live_lecture_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveLecture-index__lectureStatus')]",
    #                     describe="讲义")
    # _live_no_watched_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveStatus-index__notWatched')]",
    #                         describe="是否未看")
    # _live_status_div_location = Element(xpath="*//div[starts-with(@class, 'src-components-MyCenter-LiveButton-index__actionBlock')]",
    #                         describe="直播状态")
    # _live_button_location = Element(xpath="*//div[starts-with(@class, 'hx-btn src-components-HxButton')]",
    #                         describe="直播按钮")

    # 直播的开始时间
    _live_start_time_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__time--')]"
    # 直播老师名字
    _live_teacher_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__teachers')]"
    # 直播标签
    _live_tag_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__tag')]"
    # 直播名称
    _live_name_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__title')]"
    # 互动标签
    _live_interactive_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__interactive')]"
    # 科目
    _live_subject_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subTitle')]"
    # 直播关联的模块
    _live_module_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveScheduleItem-index__subject')]"
    # 讲义
    _live_lecture_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveLecture-index__lectureStatus')]"
    # 是否未看
    _live_no_watched_span_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveStatus-index__notWatched')]"
    # 直播状态
    _live_status_div_location = "//div[starts-with(@class, 'src-components-MyCenter-LiveButton-index__actionBlock')]"
    # 直播按钮
    _live_button_location = "//div[starts-with(@class, 'hx-btn src-components-HxButton')]"

    def __init__(self, driver: webdriver, live_id, component_location):
        """
        :param driver:
        :param live_id:直播ID
        :param component_location: 组件定位信息,为一个dict，如{"xpath": "*//div/a"]
        """
        self.live_id = live_id
        self.component_location = component_location
        super().__init__(driver)
        self.get_class_attr()

    def get_class_attr(self):
        """为类动态添加属性"""
        MainStationLiveListComponent._live_start_time_div = Element(xpath=self.component_location + self._live_start_time_div_location,
                                                                    describe="直播的开始时间")
        MainStationLiveListComponent._live_teacher_div = Element(xpath=self.component_location + self._live_teacher_div_location,
                                                                 describe="直播老师名称")
        MainStationLiveListComponent._live_tag_div = Element(xpath=self.component_location + self._live_tag_div_location,
                                                                 describe="直播标签")
        MainStationLiveListComponent._live_name_div = Element(xpath=self.component_location + self._live_name_div_location,
                                                                 describe="直播名称")
        MainStationLiveListComponent._live_interactive_div = Element(xpath=self.component_location + self._live_interactive_div_location,
                                                                 describe="互动标签")
        MainStationLiveListComponent._live_subject_div = Element(xpath=self.component_location + self._live_subject_div_location,
                                                                 describe="科目")
        MainStationLiveListComponent._live_module_div = Element(xpath=self.component_location + self._live_module_div_location,
                                                                 describe="直播关联的模块")
        MainStationLiveListComponent._live_lecture_div = Element(xpath=self.component_location + self._live_lecture_div_location,
                                                                 describe="讲义")
        MainStationLiveListComponent._live_no_watched_span = Element(xpath=self.component_location + self._live_no_watched_span_location,
                                                                 describe="是否未看")
        MainStationLiveListComponent._live_status_div = Element(xpath=self.component_location + self._live_status_div_location,
                                                                 describe="直播状态")
        MainStationLiveListComponent._live_button = Element(xpath=self.component_location + self._live_button_location,
                                                                 describe="直播按钮")
        # component = self.driver.find_element(*self.component_location)
        # component.get_attribute()

    def get_live_detail(self):
        detail_dict = {}
        detail_dict["live_start_time"] = MainStationLiveListComponent._live_start_time_div.get_element(self.driver).text
        detail_dict["live_teacher"] = MainStationLiveListComponent._live_teacher_div.get_attribute("title")
        detail_dict["live_tag"] = MainStationLiveListComponent._live_tag_div.get_element(self.driver).text
        detail_dict["live_name"] = MainStationLiveListComponent._live_name_div.get_element(self.driver).text
        detail_dict["live_interactive"] = MainStationLiveListComponent._live_interactive_div.get_element(self.driver).text
        detail_dict["live_subject"] = MainStationLiveListComponent._live_subject_div.get_attribute("title")
        detail_dict["live_module"] = MainStationLiveListComponent._live_module_div.get_attribute("title")
        detail_dict["live_lecture"] = MainStationLiveListComponent._live_lecture_div.get_element(self.driver).text
        detail_dict["live_no_watched"] = MainStationLiveListComponent._live_no_watched_span.get_element(self.driver).text
        detail_dict["live_status"] = MainStationLiveListComponent._live_status_div.get_element(self.driver).text
        detail_dict["live_button"] = MainStationLiveListComponent._live_button.get_element(self.driver).text

        return  detail_dict

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
        from pages.main_station.main_station_live_module_page import MainStationLiveModulePage

        return MainStationLiveModulePage(self.driver)

    # @allure.step("判断直播是否未看")
    # def judge_live_status(self):
    #     pass

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

class TextTes:
    aa = "A"

    def get(self):
        TextTes.bb = "B"

# if __name__ == "__main__":
#     T = TextTes()
#     T.get()
#     print(T.bb)

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
