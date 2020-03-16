# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:
"""
from appium import webdriver
import time
def aaa():

    desired_caps = {}
    desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
    desired_caps['platformVersion'] = '9' #android系统的版本号
    # desired_caps['deviceName'] = '' #手机设备名称，通过adb devices 查看
    desired_caps['deviceName'] = 'Honor 10 Lite' #手机设备名称，通过adb devices 查看
    desired_caps['appPackage'] = 'com.haixue.app.android.HaixueAcademy.h4' #apk的包名
    desired_caps['appActivity'] = 'com.haixue.academy.main.WelcomeActivity' #apk的launcherActivity
    desired_caps['udid'] = '79UDU19823022285' #apk的launcherActivity
    # desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
    # desired_caps['platformVersion'] = '5.1.1' #android系统的版本号
    # desired_caps['deviceName'] = '127.0.0.1:62027' #手机设备名称，通过adb devices 查看
    # desired_caps['unicodeKeyboard'] = True # 使用unicodeKeyboard的编码方式来发送字符串
    # desired_caps['resetKeyboard'] = True  # # 将键盘给隐藏起来
    driver = webdriver.Remote('http://127.0.0.1:4725/wd/hub', desired_caps) ##启动服务器地址，后面跟的是手机信息

if __name__ == "__main__":
    aaa()