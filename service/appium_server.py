# -*- coding: utf-8 -*-
__author__ = 'caden'

import os
import socket
import multiprocessing
import subprocess
from time import sleep

from common.check_port import check_port, release_port
from common.desired_caps import appium_desired
from common.log import logging


devices_list = ['127.0.0.1:62025']

class StartAppiumServer:

    def __init__(self):
        pass


    def appium_start(self, host, port):
        """启动appium服务"""
        bootstrap_port = str(port + 1)
        cmd = 'start /b appium -a ' + host + ' -p ' + str(port) + ' -bp ' + str(bootstrap_port)
        subprocess.Popen(cmd, shell=True, stdout=open('../log/appium_log/' + str(port) + '.log', 'a'),
                         stderr=subprocess.STDOUT)


    def start_appium_action(host, port):
        """启动appium时检查端口是否可用"""
        if check_port(host, port):
            appium_start(host, port)
        else:
            logging.info('appium %s %s 启动失败，开始释放端口' % (host, port))
            release_port(port)
            appium_start(host, port)


    def start_devices_action(host, port):
        """启动测试对象"""
        driver = appium_desired(host, port)
        return driver


    def multi_appium_start(host):
        """多进程启动appium服务"""
        logging.info("====appium服务开始启动====")
        appium_process = []

        for i in range(len(devices_list)):
            port = 4723 + 2*i
            # 依次开启进程，将进程添加到进程组里面
            appium_service = multiprocessing.Process(target=start_appium_action, args=(host, port))
            appium_process.append(appium_service)

        for appium in appium_process:
            appium.start()
        for appium in appium_process:
            appium.join()
        sleep(10)
        logging.info("====appium服务启动结束====")


    def multi_devices_start(host):
        """多进程启动测试对象"""
        logging.info("====测试对象开始启动====")
        desired_process = []

        p = multiprocessing.Pool(len(devices_list))
        results = []
        pid = []
        driver_list = []
        for i in range(len(devices_list)):
            port = 4723 + 2 * i
            # desired = multiprocessing.Process(target=start_devices_action, args=(host, port))
            # desired_process.append(desired)
            results.append(p.apply_async(start_devices_action, (host, port)))
            pid.append(os.getpid())

        for desired in desired_process:
            desired.start()
        for desired in desired_process:
            desired.join()
        # 获取每个子进程函数的返回值
        for res in results:
            # for i in range(len(pid)):
            #     driver_dict[pid[i]] = res.get()
            driver_list.append(res.get())
        sleep(5)
        logging.info("====测试对象启动完毕====")
        return driver_list


    def main_run(host):
        """启动appium和测试对象的函数"""
        multi_appium_start(host)
        driver_d = multi_devices_start(host)
        return driver_d


def check_port(host, port):
    """检查端口是否被占用"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket的TCP连接
    try:
        s.connect((host, port))
        s.shutdown(2)
    except OSError as msg:
        logging.info("端口:%s可以被使用！" % port)
        return True
    else:
        logging.info("端口:%s已经被使用！" % port)
        return False

def release_port(port):
    """释放已经被占用的端口"""
    cmd_find_pid = "netstat -aon | findstr %s" % port  # 查找该端口信息

    result = os.popen(cmd_find_pid).read()
    if str(port) and 'LISTENING' in result:
        i = result.index('LISTENING')
        start = i + len('LISTENING') + 7
        end = result.index('\n')
        pid = result[start:end]

        cmd_kill = 'taskkill -f -pid %s' % pid  # 释放该端口
        os.popen(cmd_kill)
    else:
        logging.info("端口:%s可以被使用！" % port)


