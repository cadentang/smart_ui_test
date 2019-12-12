# -*- coding: utf-8 -*-
import os
import sys
from importlib import import_module
# from pages.main_station import main_station_login_page


class App:
    """属性拦截，访问/pages下面所有的页面时都会先经过此属性拦截类"""
    def __init__(self, driver):
        self._driver = driver

    # 属性拦截，获取应用的一个目标页面对象
    def __getattribute__(self, attr):
        goal_page = None
        goal_business = None
        if attr.endswith("page"):
            # models = sys.modules[__name__]
            models = import_module("pages.main_station." + attr)
            for item in models.__dict__:
                if item.endswith("Page"):
                    goal_page = getattr(models, item)
            # goal_page = getattr(attr, i)
            # for item in models.__dict__:
            #     if item.endswith("page"):
            #         models_page = models.__dict__[item]
            #         # print(models_page)
            #         for i in models_page.__dict__:
            #             if i.endswith("Page"):
            #                 goal_page = getattr(models_page, i)
            #                 # print(goal_page)
            return goal_page(self._driver)
        elif attr.endswith("business"):
            models = import_module("business.main_station." + attr)
            for item in models.__dict__:
                if item.endswith("Business"):
                    goal_business = getattr(models, item)
            # models = sys.modules[__name__]
            # for item in models.__dict__:
            #     if item.endswith("business"):
            #         models_business = models.__dict__[item]
            #         for i in models_business.__dict__:
            #             if i.endswith("Business"):
            #                 goal_business = getattr(models_business, i)
            return goal_business(self._driver)
        else:
            return object.__getattribute__(self, attr)

