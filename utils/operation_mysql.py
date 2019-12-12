# -*- coding: utf-8 -*-
import pymysql
import xlwt
from utils.global_variable import get_value
from utils.get_log import logger


class Mysql:
    """数据库操作封装"""
    def __init__(self, mysql_port, database):
        database_config = get_value("config_dict")[mysql_port]
        self.host = database_config["ip_or_domain"]
        self.port = database_config["port"]
        self.username = database_config["user"]
        self.password = database_config["password"]
        self.database = database

        # 数据库连接配置
        self.config = {
            'host': str(self.host),
            'user': self.username,
            'password': self.password,
            'port': int(self.port),
            'db': self.database
        }

        self.db_connect = None
        self.cursor = None

    def connect_db(self):
        """连接数据库"""
        try:
            self.db_connect = pymysql.connect(**self.config)
            # 创建游标
            self.cursor = self.db_connect.cursor()
            logger.info(f"数据库连接成功，配置信息：{self.config}")
        except ConnectionError as e:
            logger.error(f"数据库连接失败，失败信息：{str(e)}")

    def execute_sql(self, sql):
        """执行sql"""
        self.connec_db()
        self.cursor.execute(sql)
        value = self.cursor.fetchall()
        self.db_connect.commit()
        return value

    def get_all(self, cursor):
        """得到所有执行sql后的结果"""
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """得到一条sql语句执行结果"""
        value = cursor.fetchone()
        return value

    def close_db(self):
        """关闭数据库连接"""
        self.db_connect.close()

    def export(self, sql, filename):
        """查询的结果导出到Excel中"""
        results = self.execute_sql(sql)
        self.cursor.scroll(0, mode='absolute')

        # 获取MYSQL里面的数据字段名称
        fields = self.cursor.description
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('table', cell_overwrite_ok=True)

        # 在Excel中写入MySQL列字段信息
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])
        workbook.save(filename)


