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
    logger.info('*** Programming Start! Please follow the hint! ***\n')
    try:
        conf = loadconf()
        _wait()

        win = {}
        for game, task in conf.items():
            print('- Step 1 - Select the current [%s] window' % game)
            for w in screen.select_window():
                k = input('%s > (input y or n): ' % w)
                if k.lower() != 'y': continue

                win[game] = w
                _wait()
                _enter_line()
                logger.info('[%s] selected: %s\n' % (game, w))
                break

        _wait()
        logger.debug('- Step 2 - Begin to scanning ... ')
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
                            logger.info('%s %s' % (_action, _))
                        else:
                            logger.info('No Support for Action: %s' % _conf.get('action'))
                    except AssertionError as e:
                        continue
            _wait()

    finally:
        _enter_line()
        logger.info('*** Over! ***')
        _wait(2)
        sys.exit(0)

def _enter_line():
    print(' ')

def _wait(sec=0.5):
    time.sleep(sec)

def _start_thread(func, args, deamon=True):
    t = Thread(target=func, args=args)
    t.setDeamon(deamon)
    t.start()

if __name__ == '__main__':
     start()