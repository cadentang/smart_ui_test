# # -*- coding: utf-8 -*-
import os
import time
import pytest
import allure
from api.exam.com import pc_login


@pytest.fixture(scope="session", autouse=True)
def go_to_api_login():
    """登录"""
    result = pc_login()
    yield result





