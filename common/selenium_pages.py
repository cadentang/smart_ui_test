# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:页面对象及页面对象的常见操作
"""
import os
import datetime
from time import sleep

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from common.base_pages import BasePages
from common.excption import PageSelectException
from utils.get_log import logger
# from common.element import PageElement



class SeleniumPages(BasePages):
    """
    页面对象
    """
    def __init__(self, driver):
        super().__init__(driver)

    # def __getattribute__(self, attr):
    #     if attr.endswith("btn"):
    #         return PageElement(attr)

class PageWait:
    """页面等待，可通过设置此值等待页面元素加载完成"""
    def __init__(self, elm, timeout=10):
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("超时时间必须为int类型 ")

        for i in range(timeout_int):
            if elm is not None:
                if elm.is_displayed() is True:
                    break
                else:
                    sleep(1)
            else:
                sleep(1)

class PageSelect:
    """
    页面下拉框操作
    """
    def __init__(self, select_elem, value=None, text=None, index=None):
        if value is not None:
            Select(select_elem).select_by_value(value)
        elif text is not None:
            Select(select_elem).select_by_visible_text(text)
        elif index is not None:
            Select(select_elem).select_by_index(index)
        else:
            raise PageSelectException("value,text,index不能都为空")

class PageAlert:
    """警告框操作"""
    def alert(self, type_=''):
        """
        对常规警告窗的操作,确定，取消
        :param timeout:
        :param type_:
        :return:
        """
        result = WebDriverWait(self.driver, self.time, self.t).until(EC.alert_is_present())
        try:
            if type_ == '':
                if result:
                    return result
                else:
                    logger.info("alert不存在")
                return False
            elif type_ == 'yes':
                result.accept()
            elif type_ == 'no':
                result.dismiss()
            else:
                logger.info("type_参数类型 错误，仅可为yes、no、或''")
        except Exception as e:
            logger.info("警告框处理发生异常，异常信息：%s" % str(e))
            return False

    @property
    def get_alert_text(self):
        """
        获取警告框的文本信息
        """
        return self.driver.switch_to.alert.text

class PageScroll:
    """滚动条操作"""
    def window_scroll(self, width=None, height=None):
        """
        滚动条
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=width, h=height)
        self.driver.execute_script(js)

    def js_scroll_top(self):
        """
        滚动条滚到顶部
        :return:
        """
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self, x=0):
        """
        滚动条滚到底部某个位置
        :param x:
        :return:
        """
        js = f"window.scrollTo({x},document.body.scrollHeight)"
        self.driver.execute_script(js)

class PageSwitchWindowOrFrame:
    """页面窗口切换操作"""
    @property
    def current_window(self):
        """获取当前窗口的句柄"""
        return self.driver.current_window_handle

    @property
    def window_handles(self):
        """
        获取所有窗口句柄
        """
        return self.driver.window_handles

    def switch_handle(self, value):
        """
        根据传入的参数类型自动判断切换窗口
        :param value:参数类型为int/str，int：根据下标切换对应的窗口，str：根据名称切换窗口
        :return:
        """
        try:
            if isinstance(value, int):
                handles = self.driver.window_handles
                self.driver.switch_to.window(handles[value])
            elif isinstance(value, str):
                self.driver.switch_to.window(value)
            else:
                logger.info("传入的type参数 %s 错误，仅可传int、str" % type(value))
        except Exception as e:
            logger.info("切换句柄失败，错误信息：%s" % str(e))

    def switch_to_frame(self, frame_reference):
        """
        切换到frame中
        :param frame_reference: frame的定位信息：id，name等，也可传入元素对象
        :return:
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
        切换到上一级frame，如果上一级是主文档，则无效
        :return:
        """
        self.driver.switch_to.parent_frame()

    def switch_to_default_frame(self):
        """
        切换到主文档，如果已是主文档则无效
        :return:
        """
        self.driver.switch_to.default_content()


class PageKeyOperation:
    """键盘事件操作"""
    def __init__(self, element, key, control=None):
        try:
            if control is None:
                element.send_keys(key)
            else:
                element.send_keys(key, control)
        except Exception as e:
            logger.error(f"键盘操作失败,异常信息:{str(e)}")
            return False


class PageMouse:
    """鼠标事件操作"""
    def __init__(self, driver, element):
        self.driver = driver
        self.element = element

    def move_to_element(self, element):
        """
        鼠标移动到某个元素上
        :param element: 元素对象
        :return:
        """
        try:
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            logger.error("鼠标悬停操作失败,异常信息:%s" % str(e))
            return False

    def context_click(self, element):
        """
        鼠标右击
        :param element:
        :return:
        """
        try:
            ActionChains(self.driver).context_click(element).perform()
        except Exception as e:
            logger.error("鼠标右击失败,异常信息:%s" % str(e))
            return False

    def double_click(self, element):
        """
        鼠标双击
        :param element:
        :param driver:
        :return:
        """
        try:
            ActionChains(self.driver).double_click(element).perform()
        except Exception as e:
            logger.error("鼠标右击失败,异常信息:%s" % str(e))
            return False

    def click_and_hold(self, element):
        """
        鼠标按住左键不放
        :param element:
        :return:
        """
        try:
            ActionChains(self.driver).click_and_hold(element).perform()
        except Exception as e:
            logger.error("按住左键不放失败,异常信息:%s" % str(e))
            return False

    def drag_and_drop_by_offset(self, element, xoffset, yoffset):
        """
        拖动元素到指定的位置
        :param element:
        :param xoffset:
        :param yoffset:
        :return:
        """
        try:
            ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset, yoffset).perform()
        except Exception as e:
            logger.error("拖动元素失败,异常信息:%s" % str(e))
            return False

    def move_by_offset(self, xoffset, yoffset):
        """
        鼠标移动至某个地方
        :param xoffset:
        :param yoffset:
        :return:
        """
        try:
            ActionChains(self.driver).move_by_offset(xoffset, yoffset).perform()
        except Exception as e:
            logger.error("鼠标移动失败,异常信息:%s" % str(e))
            return False

    def move_to_element_with_offset(self, element, x, y):
        """
        相对element元素,移动鼠标到指定的x，y位置(相对于element元素的相对位置)
        :param element:
        :param source:
        :param x:
        :param y:
        :return:
        """
        try:
            ActionChains(self.driver).move_to_element_with_offset(element, x, y).perform()
        except Exception as e:
            logger.error("鼠标移动失败,异常信息:%s" % str(e))
            return False

    def release(self, element=None):
        """
        松开鼠标左键
        :param element:
        :return:
        """
        try:
            ActionChains(self.driver).context_click(element).perform()
        except Exception as e:
            logger.error("鼠标操作失败,异常信息:%s" % str(e))
            return False

class PageLoadOrUploadFile:
    # TODO windows方式上传还有bug，待补充
    def upload_file(self, element, file_path, browser_type, upload_type='input', sys_type='windows'):
        """
        文件上传
        :param element: 元素对象
        :param file_path: 文件路径
        :param browser_type: 浏览器类型
        :param upload_type: 上传控件类型：1.input标签上传，直接send_keys。2.非input标签，借用pywin32库
        使用 pip install -i https://pypi.douban.com/simple pywin32 安装
        win定位工具：https://sourceforge.net/projects/winspyex/  winspy
        :param sys_type: 系统类型
        :return:
        """
        if upload_type == 'input':
            element.send_keys(file_path)
        else:
            if browser_type.lower() == "chrome":
                title = "打开"
            elif browser_type.lower() == "firefox":
                title = "文件上传"
            elif browser_type.lower() == "ie":
                title = "选择要加载的文件"
            else:
                title = ""  # 待补充其它类型浏览器

            # # 找元素
            # # 一级窗口"#32770","打开"
            # dialog = win32gui.FindWindow("#32770", title)
            # # 向下传递
            # ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
            # comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
            # # 编辑按钮
            # edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
            # # 打开按钮
            # button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级
            #
            # # 输入文件的绝对路径，点击“打开”按钮
            # win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)  # 发送文件路径
            # win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮

    # TODO 文件下载
    def load_file(self, path):
        """
        文件下载
        :param path:
        :return:
        """
        pass

class PageScreenShot:
    """截图操作封装"""
    def __init__(self, img_doc):
        screen_shot_path = os.path.join(ERROR_PICTURE_PATH, str(datetime.now().strftime("%Y%m%d")))
        if not os.path.exists(screen_shot_path):
            os.makedirs(screen_shot_path)
        file_name = screen_shot_path + "\\{}_{}.png".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"), img_doc)

        self.driver.get_screenshot_as_file(file_name)
        with open(file_name, mode='rb') as f:
            file = f.read()
        allure.attach(file, img_doc, allure.attachment_type.PNG)
        logger.info("页面截图文件保存在：{}".format(file_name))





