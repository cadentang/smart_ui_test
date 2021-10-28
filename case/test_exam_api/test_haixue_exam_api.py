# -*- coding: utf-8 -*-
import json
import time
import hashlib
import collections
from datetime import datetime
import allure


@allure.epic("题库首页")
@allure.feature("主站题库首页")
class TestHaixueExamApi:

    @allure.story("获取首页类别和科目列表")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_subject(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/subject/findByCategoryId?categoryId=9&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页章节精炼考点树")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_outline(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/outline/outline?categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页学员的做题情况")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_overall(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/statistics/overAll?categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页历年真题和模拟测试显示情况")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_paper(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/paper/findBySubjectId?categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页连对挑战情况")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_homedate(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/challenge/homeDate?categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页每日一题情况")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_homedate(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/statistics/dailyRank?categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200

    @allure.story("获取题库首页章节精炼下每一章节做题情况")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_haixue_exam_api_get_outline_day(self, go_to_api_login):
        request_session = go_to_api_login["se"]
        csrf_token = go_to_api_login["csrf_token"]
        url = go_to_api_login["base_url"] + "/exam-up/pc/statistics/doneQuestionStats?outlineId=302193&categoryId=9&subjectId=1&csrf_token=" + csrf_token
        result = request_session.get(url=url, headers={"Content-Type": "application/json"})
        result_dict = json.loads(result.text)
        # print(result_dict)
        assert result_dict["code"] == 200




