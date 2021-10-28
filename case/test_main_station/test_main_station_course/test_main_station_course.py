# -*- coding: utf-8 -*-
import allure
import pytest


@allure.epic("课程模块")
@allure.feature("直播日历")
class TestMainStaionCourseliveDate:

    @allure.story("直播日历")
    @allure.title("直播日历进入直播模块详情页")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_go_to_live_module(self, go_to_course):
        go_to_course.go_live_module_live_list()
        assert "/v5/my/course/live-detail" in go_to_course.driver.current_url

    @allure.story("进入更多课程")
    @allure.title("直播日历日历部分进入更多课程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_go_to_more_course_date(self, go_to_course):
        go_to_course.go_date_more_course_page()
        assert "/v5/my/course/all-course" in go_to_course.driver.current_url

    @allure.story("进入更多课程")
    @allure.title("直播日历列表部分进入更多课程")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_go_to_more_course_list(self, go_to_course):
        go_to_course.go_list_more_course_page()
        assert "/v5/my/course/all-course" in go_to_course.driver.current_url

    @allure.story("进入直播回放页面")
    @allure.title("直播日历进入直播回放页面")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_go_to_playback(self, go_to_course):
        go_to_course.go_list_live_playback()
        assert "/course/newlive/newPlaybackPage.do" in go_to_course.driver.current_url

    @pytest.mark.skip("创建直播未实现，暂时不执行")
    @allure.story("预约直播")
    @allure.title("直播日历预约直播")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_subscribe_live(self, go_to_course):
        result = go_to_course.go_list_subscribe_live()
        assert "预约成功" in result

    @allure.story("下载讲义")
    @allure.title("直播日历下载讲义")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_download_lecture_pdf(self, go_to_course):
        go_to_course.download_lecture()
        assert go_to_course.judge_is_download_lecture()


@allure.epic("课程模块")
@allure.feature("其它功能")
class TestMainStaionCourseOrther:

    @allure.story("继续上次学习")
    @allure.title("继续上次学习")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_continue_learn(self, go_to_course):
        result = go_to_course.go_last_learn()
        assert "/course/newlive/newPlaybackPage.do" in result

    @pytest.mark.skip("未实现，暂时不执行")
    @allure.story("签到")
    @allure.title("签到")
    @allure.severity(allure.severity_level.MINOR)
    def test_sign(self, go_to_course):
        result = go_to_course.go_sign()
        assert result


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("课程模块")
@allure.feature("商品切换")
class TestMainStaionCourseChooseGoods:
    pass


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("课程模块")
@allure.feature("学习建议")
class TestMainStationCourseLearnAdvice:
    pass


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("课程模块")
@allure.feature("全部课程")
class TestMainStaionCourseAllCourse:
    pass


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("课程模块")
@allure.feature("学习记录")
class TestMainStaionCourseWatchLog:
    pass