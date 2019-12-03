# -*- coding: utf-8 -*-
__author__ = 'caden'
"""
description:对MySQL数据库相关操作
"""
import pymysql
import xlwt

from utils.config import read_config


class Mysql:

    def __init__(self):
        env = read_config.get_run_config()["envrinment"]
        database_config = read_config.get_base_config(env)["mysql_3306"]
        self.host = database_config["ip_or_domain"]
        self.port = database_config["port"]
        self.username = database_config["user"]
        self.password = database_config["password"]
        self.database = "highso"

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

    def connectDB(self):
        """
        连接数据库
        """
        try:
            self.db_connect = pymysql.connect(**self.config)
            # 创建游标
            self.cursor = self.db_connect.cursor()
            print("数据库连接成功!")
        except ConnectionError as ex:
            print(str(ex))

    def executeSQL(self, sql_):
        """
        执行sql
        """
        self.connectDB()
        self.cursor.execute(sql_)
        value = self.cursor.fetchall()
        self.db_connect.commit()
        return value

    def get_all(self, cursor):
        """
        得到所有执行sql后的结果
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        得到一条sql语句执行结果
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        关闭数据库连接
        :return:
        """
        self.db_connect.close()
        print("关闭数据库成功！")

    def export(self, sql_):
        # 查询的结果导出到Excel中
        results = self.executeSQL(sql_)
        self.cursor.scroll(0, mode='absolute')
        filename = '123.xls'  # 定义Excel名字

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


