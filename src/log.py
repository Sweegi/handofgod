"""
Author: Sweegi

Logging

"""
import os

import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = './logs'

def getLogger(level='INFO'):
    logger = logging.getLogger()

    fmt = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if not os.path.isdir(LOG_DIR): os.mkdir('./logs')

    file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, 'record.log'), when='midnight')
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    logger.setLevel(getattr(logging, level))

    return logger

logger = getLogger()

