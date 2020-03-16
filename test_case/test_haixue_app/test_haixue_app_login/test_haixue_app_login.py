# -*- coding: utf-8 -*-
import allure
from pages.main_station.main_station_home_page import MainStationHomePage


@allure.feature("嗨学课堂登录测试")
class TestHaixueAppLogin:

    @allure.story("上导航未登录状态下点击及数据对比测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_top_nav_not_login(self, get_driver):
        home_page = MainStationHomePage(get_driver)
        for i in home_page.get_not_login_home_top_navigation().values():
            home_page.traverse_page(i)

def aaa():
    from appium import webdriver
    import time
    desired_caps = {}
    desired_caps['platformName'] = 'Android' #android的apk还是IOS的ipa
    desired_caps['platformVersion'] = '5.1.1' #android系统的版本号
    desired_caps['deviceName'] = '127.0.0.1:62027' #手机设备名称，通过adb devices 查看
    desired_caps['appPackage'] = 'com.haixue.app.android.HaixueAcademy.h4' #apk的包名
    desired_caps['appActivity'] = 'com.haixue.academy.main.WelcomeActivity' #apk的launcherActivity
    # desired_caps['unicodeKeyboard'] = True # 使用unicodeKeyboard的编码方式来发送字符串
    # desired_caps['resetKeyboard'] = True  # # 将键盘给隐藏起来
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps) ##启动服务器地址，后面跟的是手机信息

if __name__ == "__main__":
    aaa()