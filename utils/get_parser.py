# -*- coding: utf-8 -*-
import argparse
from utils.base_path import LOG_PATH, DRIVER_PATH

def get_arg():
    """
    自定义python命令行参数:
    1.--env: 指定运行环境，环境参数，命令行形式：python run.py --env test0,不传则默认reg环境
            环境参数列表:["test0", "test1", "test2", "reg", "stage", "auto", "prod"]
    2.--project: 指定运行项目，支持传入多个项目，如：python run.py --project project01，project02
            项目名称取/test_case下的一级名称，如主站：test_main_station,项目名则为main_station
            项目列表：["all", "main_station"]
    3.--user_port:指定项目运行的平台，平台列表：["win", "mac", "andriod", "ios", "linux"], 分布式运行有效
    4.--pattern: 指定用例运行模式，运行模式列表：["local", "distributed"]
            local: selenium,appium服务均在本地启动
            distributed：分布式执行，selenium，appium服务在远端运行，执行时临时注册node节点
    5.--browser: 浏览器运行列表:["chrome", "firefox", "ie"]
    6.--version: 运行的版本:["78"]，这个版本只写大的版本，如果是andriod或者iOS运行是模拟器的版本
    7.--log_path: 运行日志路径，本地调试是在项目根目录/log下，默认值，传入的日志路径为在jenkins上运行的日志存储路径，
                  注意如果jenkins存在在slave节点上运行时，这个路径为节点机器所在的日志路径
    8.--driver_path: 运行selenium脚本所需的driver路径
    9.--app_path: 运行appium脚本时app安装包所在的路径
    10.--app_path: 运行appium脚本时app安装包所在的路径
    11.--app_path: 运行appium脚本时app安装包所在的路径
    12.--selenium_grid: 分布式运行时hub节点地址
    """
    run_arg = {}
    ENV_LIST = ["test0", "reg", "stage", "auto", "prod"]
    PROJECT_LIST = ["main_station", "haixue_app", "exam_api"]
    USER_PORT = ["win", "mac", "andriod", "ios", "linux"]
    PATTERN = ["local", "distributed"]
    BROWSER = ["chrome", "firefox", "ie", "safari"]
    MODULE = ["test_main_station_home", "test_main_station_login", "test_main_station_register", "test_main_station_course",
              "test_main_station_exam", "test_main_station_question"]
    parser = argparse.ArgumentParser(description="自定义HaiXue项目python命令行参数")
    parser.add_argument('--env', type=str, default="stage", choices=ENV_LIST)
    parser.add_argument('--project', type=str, default="main_station", choices=PROJECT_LIST)
    parser.add_argument('--module', type=str, default="test_main_station_home")
    parser.add_argument('--user_port', type=str, default="win", choices=USER_PORT)
    parser.add_argument('--pattern', type=str, default="distributed", choices=PATTERN)
    parser.add_argument('--browser', type=str, default="firefox", choices=BROWSER)
    parser.add_argument('--version', type=str, default=None)
    parser.add_argument('--log_path', type=str, default=LOG_PATH)
    parser.add_argument('--driver_path', type=str, default=DRIVER_PATH)

    # app相关参数
    parser.add_argument('--app_path', type=str, default=None)
    parser.add_argument('--platformName', type=str, default=None)
    parser.add_argument('--platformVersion', type=str, default=None)
    parser.add_argument('--deviceName', type=str, default=None)
    parser.add_argument('--appPackage', type=str, default=None)
    parser.add_argument('--appActivity', type=str, default=None)
    parser.add_argument('--noReset', type=str, default=False)
    parser.add_argument('--udid', type=str, default=False)
    parser.add_argument('--unicodeKeyboard', type=str, default=False)
    parser.add_argument('--resetKeyboard', type=str, default=False)
    parser.add_argument('--automationName', type=str, default=False)
    parser.add_argument('--bundleId', type=str, default=False)
    parser.add_argument('--selenium_grid', type=str, default="http://127.0.0.1:4723/wd/hub")
    parser.add_argument('--desired_caps', type=str, default={
                                                                "platformName": "Android",
                                                                "platformVersion": "10",
                                                                "deviceName": "device",
                                                                "appPackage": "com.haixue.app.android.HaixueAcademy.h4",
                                                                "appActivity": "com.haixue.academy.main.WelcomeActivity",
                                                                # "noReset": True,
                                                                "unicodeKeyboard": True,
                                                                "resetKeyboard": True
                                                            })

    args = parser.parse_args()
    if args.env in ENV_LIST:
        run_arg["env"] = args.env
    else:
        run_arg["env"] = "reg"
    if args.project in PROJECT_LIST:
        run_arg["project"] = args.project
    else:
        run_arg["project"] = "main_station"

    if args.user_port in USER_PORT:
        run_arg["user_port"] = args.user_port
    else:
        run_arg["user_port"] = "pc"

    if args.pattern in PATTERN:
        run_arg["pattern"] = args.pattern
    else:
        run_arg["pattern"] = "local"

    run_arg["module"] = args.module

    if args.browser in BROWSER:
        run_arg["browser"] = args.browser
    else:
        run_arg["browser"] = "chrome"

    run_arg["version"] = args.version
    run_arg["log_path"] = args.log_path
    run_arg["driver_path"] = args.driver_path
    run_arg["selenium_grid"] = args.selenium_grid

    # app相关参数
    run_arg["app_path"] = args.app_path
    run_arg["platformName"] = args.platformName
    run_arg["platformVersion"] = args.platformVersion
    run_arg["deviceName"] = args.deviceName
    run_arg["appPackage"] = args.appPackage
    run_arg["noReset"] = args.noReset
    run_arg["udid"] = args.udid
    run_arg["unicodeKeyboard"] = args.unicodeKeyboard
    run_arg["resetKeyboard"] = args.resetKeyboard
    run_arg["automationName"] = args.automationName
    run_arg["bundleId"] = args.bundleId
    run_arg["desired_caps"] = args.desired_caps

    return run_arg


if __name__ == "__main__":
    print(get_arg())

