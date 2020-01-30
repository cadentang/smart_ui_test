# -*- coding: utf-8 -*-
from xml.dom.minidom import Document

from utils.operation_cmd import RunCmd
from utils.get_log import logger
from utils.base_path import PROJECT_ROOT_DIR
from utils.get_parser import get_arg


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

def build_environment_file(file_path, environment_list):
    """
    向指定的目录创建allure环境信息，创建的文件为xml文件
    :param file_name: 文件名称
    :param file_path: 文件路径
    :param kwargs: 环境信息key和value
    :return:
    """
    doc = Document()
    root = doc.createElement('environment')
    doc.appendChild(root)

    for i in environment_list:
        node_parameter = doc.createElement('parameter')
        node_key = doc.createElement('key')
        node_value = doc.createElement('value')

        for k,v in i.items():
            node_key.appendChild(doc.createTextNode(str(k)))
            node_value.appendChild(doc.createTextNode(str(v)))

        node_parameter.appendChild(node_key)
        node_parameter.appendChild(node_value)
        root.appendChild(node_parameter)

    file_name = "environment.xml"
    file = file_path + "/" +  file_name
    with open(file, 'w') as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

def get_environment_list():
    """得到环境参数并将其转化为所需的list类型"""
    environment_list = []
    for k, v in get_arg().items():
        d = {}
        d[k] = v
        environment_list.append(d)
    return environment_list

# if __name__ == "__main__":
#     managerList = [{'name': 'joy'},
#                    {'name': 'tom'},
#                    {'name': 'ruby'}]
#     qq = get_arg()
#     print(qq)
#     print(get_environment_list())
#     build_environment_file(PROJECT_ROOT_DIR, get_environment_list())
    # dict = {"key": "12", "value": "34"}
    # for key, value in zip(dict.keys(), dict.values()):
    #     print(key)
    #     print(value)