# -*- coding: utf-8 -*-
import requests
import json

# caden之家
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=fa283adfa1e14a6239245c0c611f3453691bdf6654da29336c07ae4e57240d88'
# 用户平台测试群
# webhook = 'https://oapi.dingtalk.com/robot/send?access_token=f27935f9b3ee25b0528cfb0a37ca254c83c996bdabac1a306d33fb5909c1c69f'
message =  {
        "title": "ui自动化测试报告",
        "project": "main_station",
        "test_env": "reg",
        "developer": "caden",
        "tester": "caden",
        "total": "20",
        "pass": "10",
        "failed": "5",
        "skip": "5",
        "passing_rate": "50%",
        "test_report_address": "http://39.107.127.90:8080/job/test_pr/allure/"
    }


def send_ding(webhook, message:dict):
    """
    发送钉钉消息
    :param webhook: 目标钉钉群
    :param message: 消息主体
    {
        "title": "ui自动化测试报告地址",
        "project": "main_station",
        "test_env": "reg",
        "developer": "caden",
        "tester": "caden",
        "total": "100",
        "pass": "80",
        "failed": "10",
        "skip": "10",
        "passing_rate": "80%",
        # "testreport_address": "http://39.107.127.90:8080/job/test_pr/allure/"
        "testreport_address": "http://39.107.127.90:8080/job/test_pr/allure/"
    }
    :return:
    """
    text_string = f"# **{message['title']}**  \n### 运行项目：{message['project']}  \n### 测试环境：{message['test_env']}  \n### 开发负责人：{message['developer']} " \
                  f"\n### 测试负责人：{message['tester']} \n### 运行用例总数：{message['total']} \n### 通过条数：{message['pass']} \n### 失败条数：{message['failed']} \n### 跳过条数：{message['skip']} " \
                  f"\n### 通过率：{message['passing_rate']}\n### [详细报告地址]({message['test_report_address']})"

    if isinstance(message, dict):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "ui测试报告",
                "text": text_string
            }
        }
        headers = {"Content-Type": "application/json", "charset": "utf-8"}
        r = requests.post(webhook, data=json.dumps(data), headers=headers)
        print(r.text)
    else:
        raise ValueError("message格式错误!")

send_ding(webhook, message)
