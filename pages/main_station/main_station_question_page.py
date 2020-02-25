# -*- coding: utf-8 -*-
from common.element import Element
from pages.main_station.main_station_base_page import MainStationBasePage


class MainStationQuestionPage(MainStationBasePage):
    """问答页面"""
    _my_question_span = Element(css="li.ant-menu-item.ant-menu-item-selected>span", describe="我的问题")
    _article_question_span = Element(css="li.ant-menu-item.ant-menu-item-selected>span", describe="问答精华")
    _question_span = Element(css="li.ant-menu-item.ant-menu-item-selected>span", describe="我要提问")
    _question_input = Element(css="div>span>input", describe="问题、考点输入框")
    _question_button = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="我要提问")

    _question_source_my_question_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题来源-我提问的")
    _question_source_my_collect_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题来源-我收藏的")
    _question_type_live_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题类型-直播回放问题")
    _question_type_video_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题类型-视频问题")
    _question_type_exam_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题类型-试题问题")
    _question_type_textbook_input = Element(xpath="//div/button[contains(text(),'我要提问')]", describe="问题类型-教材问题")

    # _question_list_component_li = "ul.ant-list-items>li"
    _question_list_component_li = ("css", "ul.ant-list-items>li")  # 定位问题列表组件