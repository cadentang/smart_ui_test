# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:selenium grid分布式测试
"""
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread

from utils.config import DRIVER_PATH

chrome_driver = DRIVER_PATH + '\\chromedriver.exe'
firefox_driver = DRIVER_PATH + '\\geckodriver.exe'
plantomjs_driver = DRIVER_PATH + '\\plantomjs.exe'

slave_chrome_driver_path = 'F:/grid/chromedriver.exe'

chrome_capabilities = {
    "browserName": "chrome",        # 浏览器名称
    "version": "",                  # 操作系统版本
    "platform": "windows",              # 平台，这里可以是windows、linux、andriod等等
    "javascriptEnabled": True,      # 是否启用js
    "webdriver.chrome.driver": "F:/grid/chromedriver.exe"  # node主机上的driver
}

lists = [
    ['http://192.168.0.103:6666/wd/hub', 'firefox', 'webdriver.chrome.driver', slave_chrome_driver_path],
    ['http://192.168.0.141:5555/wd/hub', 'firefox', 'webdriver.firefox.driver', firefox_driver],
    ['http://192.168.0.141:5556/wd/hub', 'chrome', 'webdriver.chrome.driver', chrome_driver]]

for list in lists:
    driver = webdriver.Remote(command_executor=list[0],
                              desired_capabilities={
                                  'platform': 'windows',
                                  'browserName': 'chrome',
                                  'version': '',
                                  'javascriptEnabled': True,
                                  'webdriver.chrome.driver': 'D:\\my-git-project\\91lng\\selenium_91lng_auto_test\\drivers\\chromedriver.exe'
                              })

    driver.get('http://www.baidu.com')
    driver.find_element_by_id('kw').send_keys("selenium")
    driver.find_element_by_id('su').click()

