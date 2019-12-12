# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils.operation_cmd import RunCmd
from utils.get_log import logger


def get(url, headers=None, params=None, timeout=10):

    try:
        resposnse = requests.get(url, headers=headers, params=params, timeout=float(timeout))
        return resposnse.text
    except TimeoutError:
        logger.error("Time out!")


def post(url, headers=None, params=None, data=None, timeout=10):

    try:
        response = requests.post(url, headers=headers,params=params, data=data, timeout=float(timeout))
        return response
    except TimeoutError:
        logger.error("Time out!")


# print(get("http://39.107.127.90:9999/grid/console?config=true&configDebug=true#"))
html = get("http://39.107.127.90:9999/grid/console?config=true&configDebug=true#")
soup = BeautifulSoup(html,'lxml')
config = soup.find_all(attrs={'class': 'content_detail'})
print(config)