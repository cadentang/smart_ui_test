# -*- coding: utf-8 -*-
import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])  # 项目根目录
BASE_CONFIG_PATH = os.path.join(PROJECT_ROOT_DIR, "config/config.yaml")  # 基础配置文件路径
BASE_LOG_PATH = os.path.join(PROJECT_ROOT_DIR, "log\\base_log")  # 用例运行日志文件路径
LOG_PATH = os.path.join(PROJECT_ROOT_DIR, "log")  # 日志文件路径
ALLURE_REPORT_PATH = os.path.join(PROJECT_ROOT_DIR, "report/allure_report/")  # 生成的未转化的allure报告路径
HTML_REPORT_PATH = os.path.join(PROJECT_ROOT_DIR, "report/html_report/")  # allure转化为html报告路径
TEST_REPORT_PATH = os.path.join(PROJECT_ROOT_DIR, "report/")  # 测试报告路径
DRIVER_PATH = os.path.join(PROJECT_ROOT_DIR, "drivers")  # 浏览器driver路径
RESOURCE_PATH = os.path.join(PROJECT_ROOT_DIR, "resource")  # 测试资源路径，如图片、音频、文件等
TEST_CASE_PATH = os.path.join(PROJECT_ROOT_DIR, "case")  # 测试用例路径
ERROR_PICTURE_PATH = os.path.join(PROJECT_ROOT_DIR, "report/error_picture")  # 错误截图
PAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "pages")  # 页面对象路径
BUSINESS_PATH = os.path.join(PROJECT_ROOT_DIR, "business")  # 业务层封装路径
APP_PATH = os.path.join(PROJECT_ROOT_DIR, "app")  # app安装包放置的路径
DOWNLOAD_LECTURE_PATH = os.path.join(PROJECT_ROOT_DIR, "resource\lecture")  # 讲义下载路径