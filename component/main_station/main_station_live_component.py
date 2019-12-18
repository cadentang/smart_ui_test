# -*- coding: utf-8 -*-
from common.web_component import BaseWebComponents


class MainStationLiveListComponent(BaseWebComponents):

    def __init__(self, driver, live_id, **kwargs):
        self.live_button = None
        self.model = None
        self.lecture = None
        super().__init__(driver)

    # 进入模块详情页
    def go_to_model_detail_page(self):
        pass

    # 判断直播状态
    def judge_live_status(self):
        pass

    # 下载讲义
    def download_lecture(self):
        pass

    # 判断讲义状态
    def judge_lecture(self):
        pass

    # 进入直播
    def go_to_live_room(self):
        pass

    # 进入回放页面
    def go_to_live_playback(self):
        pass
