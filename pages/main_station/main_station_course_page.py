# -*- coding: utf-8 -*-
import os
import shutil
from time import sleep

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By

from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage
from pages.main_station.main_station_live_video_module_page  import MainStationLiveVideoModulePage
from pages.main_station.main_station_video_page import MainStationVideoPage
from common.selenium_pages import PageSwitchWindowOrFrame, PageMouse, PageScroll
from component.main_station.main_station_live_component import MainStationLiveListComponent
from utils.base_path import DOWNLOAD_LECTURE_PATH
from utils.get_log import logger
from common.selenium_driver import SeleniumDriver


class MainStationCoursePage(MainStationBasePage):
    """课程页面"""
    _date_more_course_div = Element(xpath="//div[starts-with(@class, 'src-pages-center-Calendar-index__moreClass')]", describe="更多课程")
    _list_more_course_div = Element(xpath="//div[contains(text(), '查看更多课程')]", describe="列表页查看更多课程")
    _sign_button = Element(xpath="//div/button[contains(text(),'立即签到')]", describe="签到按钮")
    _continue_watch_button = Element(xpath="//button[contains(text(), '继续观看')]",  describe="继续观看按钮")
    _watchlog_button = Element(xpath="//div[contains(text(), '看课记录')]",  describe="看课记录")
    _week_report_div = Element(css=".learning-bottom-text", describe="学习周报")

    _first_video_module = Element(xpath="//div/section/main/div/main/div[6]/div[3]/div/div[2]/div[2]/div[1]/div[3]/button",
                                  describe="全部课程第一个录播模块按钮")
    _first_live_module = Element(xpath="//div/section/main/div/main/div[6]/div[3]/div/div[3]/div[2]/div[1]/div[3]/button",
                                 describe="全部课程第一个直播模块按钮")

    # 直播日历列表控件
    _live_date_div = (By.XPATH, "//div[starts-with(@class, 'src-pages-center-CourseTimeline-index__wrap')]")
    # 单条直播组件
    _live_list_compent_div = (By.XPATH, "//div[starts-with(@class, 'src-pages-center-CourseTimeline-index__itemWrap')]")
    # 签到成功
    _sign_success_span = (By.XPATH, "//div/span[contains(text(), '签到成功')]")

    @allure.step("日历日期部分进入更多课程")
    def go_date_more_course_page(self):
        self._date_more_course_div.click()
        self.switch_target_page()
        from pages.main_station.main_station_more_course_page import MainStationMoreCoursePage
        return MainStationMoreCoursePage(self.driver)

    @allure.step("日历列表部分进入更多课程")
    def go_list_more_course_page(self):
        self._list_more_course_div.click()
        self.switch_target_page()
        from pages.main_station.main_station_more_course_page import MainStationMoreCoursePage
        return MainStationMoreCoursePage(self.driver)

    @allure.step("日历列表进入直播回放页面")
    def go_list_live_playback(self):
        """选择最近一个直播回放状态的直播,直播"""
        compent_lists = self.driver.find_elements(*self._live_list_compent_div)
        for i in range(len(compent_lists)-1, -1,-1):
            if "直播回放" in compent_lists[i].text:
                sleep(2)
                element = compent_lists[i].find_elements(*MainStationLiveListComponent._live_playback_button)
                self.driver.execute_script("arguments[0].click();", element[-1])
                return compent_lists[i].text

    @allure.step("日历列表预约直播")
    def go_list_subscribe_live(self):
        """选择最近一个可以预约的直播预约"""
        compent_lists = self.driver.find_elements(*self._live_list_compent_div)
        for i in range(len(compent_lists)-1, -1,-1):
            if "直播预约" in compent_lists[i].text:
                sleep(2)
                element = compent_lists[i].find_elements(*MainStationLiveListComponent._live_subscribe_button)
                self.driver.execute_script("arguments[0].click();", element[-1])
                return compent_lists[i].text

    @allure.step("日历列表处下载讲义")
    def download_lecture(self):
        """选择直播列表最近的一场有讲义的直播下载"""
        if os.path.exists(DOWNLOAD_LECTURE_PATH):
            shutil.rmtree(DOWNLOAD_LECTURE_PATH)
            os.mkdir(DOWNLOAD_LECTURE_PATH)
        else:
            os.mkdir(DOWNLOAD_LECTURE_PATH)
        compent_lists = self.driver.find_elements(*self._live_list_compent_div)
        for i in range(len(compent_lists)-1, -1,-1):
            if "讲义" in compent_lists[i].text:
                sleep(2)
                element = compent_lists[i].find_elements(*MainStationLiveListComponent._live_have_lecture_div)
                self.driver.execute_script("arguments[0].click();", element[-1])
                return compent_lists[i].text

    @allure.step("日历列表进入模块详情页")
    def go_live_module_live_list(self):
        compent_lists = self.driver.find_elements(*self._live_list_compent_div)
        for i in range(len(compent_lists)-1, -1,-1):
            pass

    @allure.step("签到")
    def go_sign(self):
        self._sign_button.click()
        try:
            sleep(2)
            self.driver.find_element(*self._sign_success_span)
            return True
        except:
            return False

    @allure.step("进入看课记录页面")
    def go_learn_log(self):
        self._watchlog_button.click()
        self.switch_target_page()
        from pages.main_station.main_station_watch_log_page import MainStationWatchLogPage
        return MainStationWatchLogPage(self.driver)

    @allure.step("进入学习周报页面")
    def go_week_report(self):
        self._week_report_div.click()
        self.switch_target_page()
        from pages.main_station.main_station_week_report_page import MainStationWeekReportPage
        return MainStationWeekReportPage(self.driver)

    @allure.step("进入上次学习页面")
    def go_last_learn(self):
        self._continue_watch_button.click()
        sleep(2)
        self.switch_target_page()
        return self.driver.current_url

    @allure.step("选择一个或者多个商品显示")
    def choose_goods(self, goods_name_list):
        pass

    @allure.step("选择某个科目下的某个阶段的某个模块学习")
    def choose_learn_advice(self):
        pass

    @allure.step("通过全部课程进入直播模块学习")
    def go_to_live_module_all_course(self):
        self._first_live_module.click()
        sleep(2)
        from pages.main_station.main_station_live_page import MainStationLivePage
        return MainStationLivePage(self.driver)

    @allure.step("通过全部课程进入录播模块学习")
    def go_to_video_module_all_course(self):
        self._first_video_module.click()
        sleep(2)
        from pages.main_station.main_station_video_page import MainStationVideoPage
        return MainStationVideoPage(self.driver)

    def scroll_live_list(self):
        """直播日历列表滚动"""
        sleep(2)
        PageMouse(self.driver).move_to_element(self._live_date_div)
        PageScroll(self.driver).js_scroll_top()

    def get_all_subject(self):
        """获取选择的商品下有哪些科目"""
        pass

    def get_exam_season(self):
        """获取该科目下有哪些考季"""
        pass

    def switch_target_page(self):
        """点击进入目标页面， 关闭上一个页面"""
        window = PageSwitchWindowOrFrame(self.driver)
        self.driver.close()
        sleep(2)
        window.switch_handle(0)

    def judge_is_download_lecture(self):
        """判断是否下载成功"""
        lecture_file = os.listdir(DOWNLOAD_LECTURE_PATH)
        logger.info(f"下载讲义：{lecture_file}")
        if len(lecture_file) >= 1:
            # shutil.rmtree(DOWNLOAD_LECTURE_PATH)
            # os.mkdir(DOWNLOAD_LECTURE_PATH)
            return True
        else:
            return False

    def set_live(self):
        categroy = (By.ID, "categoryId")
        subject = (By.ID, "subjectId")
        source = (By.ID, "sourceId")
        module = (By.ID, "module")
        module_id = (By.ID, "keyword")
        module_query = (By.XPATH, "//button/span[contains(text(), '查询')]")
        module_checkbox = (By.CSS_SELECTOR, "td>label>span>input[type='checkbox']")
        module_confirm = (By.XPATH, "//button/span[contains(text(), '确定')]")
        live = (By.ID, "liveName")
        type = (By.ID, "type")
        teacher = (By.CSS_SELECTOR, "#teacher")
        teacher_name = (By.CSS_SELECTOR, "#teacherName")
        teacher_query = (By.XPATH, "/html/body/div[6]/div/div[2]/div/div[2]/div[2]/div[1]/form/div[2]/div/div/span/button/span")
        # teacher_checkbox = (By.CSS_SELECTOR, "td>label>span>input[type='radio']")
        teacher_checkbox = (By.CSS_SELECTOR, "tr[data-row-key='17229']")
        teacher_confirm = (By.XPATH, "/html/body/div[6]/div/div[2]/div/div[2]/div[3]/div/button[2]")
        start_time = (By.CSS_SELECTOR, "input[placeholder='开始时间']")
        end_time = (By.CSS_SELECTOR, "input[placeholder='结束时间']")
        time_confirm = (By.XPATH, "//ul/li/button/span[contains(text(), '确定')]")
        # time_confirm = (By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div[2]/ul/li/button")

        driver = SeleniumDriver().driver()
        # if "w0" in self.driver.current_url:
        #     driver.get("https://antd-study-admin.test0.highso.com.cn/")
        # elif "w1" in self.driver.current_url:
        #     driver.get("https://antd-study-admin.reg.highso.com.cn/")
        # elif "w2" in self.driver.current_url:
        #     driver.get("https://antd-study-admin.stage.highso.com.cn/")
        # else:
        #     logger.info("未知的测试环境")
        driver.get("https://antd-study-admin.stage.highso.com.cn/")

        driver.find_element(*(By.ID, "username")).send_keys("tangkun4379")
        driver.find_element(*(By.ID, "password")).send_keys("123456")
        driver.find_element(*(By.ID, "login-submit")).click()
        sleep(2)
        driver.refresh()
        driver.find_element(*(By.CSS_SELECTOR, "span.anticon.anticon-play-square")).click()
        driver.find_element(*(By.CSS_SELECTOR, "a[href='/live/manage']")).click()
        driver.find_element(*(By.CSS_SELECTOR, "a[href='/live/create']")).click()
        driver.find_element(*(By.XPATH, "//div[contains(text(), '创建学术直播')]")).click()

        sleep(2)
        # js = "$('categoryId').removeAttr('readonly')"
        js_category = 'document.getElementById("categoryId").removeAttribute("readonly")'
        js_subject = 'document.getElementById("subjectId").removeAttribute("readonly")'
        js_source = 'document.getElementById("sourceId").removeAttribute("readonly")'
        js_type = 'document.getElementById("type").removeAttribute("readonly")'

        driver.execute_script(js_category)
        driver.execute_script(js_subject)
        driver.execute_script(js_source)
        driver.execute_script(js_type)
        driver.find_element(*categroy).send_keys("一级建造师")
        driver.find_element(*(By.XPATH, "//span[contains(text(), '一级建造师')]")).click()
        driver.find_element(*subject).send_keys("建设工程经济")
        driver.find_element(*(By.XPATH, "//span[contains(text(), '建设工程经济')]")).click()

        driver.find_element(*source).click()
        # driver.find_element(*source).send_keys("嗨学")
        driver.find_element(*(By.XPATH, "//div[contains(text(), '嗨学')]")).click()

        driver.find_element(*module).click()
        driver.find_element(*module_id).send_keys("17229")
        sleep(2)
        driver.execute_script("arguments[0].click();", driver.find_element(*module_query))
        sleep(2)
        driver.execute_script("arguments[0].click();", driver.find_element(*module_checkbox))
        driver.execute_script("arguments[0].click();", driver.find_element(*module_confirm))

        driver.find_element(*live).send_keys("直播测试")
        sleep(2)
        from common.selenium_pages import PageScroll
        PageScroll(driver).js_scroll_end()
        driver.find_element(*teacher).click()
        sleep(2)
        driver.find_element(*teacher_name).send_keys("唐锟")
        aa = driver.find_element(*teacher_query)
        bb = driver.find_element(*teacher_checkbox)
        cc = driver.find_element(*teacher_confirm)
        driver.execute_script("arguments[0].click();", aa)
        sleep(5)
        driver.execute_script("arguments[0].click();", bb)
        sleep(2)
        driver.execute_script("arguments[0].click();", cc)
        sleep(2)

        driver.find_element(*start_time).send_keys("2020-03-22 16:00")
        sleep(2)
        driver.execute_script("arguments[0].click();",driver.find_element(*time_confirm))

        driver.find_element(*end_time).send_keys("2020-03-22 16:30")
        sleep(2)
        driver.execute_script("arguments[0].click();",driver.find_element(*time_confirm))
        # driver.quit()
        sleep(10)


if __name__ == "__main__":
    # from pages.main_station.main_station_home_page import MainStationHomePage
    # aa = MainStationCoursePage("aaa")
    # aa.judge_is_download_lecture()


    # chromeOptions = webdriver.ChromeOptions()
    # prefs = {"download.default_directory": "D:\haixue_work\script\haixue_git\haixue-test-ui\\resource\\lecture"}
    # chromeOptions.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(executable_path="D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe",
    #                           chrome_options=chromeOptions)
    # driver.maximize_window()
    # driver.get("http://w2.highso.com.cn/v5")
    # aa = MainStationHomePage(driver)
    MainStationCoursePage("111").set_live()
    # bb = aa.go_to_login_page().to_login("haixue", "19983271081", "123456")


    # # print(driver.current_url)
    # # driver.find_element_by_css_selector()
    # sleep(3)
    # from pages.main_station.main_station_home_page import MainStationHomePage
    #
    # aa = MainStationHomePage(driver)
    # bb = aa.go_to_login_page().to_login("haixue", "19983271081", "123456")
    # # aa.get_bottom_list_navigations()
    # sleep(3)
    # bb.download_lecture()
    # # element = bb.driver.find_element(*(By.XPATH, "//div/section/main/div/main/div[1]/div[1]/div[3]/div/div/div[15]/div[2]/div/div[2]/button"))
    # # driver.execute_script("arguments[0].click();", element)
    #
    # # aa.switch_category("二级建造师")
    # # from common.selenium_pages import PageScroll
    # # PageScroll(aa.driver).js_scroll_end()
    # # print(aa.driver.find_element(By.XPATH, "//div/section/main/div/main/div[6]/div[3]/div/div[2]/div[2]/div[1]/div[3]/button").text)
    # sleep(1)
    # # bb.go_date_more_course_page()
    # # aa.logout()

