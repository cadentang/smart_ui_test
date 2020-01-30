# -*- coding: utf-8 -*-
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from utils.base_path import *

class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        logging.root.setLevel(logging.NOTSET)
        self.log_path = os.path.join(BASE_LOG_PATH, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(self.log_path):
            print(self.log_path)
            os.mkdir(self.log_path)
        self.console_level = "WARNING"
        self.file_level = "DEBUG"
        self.log_file_name = "test.log"
        self.backup_count = 5
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """获取日志对象 """
        if not self.logger.handlers:
            # 控制台输出配置
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_level)
            self.logger.addHandler(console_handler)

            # 文件输出配置
            file_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_path, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()

