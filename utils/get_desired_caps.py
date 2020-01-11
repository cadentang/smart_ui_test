# -*- coding: utf-8 -*-

def get_desired_caps(desired_type, data):
    """配置"""
    if desired_type == "selenium":
        desired_caps = {
            'platform': 'windows',
            'browserName': 'chrome',
            'version': '',
            'javascriptEnabled': True,
            'webdriver.chrome.driver': 'D:\haixue_work\script\haixue_git\haixue-test-ui\drivers\chrome\chromedriver_win_78.exe'
        }
    elif desired_type == "appium":
        desired_caps = {
            "platformName": data['platformName'],
            "platformVersion": data["platformVersion"],
            "deviceName": data["deviceName"],
            "app": data["app_path"],
            "appPackage": data["appPackage"],
            "appActivity": data["appActivity"],
            "noReset": False,
            "udid": data["udid"],
            "unicodeKeyboard": True,
            "resetKeyboard": True
        }
    else:
        raise ValueError("desired_type只能是selenium或者appium！")

    return desired_caps
