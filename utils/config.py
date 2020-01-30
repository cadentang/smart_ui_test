# -*- coding: utf-8 -*-
from utils.operation_yaml import YamlReadAndWrite
from utils.get_parser import get_arg
from utils.base_path import BASE_CONFIG_PATH
from utils.get_log import logger


class ReadConfig:
    """ 获取基础配置文件信息"""

    def __init__(self, run_arg=None):
        """
        :param run_arg:命令行运行参数
            {
                'env': 'reg',
                'project': 'main_station',
                'user_port': 'pc',
                'pattern': 'local',
                'browser': '79'
            }
        """
        base_yaml = YamlReadAndWrite(BASE_CONFIG_PATH)
        self.base_config = base_yaml.read_yaml_data
        if isinstance(run_arg, dict) or run_arg == None:
            self.run_arg = run_arg
        else:
            logger.error("run_arg参数类型错误，必须为dict")
            raise ValueError("run_arg参数类型错误，必须为dict")

    def get_config(self):
        """
        获取用例运行时配置相关，返回配置字典
        """
        config_dict = {}
        if self.run_arg != None:
            config_dict["env"] = self.run_arg["env"]
            config_dict["user_port"] = self.run_arg["user_port"]
            config_dict["pattern"] = self.run_arg["pattern"]
            config_dict["project_list"] = self.run_arg["project"]
            config_dict["browser"] = self.run_arg["browser"]
            config_dict["version"] = self.run_arg["version"]

            for item in self.base_config[0]["base_config"]:
                if self.run_arg["env"] == item:
                    config_dict["env_config"] = self.base_config[0]["base_config"][item]

            for item in self.base_config[0]["run_config"]:
                if item == "log":
                    config_dict["log"] = self.base_config[0]["run_config"][item]
                if item == "time_out":
                    config_dict["time_out"] = self.base_config[0]["run_config"][item][0]
                if item == "service":
                    config_dict["service"] = self.base_config[0]["run_config"][item]
        else:

            config_dict["base_config"] = self.base_config[0]["base_config"]

        logger.info(f"用例运行配置字典config_dict: {config_dict}")

        return config_dict



