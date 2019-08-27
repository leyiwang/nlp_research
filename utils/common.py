#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  common function
  Author: wangleyi
  Email: leyiwang.cn@gmail.com
  File:  common.py
  Date: 2019-04-16 13:37
"""
import configparser
import os
import time

import pandas as pd
from fake_useragent import UserAgent

from utils.log import logger

get_abs_path = lambda x: os.path.normpath(os.path.join(os.path.dirname(__file__), x))


class Utils(object):
    UA = UserAgent(verify_ssl=False)
    CONFIG = configparser.ConfigParser()
    CONFIG.read(get_abs_path('../conf/conf.ini'))

    @staticmethod
    def xlsx_writer(save_dir, fname, data, header=None):
        save_path = os.path.join(save_dir, fname)
        logger.info("{} papers matched!".format(len(data)))
        if len(data) == 0:
            return
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        df = pd.DataFrame(data=data, dtype=str)
        df.to_excel(save_path, float_format=None, header=header, index=False)

    @staticmethod
    def get_current_date():
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))
