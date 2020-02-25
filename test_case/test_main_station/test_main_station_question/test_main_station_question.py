# -*- coding: utf-8 -*-
import allure
import pytest

from pages.main_station.main_station_home_page import MainStationHomePage
from pages.main_station.main_station_question_page import MainStationQuestionPage


@allure.feature("问答中心-提问")
class TestQuestion:

    @allure.story("对课程提问")
    @allure.title("对课程提问-最近看的课程，如果没有则false")
    @allure.severity(allure.severity_level.BLOCKER)
    # @pytest.mark.parametrize("register_data", get_register_data())
    def test_question_course(self):
        pass

    @allure.story("对教材提问")
    @allure.title("对教材提问-排在最上面的考点")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_textbook(self):
        pass

    @allure.story("对试题提问")
    @allure.title("对试题提问-最近做的一道试题提问，如果没有则为false")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_question_(self):
        pass
