# -*- coding: utf-8 -*-


class MyException(Exception):
    """自定义异常"""

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class PageSelectException(MyException):
    """下拉框异常"""
    pass


class PageElementError(MyException):
    """页面元素异常"""
    pass


class FindElementTypesError(MyException):
    """查找元素类型错误"""
    pass