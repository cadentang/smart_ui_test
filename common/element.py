# -*- coding: utf-8 -*-
import types
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.get_log import logger

LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,

    # appium-andriod特有元素定位方法
    'ios_uiautomation': MobileBy.IOS_UIAUTOMATION,
    'ios_predicate': MobileBy.IOS_PREDICATE,
    'ios_class_chain': MobileBy.IOS_CLASS_CHAIN,
    'android_uiautomator': MobileBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': MobileBy.ANDROID_VIEWTAG,
    'android_datamatcher': MobileBy.ANDROID_DATA_MATCHER,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
    'custom': MobileBy.CUSTOM,
}


class Element:
    """单个页面元素"""
    def __init__(self, context=False, timeout=5, describe=None, **kwargs):
        self.time_out = timeout
        if not kwargs:
            raise ValueError("请传入一个定位！")
        if len(kwargs) > 1:
            raise ValueError("请仅传入一个定位！")
        self.key, self.value = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[self.key], self.value)
        except KeyError:
            raise KeyError(f"请使用以下定位方法：{LOCATOR_LIST}")
        self.has_context = bool(context)

    def get_element(self, driver):
        """定位元素并将定位的元素红色高亮显示"""
        try:
            ele = driver.find_element(*self.locator)
        except NoSuchElementException:
            return None
        else:
            try:
                style_red = 'arguments[0].style.border="2px solid red"'
                driver.execute_script(style_red, ele)
            except BaseException:
                return ele
            return ele

    def find(self, driver):
        """多次查找元素"""
        for i in range(1, self.time_out):
            logger.info(f"第{i}次搜索元素：{self.locator} ")
            if self.get_element(driver) is not None:
                return self.get_element(driver)
        else:
            return self.get_element(driver)

    # def is_selected(self, driver):
    #     """判断元素是否被选中，返回bool值 及点（选中/取消选中）"""
    #
    #
    #     ele = self.get_element(driver)
    #     try:
    #         if type_ == '':
    #             r = ele.is_selected()
    #             return r
    #         elif type_ == 'click':  # 如果type参数为click，执行元素的点击操作
    #             ele.click()
    #         else:
    #             print(f"type参数 {type_} 错误，仅可为click或''")
    #     except Exception as e:
    #         logger.info("元素定位错误，错误信息：%s" % str(e))
    #         return False

    def is_element_dom_exist(self, locator):
        """
        判断单个元素是否在DOM里面,不一定显示
        :param locator:
        :return:
        """
        try:
            self.find_element(locator)
            return True
        except Exception as e:
            logger.info("元素定位错误，错误信息：%s" % str(e))
            return False

    def is_element_dom_exists(self, locator):
        """
        判断一组元素是否在DOM里面,不一定显示，若不存在，返回一个空的list
        :param locator: 定位元素的方式和值，类型为元组，如：("id", "value1")
        :return:
        """
        ''' 判断一组元素是否在DOM里面 （是否存在），若不存在，返回一个空的list'''
        element = self.find_elements(locator)
        n = len(element)
        if n == 0:
            return False
        elif n == 1:
            return True
        else:
            logger.info(f"定位到元素的个数：{n}")
            return True

    # def __getattribute__(self, attr):
    #     if attr.startswith('p_') or attr.startswith('_p_'):
    #         _proxy = self.resolve_poco(self._dict[attr][1])  #获取对应元素操作对象的代理
    #         _proxy._name = self._dict[attr][0]   #绑定注释信息
    #         _proxy.click = types.MethodType(allure_click, _proxy)  #绑定click方法
    #         return _proxy
    #     else:
    #         return object.__getattribute__(self, attr)

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            driver = instance.driver

        return self.find(driver)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("描述符不支持这这种形式")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("元素未找到，不能设置值")
        elem.send_keys(value)


class Elements(Element):
    """
    定位多个或一组元素
    """
    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("描述符不支持这这种形式")
        elems = self.__get__(instance, instance.__class__)

        if not elems:
            raise ValueError("元素组未找到")
        [elem.send_keys(value) for elem in elems]




