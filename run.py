# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
sys.path.append("..\\business")
sys.path.append("..\\common")
sys.path.append("..\\component")
sys.path.append("..\\config")
sys.path.append("..\\data")
sys.path.append("..\\drivers")
sys.path.append("..\\extend")
sys.path.append("..\\log")
sys.path.append("..\\pages")
sys.path.append("..\\report")
sys.path.append("..\\resource")
sys.path.append("..\\script")
sys.path.append("..\\service")
sys.path.append("..\\test_case")
sys.path.append("..\\utils")
import os
import time
import platform
from datetime import datetime
import pytest

from utils.config import ReadConfig
from utils.get_log import logger
from utils.base_path import LOG_PATH, BASE_LOG_PATH, ALLURE_REPORT_PATH, HTML_REPORT_PATH, \
    TEST_CASE_PATH, ERROR_PICTURE_PATH, PROJECT_ROOT_DIR
from utils.get_parser import get_arg
from utils import global_variable
from utils.get_allure import change_to_html
from utils.get_allure import build_environment_file, get_environment_list

Module_list = []


if __name__ == "__main__":

    """
        pytest -q 静默模式，只输出异常case
        pytest -v 详细，显示明细及case结果标志灯
        pytest casefile.py	指定case文件执行
        pytest casedir	指定路径运行
        pytest casedir/casefile::caseclass::casefunc	运行具体的case方法、类等
        pytest --pyargs pkgname	指定包执行，根据系统文件路径定位case，后期可以用pip安装包的方法部署执行case
        pytest -k "key_words_1 and not key_words_1"	执行符合key_words_1命名规则的文件、类及方法，
        忽略key_words_2命名规则的文件、类及方法
        pytest -m "mark_name"	需要在指定case方法上添加@pytest.mark.mark_name来指定方法属于哪个mark
        blocker，critical，normal，minor，trivial。用例等级
    """
    # 检查目录，目录不存在则新建
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    if not os.path.exists(BASE_LOG_PATH):
        os.mkdir(BASE_LOG_PATH)
    if not os.path.exists(TEST_CASE_PATH):
        os.mkdir(TEST_CASE_PATH)
    if not os.path.exists(ALLURE_REPORT_PATH):
        os.mkdir(ALLURE_REPORT_PATH)
    if not os.path.exists(HTML_REPORT_PATH):
        os.mkdir(HTML_REPORT_PATH)
    if not os.path.exists(ERROR_PICTURE_PATH):
        os.mkdir(ERROR_PICTURE_PATH)

    now_time = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    # 建立allure生成原始报告的目录
    xml_now_report_path = os.path.join(ALLURE_REPORT_PATH, str(datetime.now().strftime("%Y%m%d")))
    if not os.path.exists(xml_now_report_path):
        os.mkdir(xml_now_report_path)
    xml_report_path = os.path.join(xml_now_report_path, now_time)
    if not os.path.exists(xml_report_path):
        os.mkdir(xml_report_path)

    # 建立经allure转化成html报告的目录
    html_now_report_path = os.path.join(HTML_REPORT_PATH, str(datetime.now().strftime("%Y%m%d")))
    if not os.path.exists(html_now_report_path):
        os.mkdir(html_now_report_path)
    html_report_path = os.path.join(html_now_report_path, now_time)
    if not os.path.exists(html_report_path):
        os.mkdir(html_report_path)

    # 获取代码运行的平台信息
    platform_name = platform.platform()
    logger.info(f"platform_name: {platform_name}" )
    if "Windows" in platform_name:
        platform_target = "win"
    elif "Linux" in platform_name:
        platform_target = "linux"
    elif "Mac" in platform_name:
        platform_target = "mac"
    else:
        ValueError("注意检查程序运行平台信息")

    # 设置全局变量值
    global_variable._init()
    globle_arg = get_arg()
    print(globle_arg)
    global_variable.set_value("get_arg", globle_arg)
    global_variable.set_value("platform", platform_target)
    global_variable.set_value("selenium_grid", globle_arg["selenium_grid"])
    print(ReadConfig(globle_arg).get_config())
    global_variable.set_value("config_dict", ReadConfig(globle_arg).get_config())
    logger.info(f"运行的全局变量: {globle_arg}")

    # 获取运行的模块
    run_module = globle_arg["module"]
    case_list = []
    # base_command_arg = [f"--alluredir={xml_report_path}"]
    base_command_arg = ["--alluredir=./allure-results"]

    if globle_arg["project"] == "main_station":
        path = os.listdir(TEST_CASE_PATH + "/test_main_station")
        if "all" in globle_arg["module"]:
            case_path = TEST_CASE_PATH + "/test_main_station"
            case_list.append(case_path)
            base_command_arg.append(case_path)
        elif globle_arg["module"] is not "":
            for i in range(len(run_module.split(","))):
                for j in range(len(path)):
                    if run_module.split(",")[i] == path[j]:
                        case_list.append(TEST_CASE_PATH + "/test_main_station/" + run_module.split(",")[i])
                        base_command_arg.append(TEST_CASE_PATH + "/test_main_station/" + run_module.split(",")[i])
        else:
            logger.info("所选用例模块为空，不能运行！")

    logger.info(f"运行的测试模块: {case_list}")

    pytest.main(base_command_arg)
    # pytest.main([f"--alluredir={xml_report_path}", case_path_home,case_path_login])
    # pytest.main([f"--alluredir={xml_report_path}", TEST_CASE_PATH+"/test_main_station/test_main_station_home", '--workers=1','--tests-per-worker=2'])

    # 将环境信息置于xml报告路径下，转化为html报告后在html中呈现
    # build_environment_file(xml_report_path, get_environment_list())
    local_path = PROJECT_ROOT_DIR + "/allure-results"
    build_environment_file(local_path, get_environment_list())
    # 使用allure将xml报告生成为html报告
    time.sleep(10)
    change_to_html(xml_report_path, html_report_path)
    logger.info("测试任务完成！")






