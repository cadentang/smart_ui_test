# -*- coding: utf-8 -*-
from time import sleep

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as ex

from common.selenium_pages import PageSwitchWindowOrFrame
from common.web_component import BaseWebComponents
from common.element import Element
from utils.get_log import logger


class MainStationQuestionComponent(BaseWebComponents):
    """
    问题组件，适用于问答中心-我的问题列表、问答精华列表、提问问题关联列表，问题详情页面
    题库-题目解析关联的问答列表
    """
    _dianzan_svg = (By.CSS_SELECTOR, 'div>div>div>span:nth-child(2)')  # 点赞、取消点赞
    _collect_svg = (By.CSS_SELECTOR, 'div>div>div>span:nth-child(1)')  # 收藏、取消收藏
    _question_content_span = (By.CSS_SELECTOR, 'h3>div>span:nth-child(2)')  # 列表页收起状态学员提问的内容
    _question_appent_content_span = (By.CSS_SELECTOR, 'div>h4>span:nth-child(2)')  # 列表页和详情页追问问题内容，详情页可能会有多个
    _question_button_span = (By.CSS_SELECTOR, 'h3>div>span:nth-child(3)')  # 显示详情和收起按钮
    _question_answer_span = (By.CSS_SELECTOR, 'h3>div>span:nth-child(2)')  # 老师回复的内容
    _question_content_li = (By.CSS_SELECTOR, 'div>ul>li.ant-rate-star.ant-rate-star-zero')  # 评分的星星
    _question_rate_content_span = (By.CSS_SELECTOR, 'h3>div>span:nth-child(2)')  # 评分标签
    _question_content_input = (By.CSS_SELECTOR, 'h3>div>span:nth-child(2)')  # 评分内容输入框
    _question_content_button = (By.CSS_SELECTOR, 'div>button')  # 评分提交按钮
    _main_question = (By.XPATH, "//p[text()='学员您好！我们的老师正在为您解答中，请耐心等候！']")
    _append_question = (By.XPATH, "//div[text()='学员您好！我们的老师正在为您解答中，请耐心等候！']")
    _new_mark_span = (By.XPATH, "//div/span[text()='NEW']")  # NEW标签

    _main_score_span = (By.XPATH, '//li/div/div/div/div/span[contains(text(), "已评分：")]')  # 列表主问题已评分标识
    _main_no_score_span = (By.XPATH, '//li/div/div/div/div/span[contains(text(), "请对此次回答评分：")]')  # 列表主问题未评分标识
    _append_score_span = (By.XPATH, '//li/div/div/div/div/div/div/div/span[contains(text(), "已评分：")]')  # 列表追问问题已评分标识
    _append_no_score_span = (By.XPATH, '//li/div/div/div/div/div/div/div/span[contains(text(), "请对此次回答评分：")]')  # 列表追问问题未评分标识
    _append_question_mark_span = (By.XPATH, "//h4/span[text()='追问：']")  #  判断问题是否有追问问题标志

    def __init__(self, driver: webdriver, component_location):
        """
        :param driver:
        :param component_location: 组件定位信息,为一个dict，如{"xpath": "*//div/a"]
        """
        self.component_location = component_location
        super().__init__(driver)
        self.component_element = self.driver.find_element(*self.component_location)

    @allure.step("点赞/取消点赞")
    def dianzan(self):
        self.component_element.find_element(*self._dianzan_svg).click()
        return  self.component_element.find_element(*self._dianzan_svg).text

    @allure.step("收藏/取消收藏")
    def collect(self):
        self.component_element.find_element(*self._collect_svg).click()
        return self.component_element.find_element(*self._collect_svg).text

    def judg_is_dianzan(self):
        if "已点赞" in self.component_element.find_element(*self._dianzan_svg).text:
            return True
        else:
            return False

    def judg_is_shoucang(self):
        if "已收藏" in self.component_element.find_element(*self._collect_svg).text:
            return True
        else:
            return False

    @allure.step("对主问题评分, 根据分数及评价内容评分")
    def score_main_question(self, score, content):
        """
        :param score: 分数
        :param content: 评分的内容
        :return:
        """
        score_list = [1, 2, 3, 4, 5]
        if score in score_list:
            sc = (By.CSS_SELECTOR, f"li>div[aria-posinset={str(score)}][aria-checked='false']")
            self.component_element.find_element(*self._question_content_li).find_element(*sc).click()
            self.component_element.find_element(*self._question_content_input).send_keys(content)
            self.component_element.find_element(*self._question_content_button).click()
        else:
            logger.info(f"传入的分数{score}不能评分")

    @allure.step("查看问答详情")
    def question_detail(self):
        """从列表页进入问题详情页, 只适用于列表页组件, 返回问题详情页问题组件"""
        window = PageSwitchWindowOrFrame(self.driver)
        # self.driver.refresh()
        sleep(2)
        try:
            aa = self.component_element.find_element(*self._question_content_span)
            aa.click()
        except ex.StaleElementReferenceException:
            self.component_element.find_element(*self._question_content_span).click()
        self.driver.close()
        window.switch_handle(0)

    def judge_is_answer(self):
        """判断问题老师是否回答,
        0:主问题老师未回复， 1:追问问题老师未回复， 2:追问问题老师已回复， 3：主问题老师已回复无追问问题"""
        wait_answer_text = "学员您好！我们的老师正在为您解答中，请耐心等候！"
        # logger.info(f"self.component_element.find_element(*self._main_question): {self.component_element.find_element(*self._main_question).text}")
        try:
            print(self.component_element.find_element(*self._main_no_score_span).text)
            if self.judge_is_append() == True:

                try:
                    self.component_element.find_element(*self._append_question)
                    return 1
                except ex.NoSuchElementException:
                    return 2
            else:
                return 3
        except ex.NoSuchElementException:
            return 0

    def judge_is_append(self):
        """判断列表是否存在追问问题"""
        append_mark = "追问："
        try:
            self.component_element.find_element(*self._append_question_mark_span)
            return True
        except ex.NoSuchElementException:
            return False
        # if self.component_element.find_element(*self._append_question_mark_span).text == append_mark:
        #     return True
        # else:
        #     return False

    def judge_is_score(self, is_append=False):
        """判断问题是否评分"""
        if is_append == False:
            if self.judge_is_answer() in [1,2,3]:
                if self.component_element.find_element(*self._main_score).text == "已评分：":
                    return True
                else:
                    return False
            elif self.judge_is_answer() == 0:
                logger.info("主问题老师未回复不能评分")
                return False
            else:
                logger.info("出现异常")
        else:
            if self.judge_is_answer() == 2:
                if self.component_element.find_element(*self._append_score).text == "已评分：":
                    return True
                else:
                    return False
            else:
                return False

    def judg_new_mark(self):
        """判断是否有new标签"""
        if self.component_element.find_element(*self._new_mark_span).text == "NEW":
            return True
        else:
            return False

    def get_main_content(self):
        """获取该问题的主问题文本内容"""
        text = self.component_element.find_element(*self._question_content_span).text
        return text

    def get_append_content(self, is_detail_page=False):
        """获取列表页和详情页的追问问题文本内容， 列表页获取最新的追问，详情页获取所有的追问,详情页返回的是一个list"""
        if is_detail_page == False:
            text = self.component_element.find_element(*self._question_appent_content_span).text
        else:
            text = self.component_element.find_elements(*self._question_appent_content_span).text
        return text

    def get_question_id(self):
        """获取question_id"""
        url = self.driver.current_url
        try:
            if "detail" in url:
                question_id = int(url.split("/")[-1])
                return question_id
            else:
                self.question_detail()
                question_id = int(url.split("/")[-1])
                return question_id
        except:
            logger.info("未进入问题详情页，不能获取到ID")


#
# if __name__ == "__main__":
#     driver = webdriver.Chrome("D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe")
#     driver.maximize_window()
#
#     driver.get("http://w2.highso.com.cn/v5")
#     # driver.find_element_by_css_selector()
#     sleep(3)
#     from pages.main_station.main_station_home_page import MainStationHomePage
#
#     aa = MainStationHomePage(driver)
#     sleep(2)
#     bb = aa.go_to_login_page().to_login("haixue", "19983271081", "123456")
#     # aa.get_bottom_list_navigations()
#     # aa.logout()
#     # bb.go_message()
#     sleep(1)
#     bb.go_question()
#     sleep(1)
#     # question_list_component_lis = (By.CSS_SELECTOR, "ul.ant-list-items>li:nth-child(1)")  # 定位问题列表组件,有可能有多个
#     # eles = driver.find_element(*question_list_component_lis)
#     eles = MainStationQuestionComponent(driver, (By.CSS_SELECTOR, f"ul.ant-list-items>li:nth-child(1)"))
#     sleep(1)
#     # print(eles.dianzan())
#     d = eles.judge_is_answer()
#     print(d)
#     # print(eles)
#     # print(len(eles))
#     # for i in range(len(eles)):
#     #     print(eles[i].find_element(*(By.CSS_SELECTOR, 'h3>div>span:nth-child(2)')).text)
#         # compent = MainStationQuestionComponent(driver, (By.CSS_SELECTOR, f"ul.ant-list-items>li:nth-child({i + 1})"))
#         # print(compent.get_main_content())
#
#     # lo = (By.XPATH,'//*[@id="root"]/div/section/main/div/main/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/div/div/ul/li[2]')
#     # com = MainStationQuestionComponent(bb.driver, lo)
#     # com.question_detail()
