#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  log
  Author: wangleyi
  Email: leyiwang.cn@gmail.com
  File:  log.py
  Date: 2019-04-16 13:52
"""
import logging
import logging.handlers
from colorlog import ColoredFormatter


def init_log(name, level=logging.INFO,
             format="%(levelname)s %(asctime)s PID:%(process)d"
                    " %(filename)s:%(funcName)s:%(lineno)d: %(message)s",
             datefmt="%Y-%m-%d %H:%M:%S"):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    color_formatter = ColoredFormatter("%(log_color)s" + format, datefmt)

    stream_handle = logging.StreamHandler()
    stream_handle.setFormatter(color_formatter)
    logger.addHandler(stream_handle)
    return logger


logger = init_log("log")
