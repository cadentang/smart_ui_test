# -*- coding: utf-8 -*-
import argparse

def get_arg():
    """
    自定义python命令行参数:
    1.--env: 指定运行环境，环境参数，命令行形式：python run.py --env test0,不传则默认reg环境
            环境参数列表:["test0", "test1", "test2", "reg", "stage", "auto", "prod"]
    2.--project: 指定运行项目，支持传入多个项目，如：python run.py --project project01，project02
            项目名称取/test_case下的一级名称，如主站：test_main_station,项目名则为main_station
            项目列表：["all", "main_station"]
    3.--user_port:指定项目运行的端，支持多端运行，端列表：["pc", "andriod", "ios", "h5", "mini_program"]
    4.--pattern: 指定用例运行模式，运行模式列表：["local", "distributed"]
            local: selenium,appium服务均在本地启动
            distributed：分布式执行，selenium，appium服务在远端运行，执行时临时注册node节点
    5.--browser: 浏览器运行列表:["chrome", "firefox", "ie"]
    """
    run_arg = {}
    ENV_LIST = ["test0", "test1", "test2", "reg", "stage", "auto", "prod"]
    PROJECT_LIST = ["all", "main_station"]
    USER_PORT = ["pc", "andriod", "ios", "h5", "mini_program"]
    PATTERN = ["local", "distributed"]
    BROWSER = ["chrome", "firefox", "ie"]

    parser = argparse.ArgumentParser(description="自定义HaiXue项目python命令行参数")
    parser.add_argument('--env', type=str, default="reg")
    parser.add_argument('--project', type=str, default="main_station")
    parser.add_argument('--user_port', type=str, default="pc")
    parser.add_argument('--pattern', type=str, default="local")
    parser.add_argument('--browser', type=str, default="chrome")
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

    if args.browser in BROWSER:
        run_arg["browser"] = args.browser
    else:
        run_arg["browser"] = "chrome"

    return run_arg

