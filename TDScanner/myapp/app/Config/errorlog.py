#!/opt/python27/bin/python
#coding:utf-8

import logging
from logging.handlers import TimedRotatingFileHandler as TimeHandler

def logger(log_name, log_path, log_level = logging.DEBUG):
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    file_handler = TimeHandler(log_path, 'W0')
    formatter = logging.Formatter("时间：%(asctime)s 文件：%(name)s 行数：%(lineno)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
    
