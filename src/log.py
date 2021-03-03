"""
Author: Sweegi

Logging

"""
import io
import os
import sys

import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = './logs'

def getLogger(level='INFO'):
    logger = logging.getLogger()

    fmt = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if not os.path.isdir(LOG_DIR): os.mkdir('./logs')

    log_file = os.path.join(LOG_DIR, 'record.log')
    file_handler = TimedRotatingFileHandler(log_file, encoding='utf-8', when='midnight')
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    stream_handler = StreamHandler()
    _fmt = logging.Formatter('%(message)s')
    stream_handler.setFormatter(_fmt)
    logger.addHandler(stream_handler)

    logger.setLevel(getattr(logging, level))

    return logger

logger = getLogger()

