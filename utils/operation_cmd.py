# -*- coding: utf-8 -*-
import subprocess


class RunCmd:
    @staticmethod
    def run_cmd(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        result = output.decode("utf-8")
        return result



