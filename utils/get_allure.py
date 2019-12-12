# -*- coding: utf-8 -*-
from utils.operation_cmd import RunCmd
from utils.get_log import logger


def change_to_html(xml_report_path, html_report_path):
    """
    使用allure将xml报告生成为html报告
    :param xml_report_path: allure生成的报告原始路径
    :param html_report_path: 转化后生成的html报告的路径
    :return:
    """
    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
    try:
        RunCmd().run_cmd(cmd)
    except Exception as e:
        logger.error(f"报告转换失败,请手动转化，失败信息：{str(e)}")
