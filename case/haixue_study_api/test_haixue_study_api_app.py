# -*- coding: utf-8 -*-
import allure
import pytest
import json
from utils.get_log import logger


@allure.epic("haixue-study-api相关接口")
@allure.feature("haixue-study-api相关接口-APP端")
class TestHaixueAppStudyApi:

    @allure.story("商品")
    @allure.title("商品-获取用户商品信息")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_user_goods_message(self, get_app_session):
        query = {'categoryId': 9}
        params = get_app_session[0].sig_dict(query, get_app_session[2], get_app_session[3])
        rx = get_app_session[1].get(url="http://w0.highso.com.cn/study/app/customerGoods/v1/goods", params=params)
        response = json.loads(rx.text)
        print(response)
        logger.info(f"请求url地址:{rx.url}请求响应信息：{response}")
        assert response["m"] == "ok"
        assert response["s"] == 1
        assert response["data"] != ""


    @allure.story("商品")
    @allure.title("商品-保存用户选择的商品、科目和阶段")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_save_user_choose(self, get_app_session):
        url = "http://w0.highso.com.cn/study/app/operate/v1/saveGoodsChoose"
        data = {"goodsIds": [75747, 75737, 60211, 60047, 60335, 60301, 59597, 59567, 59601, 59541, 59577]}
        query, headers = get_app_session[0].sig_post_json(data, {}, get_app_session[2], get_app_session[3])
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        response = get_app_session[1].post(url=url, params=query, json=data)
        response_result = response.text

        logger.info(f"请求url地址:{response_result.url} + "" + 请求响应信息：{response_result}")
        assert response_result["m"] == "ok"
        assert response_result["s"] == 1
        assert response_result["data"] != ""