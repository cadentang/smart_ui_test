# -*- coding: utf-8 -*-
import abc


class BaseDriver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def driver(self):
        pass

    @abc.abstractmethod
    def get_driver(self):
        pass

    @abc.abstractmethod
    def quit_driver(self):
        pass

    @abc.abstractmethod
    def close_driver(self):
        pass

