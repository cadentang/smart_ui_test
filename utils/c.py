# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:
"""
# from appium import webdriver
# import time
# def aaa():
#
#     desired_caps = {}
#     desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
#     desired_caps['platformVersion'] = '9' #android系统的版本号
#     # desired_caps['deviceName'] = '' #手机设备名称，通过adb devices 查看
#     desired_caps['deviceName'] = 'Honor 10 Lite' #手机设备名称，通过adb devices 查看
#     desired_caps['appPackage'] = 'com.haixue.app.android.HaixueAcademy.h4' #apk的包名
#     desired_caps['appActivity'] = 'com.haixue.academy.main.WelcomeActivity' #apk的launcherActivity
#     desired_caps['udid'] = '79UDU19823022285' #apk的launcherActivity
#     # desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
#     # desired_caps['platformVersion'] = '5.1.1' #android系统的版本号
#     # desired_caps['deviceName'] = '127.0.0.1:62027' #手机设备名称，通过adb devices 查看
#     # desired_caps['unicodeKeyboard'] = True # 使用unicodeKeyboard的编码方式来发送字符串
#     # desired_caps['resetKeyboard'] = True  # # 将键盘给隐藏起来
#     driver = webdriver.Remote('http://127.0.0.1:4725/wd/hub', desired_caps) ##启动服务器地址，后面跟的是手机信息

if __name__ == "__main__":
    from selenium import webdriver

    """
    node注册：java -Dwebdriver.chrome.driver=/path/to/chromedriver.exe 
    -jar /Users/admin/selenium-server-standalone-3.14.0.jar -role node -hub http://<IP_GRID_HUB>:4444/grid/register
    """

    chrome_driver = "D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_79.exe"
    chrome_capabilities = {
        "browserName": "chrome",  # 浏览器名称
        "version": "80",  # 操作系统版本
        "platform": "windows",  # 平台，这里可以是windows、linux、andriod等等
        "javascriptEnabled": True,  # 是否启用js
        # "webdriver.chrome.driver": chrome_driver
    }
    driver = webdriver.Remote(command_executor="http://192.168.124.10:5555/wd/hub", desired_capabilities=chrome_capabilities)
    # driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("http://w2.highso.com.cn/v5")