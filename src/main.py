"""
Author: Sweegi

"""
import os
import sys
import json
import time
import logging
from threading import Thread
from functools import partial

import screen
import ocr
import mouse
from log import logger

_CONF_FILE = "./task.conf"

# 读取任务配置文件
def loadconf():
    _conf_data = {}

    with open(_CONF_FILE, 'r', encoding='utf-8') as _f:
        _conf_data = json.load(_f)

    return _conf_data

def start():
    logger.info('*** 程序启动，请根据提示操作 ***\n')
    try:
        conf = loadconf()
        _wait()

        win = {}
        for game, task in conf.items():
            print('请确认%s监控窗口' % game)
            for w in screen.select_window():
                k = input('%s > (y or n): ' % w)
                if k.lower() != 'y': continue

                win[game] = w
                logger.warning('%s 已选择窗口: %s' % (game, w))
                break

        logger.debug('开始识别 ... ')
        while True:
            for game, task in conf.items():
                win_id = win.get(game)
                _img = screen.window_shot(win_id)

                for _, _conf in task.items():
                    try:
                        _txt = _conf.get('text')
                        if _txt:
                            assert ocr.recognize_text(_img, _txt)

                        _color = _conf.get('color')
                        if _color:
                            assert ocr.recognize_color(_img, _color)

                        _target, _action = _conf.get('action').split(':')
                        if _target == 'mouse':
                            getattr(mouse, _action)()
                            logger.info('%s %s' % (_action, _txt))
                        else:
                            logger.info('不支持的action: %s' % _conf.get('action'))
                    except AssertionError as e:
                        continue
            _wait()

    finally:
        logger.info('*** 程序结束 ***')
        _wait(2)
        sys.exit(0)

def _wait(sec=0.5):
    time.sleep(sec)

def _start_thread(func, args, deamon=True):
    t = Thread(target=func, args=args)
    t.setDeamon(deamon)
    t.start()

if __name__ == '__main__':
    start()
