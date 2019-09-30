# -*- coding:utf8 -*-
# Time    : 2019/9/17 10:52
# Author  : Richard
# Email   : tangtao556@qq.com
# File    : log.__init__.py
import json
import logging
import logging.config
import os


class Log:
    def __init__(self, logger_name=__name__, logging_level=logging.DEBUG, conf=None):
        self.logger_name = logger_name
        self.logging_level = logging_level
        self.config = conf or os.path.join(os.path.dirname(os.path.abspath(__file__)), "log4p.json")
        self.logger = self.create()

    def create(self):
        # Create a logger
        agent_logger = logging.getLogger(self.logger_name)
        agent_logger.setLevel(self.logging_level)
        with open(self.config, 'r') as logging_configuration_file:
            config_dict = json.load(logging_configuration_file)
            for k, v in config_dict.get('handlers').items():
                if v.get('filename'):
                    v['filename'] = os.path.join(os.path.dirname(self.config), v['filename'])
        logging.config.dictConfig(config_dict)
        return agent_logger


log = Log().logger
