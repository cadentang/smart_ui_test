# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:js相关操作封装
"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

# from utils.log import logger


class JsElement:
    """
    css
    >> from js import CSSElement
    >> class MyPage(Page):
            input = CSSElements('.sk')
            button = CSSElements('#su')
    """

    driver = None

    def __init__(self, css, index=None, describe=None):
        self.css = css
        if index is None:
            self.index = "0"
        else:
            self.index = str(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def clear(self):
        """
        清除文本中的内容，只支持css语法
        """
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.border="2px solid red";
                    elm.value = "";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def set_text(self, value):
        """
        文本框输入值
        :param value:
        :return:
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.border="2px solid red";
                    elm.value = "{value}";""".format(css=self.css, index=self.index, value=value)
        driver.execute_script(js)

    def click(self):
        """
        js点击
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                   elm.style.border="2px solid red";
                   elm.click();""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def click_display(self):
        """
        点击可见的元素，否则跳过
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = 'var elm = document.querySelector("' + self.css + '");' \
             ' if(elm != null){elm.style.border="2px solid red";elm.click();}'
        driver.execute_script(js)

    def display(self):
        """
        显示隐藏你给的元素
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.display = "block";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def remove_attribute(self, attribute):
        """
        移除元素某个属性
        :param attribute:
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.removeAttribute("{attr}");""".format(css=self.css, index=self.index, attr=attribute)
        driver.execute_script(js)

    def set_attribute(self, attribute, value):
        """
        设置元素的某个属性
        :param attribute:
        :param value:
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.setAttribute("{attr}", "{value}");
                    """.format(css=self.css, index=self.index, attr=attribute, value=value)
        driver.execute_script(js)

    def clear_style(self):
        """
        清除元素的样式
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style="";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def clear_class(self):
        """
        Js清除元素的class
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                     elm.removeAttribute("class");""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def inner_text(self, text):
        """
        设置元素的text值
        :param text: 文本
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                     elm.innerText="{text}";""".format(css=self.css, index=self.index, text=text)
        driver.execute_script(js)

    def remove_child(self, index=0):
        """
        移除元素的某个子节点，如一个下拉框的某个选项，index方式
        :param index: 索引
        """
        logger.info("元素的当前操作: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelector("{css}");
                    elm.removeChild(elm.childNodes[{index}]);""".format(css=self.css, index=str(index))
        driver.execute_script(js)





