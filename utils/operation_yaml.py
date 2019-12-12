# -*- coding: utf-8 -*-
import os
from ruamel import yaml


class YamlReadAndWrite:
    """对yaml文件的操作"""
    def __init__(self, yaml_file_path):
        if os.path.exists(yaml_file_path):
            self.yaml_file_path = yaml_file_path
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def read_yaml_data(self):
        if not self._data:
            with open(self.yaml_file_path, 'r', encoding="utf-8") as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data

    def write_yaml_data(self, add_data):
        """写入数据"""
        with open(self.yaml_file_path, "a", encoding="utf-8") as f:
            yaml.load(f, Loader=yaml.RoundTripLoader)
            yaml.dump(add_data, f)

    def update_yaml_data(self, update_data):
        """更新数据"""
        with open(self.yaml_file_path, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.RoundTripLoader)
            data['service']['memo_query']['server_ip'][0] = 'mysql_host={}'.format(update_data)



