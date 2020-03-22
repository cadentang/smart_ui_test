# -*- coding: utf-8 -*-
import allure
import pytest


@allure.epic("问答中心")
@allure.feature("我要提问")
class TestAskQuestion:

    @allure.story("对课程提问")
    @allure.title("对课程提问-最近看课的第一个记录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["老师，这个视频里面提到的建筑经济如何计算？"])
    def test_ask_question_course(self, go_to_question_page, content):
        text = go_to_question_page.question_for_course(content)
        assert go_to_question_page.check_question(text)

    @allure.story("对教材提问")
    @allure.title("对教材提问-排在最上面的考点")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["老师，这个教材里面提到的建筑经济如何计算？"])
    def test_ask_question_textbook(self, go_to_question_page, content):
        text = go_to_question_page.question_for_textbook(content)
        assert go_to_question_page.check_question(text)

    @allure.story("对试题提问")
    @allure.title("对试题提问-最近做的一道试题提问")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["老师，这个题目里面提到的建筑经济如何计算？"])
    def test_ask_question_exam(self, go_to_question_page, content):
        text = go_to_question_page.question_for_examrecord(content)
        assert go_to_question_page.check_question(text)

    @allure.story("追问")
    @allure.title("对老师回复的问题进行追问")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["老师，你的回答我不太明白，请再解释下"])
    def test_ask_question_append_ask(self, go_to_question_page, content):
        text = go_to_question_page.question_for_append(content)
        assert go_to_question_page.check_question(text, is_append=True)

    @allure.story("补充问题")
    @allure.title("对自己提的问题做补充问题")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["老师，这个题目里面提到的建筑经济如何计算？"])
    def test_ask_question_supplement(self, go_to_question_page, content):
        text = go_to_question_page.question_for_supplement(content)
        assert go_to_question_page.check_question(content)

    @allure.story("老师回复问题")
    @allure.title("对自己提的问题做补充问题")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", ["同学，你好！这个题目很简单？"])
    def test_ask_question_teacher_answer(self, go_to_question_page, content):
        text = go_to_question_page.question_for_course(content)
        result = go_to_question_page.question_teacher_replay()
        assert result

    @pytest.mark.skip("未实现，暂时不执行")
    @allure.story("提问权限")
    @allure.title("没有权限提问")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ask_question_no_permission(self, go_to_question_page, content):
        pass

    @pytest.mark.skip("未实现，暂时不执行")
    @allure.story("提问权限")
    @allure.title("超过提问次数限制")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ask_question_over_perssion(self):
        """使用账号stage:19983271081,123456.二建科目验证，对教材提问"""
        pass

    @pytest.mark.skip("未实现，暂时不执行")
    @allure.story("精进提问弹窗")
    @allure.title("精进用户提问出现精进弹窗")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ask_questin_jj_popup(self):
        pass


@allure.epic("问答中心")
@allure.feature("我的问题")
class TestMyQuestion:

    @allure.story("点赞问题")
    @allure.title("对我的问题进行点赞")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_my_question_diazan(self, go_to_question_page):
        go_to_question_page.question_dianzan()
        assert go_to_question_page.get_compent_list().judg_is_dianzan()

    @allure.story("收藏问题")
    @allure.title("对我的问题进行收藏")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_my_question_shoucang(self, go_to_question_page):
        go_to_question_page.question_collect()
        assert go_to_question_page.get_compent_list().judg_is_shoucang()

    @allure.story("评分")
    @allure.title("对我的问题主问题回复进行评分-评1星")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", "对我的问题主问题回复进行评分-评1星")
    def test_my_question_main_pingfen_1(self, go_to_question_page, content):
        go_to_question_page.question_appraise_one_star(content)
        assert go_to_question_page.get_compent_list().judge_is_score()

    @allure.story("评分")
    @allure.title("对我的问题主问题回复进行评分-评4星")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("content", "对我的问题主问题回复进行评分-评4星")
    def test_my_question_main_pingfen_4(self, go_to_question_page, content):
        go_to_question_page.question_appraise_four_star(content)
        assert go_to_question_page.get_compent_list().judge_is_score()


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("问答中心")
@allure.feature("问答精华")
class TestEssenceQuestion:

    @allure.story("问答精华列表对问题点赞")
    @allure.title("对试题进行点赞及收藏")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_essence_question_dianzan(self):
        pass


@pytest.mark.skip("未实现，暂时不执行")
@allure.epic("问答中心")
@allure.feature("搜索问题及考点")
class TestSearchQuestionAndOutline:

    @allure.story("搜索问题")
    @allure.title("搜索问题")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_question(self):
        pass

    @allure.story("搜索问题")
    @allure.title("对试题进行点赞及收藏")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_outline(self):
        pass
