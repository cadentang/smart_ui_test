# -*- coding: utf-8 -*-
import allure
import pytest
from pages.main_station.main_station_home_page import MainStationHomePage
from pages.main_station.main_station_question_page import MainStationQuestionPage


@allure.feature("问答中心")
class TestQuestion:

    @allure.story("对课程提问")
    @allure.title("对课程提问-最近看课的第一个记录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", "老师，这个视频里面提到的建筑经济如何计算？")
    def test_question_course(self, get_driver, go_to_question_page, content):
        # MainStationHomePage(get_driver).go_to_login_page().to_login("haixue", "19983271082", "123456")
        # question_page = MainStationHomePage(get_driver).go_question()
        go_to_question_page.question_for_course(content)
        assert go_to_question_page.check_question(content)

    @allure.story("对教材提问")
    @allure.title("对教材提问-排在最上面的考点")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", "老师，这个教材里面提到的建筑经济如何计算？")
    def test_question_textbook(self, get_driver, content):
        MainStationHomePage(get_driver).go_to_login_page().to_login("haixue", "19983271082", "123456")
        question_page = MainStationHomePage(get_driver).go_question()
        question_page.question_for_textbook(content)
        assert question_page.check_question(content)

    @allure.story("对试题提问")
    @allure.title("对试题提问-最近做的一道试题提问")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", "老师，这个题目里面提到的建筑经济如何计算？")
    def test_question_exam(self, get_driver, content):
        MainStationHomePage(get_driver).go_to_login_page().to_login("haixue", "19983271082", "123456")
        question_page = MainStationHomePage(get_driver).go_question()
        question_page.question_for_examrecord(content)
        assert question_page.check_question(content)

    @allure.story("点赞及收藏问题")
    @allure.title("对试题进行点赞及收藏")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_diazan_shoucang(self):
        pass

    @allure.story("对问题回复进行评分")
    @allure.title("对问题回复进行评分")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_pingfen(self):
        pass

    @allure.story("对老师回复的问题进行追问")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_zhuiwen(self):
        pass

    @allure.story("对自己提的问题做补充问题")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_buchong(self):
        pass

    @allure.story("搜索问题")
    @allure.severity(allure.severity_level.MINOR)
    def test_question_sswt(self):
        pass

    @allure.story("搜索考点")
    @allure.severity(allure.severity_level.MINOR)
    def test_question_sskd(self):
        pass