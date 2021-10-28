# # -*- coding: utf-8 -*-
# import json
# import time
# import hashlib
# import collections
# from datetime import datetime
# import allure
#
#
# @allure.epic("章节精炼")
# @allure.feature("章节精炼0")
# class TestExamWeb:
#
#     @allure.story("章节精炼初始化接口")
#     @allure.severity(allure.severity_level.BLOCKER)
#     def test_exam_common_exercise(self, go_to_api_login):
#
#         request_session = go_to_api_login["se"]
#         study_url = "http://w1.highso.com.cn/exam/common/exercise.do?recordModule=101&categoryId=9&subjectId=1&businessId=350317"
#         r2 = request_session.get(url=study_url, headers={"Content-Type": "application/json"})
#
#         print(r2.text)
#
#
#
#     @allure.story("章节精炼初始化接口")
#     @allure.severity(allure.severity_level.BLOCKER)
#     def test_exam_common_exercise_1(self, go_to_api_login):
#         request_session = go_to_api_login["se"]
#         csrf_token = go_to_api_login["csrf_token"]
#         study_url = "http://w1.highso.com.cn/study/pc/live/timeLimitLive?categoryId=9&csrf_token=" + csrf_token
#         r2 = request_session.get(url=study_url, headers={"Content-Type": "application/json"})
#
#         print(r2.text)
#
#
#
#
#
#
