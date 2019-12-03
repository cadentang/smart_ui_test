# -*- coding: utf-8 -*-
__author__ = 'caden'


class MyException(Exception):
    """
    自定义异常
    """

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
    """
    下拉框异常
    """
    pass


class PageElementError(MyException):
    """
    Raises an error using the PagElement class
    """
    pass


class FindElementTypesError(MyException):
    """
    Find element types Error
    """
    pass