# -*- coding: utf-8 -*-
# import allure
import pytest
import json
# from utils.get_log import logger


# @allure.epic("测试haixue-study-api服务")
# @allure.feature("测试haixue-study-api服务的pc端接口")
class TestHaixueStudyApi1232:

    # @allure.story("获取用户直播日历数据")
    # @allure.title("获取用户直播日历数据-购买用户")
    # @allure.severity(allure.severity_level.BLOCKER)
    def test_go_to_live_module_99(self, get_pc_session):
        rx = get_pc_session.get(url="http://w0.highso.com.cn/study/pc/live/timeLimitLive?categoryId=9")
        response = json.loads(rx.text)
        print(response)
        # logger.info(f"请求url地址:{rx.url}请求响应信息：{response}")
        assert response["code"] == 200
        assert response["msg"] == None
        assert response["data"] != ""

      # se = requests.session()
    # header1 = {"Content-type":"application/json"}
    # data1 = {"account": "19983271081",
    #         "password": "e10adc3949ba59abbe56e057f20f883e",
    #         "needServiceToken": "true",
    #         "systemCode": "haixue-upcore-api"}
    #
    # re = se.post(url="http://w0.highso.com.cn/passport-api/auth/pwd", data=json.dumps(data1), headers=header1)
    # service_token = json.loads(re.text)["data"]["serviceToken"]
    # get_cookie = requests.utils.dict_from_cookiejar(re.cookies)
    # header2 = {"Cookie": f"pass_sec={get_cookie['pass_sec']};deviceType=NORMAL; pageNum=0"}
    # get_url = f"http://w0.highso.com.cn/upcore/serviceToken/validate?serviceToken={service_token}&deviceType=NORMAL&pageNum=0&bdVid"
    # r = se.get(url=get_url)
    # rx = se.get(url="http://w0.highso.com.cn/study/pc/live/timeLimitLive?categoryId=9")
    # print(rx.text)






