# -*- coding: utf-8 -*-
import os
import socket
import multiprocessing
import subprocess
from time import sleep

import yaml
from appium.webdriver import webdriver

from utils.get_log import logging

devices_list = ['127.0.0.1:62025']

class StartAppiumServer:

    def __init__(self):
        pass

    def appium_start(self, host, port):
        """启动appium服务"""
        bootstrap_port = str(port + 1)
        cmd = 'start /b appium -a ' + host + ' -p ' + str(port) + ' -bp ' + str(bootstrap_port)
        subprocess.Popen(cmd, shell=True, stdout=open('./' + str(port) + '.log', 'a'),
                         stderr=subprocess.STDOUT)

    def start_appium_action(self, host, port):
        """启动appium时检查端口是否可用"""
        if check_port(host, port):
            self.appium_start(host, port)
        else:
            logging.info(f'appium {host} {port} 启动失败，开始释放端口')
            release_port(port)
            self.appium_start(host, port)

    def start_devices_action(self, host, port):
        """启动测试对象"""
        driver = appium_desired(self, host, port)
        return driver

    def stop_appium(self, post_num=4723):
        '''关闭appium服务'''
        if pc.upper() == 'WIN':
            p = os.popen(f'netstat  -aon|findstr {post_num}')
            p0 = p.read().strip()
            if p0 != '' and 'LISTENING' in p0:
                p1 = int(p0.split('LISTENING')[1].strip()[0:4])  # 获取进程号
                os.popen(f'taskkill /F /PID {p1}')  # 结束进程
                print('appium server已结束')
        elif pc.upper() == 'MAC':
            p = os.popen(f'lsof -i tcp:{post_num}')
            p0 = p.read()
            if p0.strip() != '':
                p1 = int(p0.split('\n')[1].split()[1])  # 获取进程号
                os.popen(f'kill {p1}')  # 结束进程
                print('appium server已结束')

    def multi_appium_start(self, host):
        """多进程启动appium服务"""
        logging.info("====appium服务开始启动====")
        appium_process = []

        for i in range(len(devices_list)):
            port = 4723 + 2*i
            # 依次开启进程，将进程添加到进程组里面
            appium_service = multiprocessing.Process(target=self.start_appium_action, args=(host, port))
            appium_process.append(appium_service)

        for appium in appium_process:
            appium.start()
        for appium in appium_process:
            appium.join()
        sleep(10)
        logging.info("====appium服务启动结束====")

    def multi_devices_start(self, host):
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
            results.append(p.apply_async(self.start_devices_action, (host, port)))
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

    def main_run(self, host):
        """启动appium和测试对象的函数"""
        self.multi_appium_start(host)
        driver_d = self.multi_devices_start(host)
        return driver_d


def check_port(host, port):
    """检查端口是否被占用"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket的TCP连接
    try:
        s.connect((host, port))
        s.shutdown(2)
    except OSError as msg:
        logging.info(f"端口:{port}可以被使用！")
        return True
    else:
        logging.info(f"端口:{port}已经被使用！")
        return False

def release_port(port):
    """释放已经被占用的端口"""
    cmd_find_pid = f"netstat -aon | findstr {port}"  # 查找该端口信息

    result = os.popen(cmd_find_pid).read()
    if str(port) and 'LISTENING' in result:
        i = result.index('LISTENING')
        start = i + len('LISTENING') + 7
        end = result.index('\n')
        pid = result[start:end]

        cmd_kill = f'taskkill -f -pid {pid}'  # 释放该端口
        os.popen(cmd_kill)
    else:
        logging.info(f"端口:{port}可以被使用！")

def appium_desired(host, port):
    with open('../config/91lng_caps.yaml','r',encoding='utf-8') as file:
        data = yaml.load(file)
    appPackage = "com.haixue.app.android.HaixueAcademy.h4"

    desired_caps = {}
    desired_caps['platformName'] = data['platformName']
    desired_caps['platformVersion'] = data['platformVersion']
    desired_caps['deviceName'] = data['deviceName']

    base_dir = os.path.dirname(os.path.dirname(__file__))
    app_path = os.path.join(base_dir, 'app', data['appname'])
    desired_caps['app'] = app_path

    desired_caps['appPackage'] = data['appPackage']
    desired_caps['appActivity'] = data['appActivity']
    desired_caps['noReset'] = data['noReset']
    #desired_caps['udid'] = data['udid']

    desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
    desired_caps['resetKeyboard'] = data['resetKeyboard']
    desired_caps['automationName'] = 'uiautomator2'

    logging.info('====start app====')
    driver=webdriver.Remote('http://'+str(host)+':'+str(port)+'/wd/hub',desired_caps)
    driver.implicitly_wait(8)
    return driver

pc = input('请输入系统 win or mac：')
def stop_appium(post_num=4723):
    '''关闭appium服务'''
    if pc.upper() =='WIN':
        p = os.popen(f'netstat  -aon|findstr {post_num}')
        p0 = p.read().strip()
        if p0 != '' and 'LISTENING' in p0:
            p1 = int(p0.split('LISTENING')[1].strip()[0:4])  # 获取进程号
            os.popen(f'taskkill /F /PID {p1}')  # 结束进程
            print('appium server已结束')
    elif pc.upper() == 'MAC':
        p = os.popen(f'lsof -i tcp:{post_num}')
        p0 = p.read()
        if p0.strip() != '':
            p1 = int(p0.split('\n')[1].split()[1])  # 获取进程号
            os.popen(f'kill {p1}')  # 结束进程
            print('appium server已结束')

def start_appium(post_num=4723):
    '''开启appium服务'''
    stop_appium(post_num)    # 先判断端口是否被占用，如果被占用则关闭该端口号
    # 根据系统，启动对应的服务
    cmd_dict = {
        'WIN':f' start /b appium -a 127.0.0.1 -p {post_num} --log xxx.log --local-timezone ',
        'MAC':f'appium -a 127.0.0.1 -p {post_num} --log xxx.log --local-timezone  & '
    }
    os.system(cmd_dict[pc.upper()])
    time.sleep(3)  # 等待启动完成
    print('appium启动成功')


if __name__ == "__main__":
    start_server = StartAppiumServer().appium_start("127.0.0.1", 4723)

{
 "platformName": "OPPO R11",
 "platformVersion":"4.4.2",
 "deviceName": "127.0.0.1:62001 device",
 "appPackage": "com.haixue.app.android.HaixueAcademy.h4",
 "appActivity": "com.haixue.academy.me.LoginActivity"
}