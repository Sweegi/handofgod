"""
Author: Sweegi

"""
import os
import sys
import json
import time
import logging
import traceback
from threading import Thread
from functools import partial

import screen
import ocr
import mouse
from log import logger

_CONF_FILE = "./ro.conf"

# 读取任务配置文件
def loadconf():
    _conf_data = {}

    with open(_CONF_FILE, 'r', encoding='utf-8') as _f:
        _conf_data = json.load(_f)

    return _conf_data

def start():
    logger.info('***  启动程序! 请根据提示操作! ***\n')
    try:
        conf = loadconf()
        _wait()

        win = {}
        # multi-process
        title = 'RO'
        repeat = conf.get('repeat')
        window_name = conf.get('window_name')

        _func(window_name, title, repeat)
    finally:
        _enter_line()
        logger.info('*** Over! ***')
        _wait(2)
        sys.exit(0)

def _func(window_name, title, repeat):
    try:
        # 游戏窗口
        _current_win = None
        
        logger.info('- Step 1 - 选择当前 [%s] 窗口, 请输入 y or n :\n' % title)
        winlist = screen.enum_windows(window_name)
        for w in winlist:
            k = input('   窗口名: %s > ' % w.get('title'))
            if k.lower() != 'y': continue

            _current_win = screen.get_window(w)
            _enter_line()
            logger.info('窗口选择成功!\n')
            _wait()
            break

        if not _current_win: return

        logger.info('- Step 2 - 使用鼠标选择监视区域 ... ')
        _wait()

        screen.set_window_to_top(_current_win)

        sc = screen.CTkPrScrn() # absolute position for window

        logger.info('- Step 3 - 开始扫描 ... ')
        while True:
            # _img, _img_black = screen.capture(_current_win, sc.start_x, sc.start_y, sc.end_x, sc.end_y)
            screen.capture(_current_win, sc.start_x, sc.start_y, sc.width, sc.height)

            for _, _conf in repeat.items():
                try:
                    _txt = _conf.get('text')
                    if _txt:
                        assert ocr.recognize_text(_img, _txt)

                    '''
                    _color = _conf.get('color')
                    if _color:
                        assert ocr.recognize_color(_img, _color)
                    '''

                    _target, _action = _conf.get('action').split(':')
                    if _target == 'mouse':
                        getattr(mouse, _action)()
                        logger.info('%s %s' % (_action, _))
                    else:
                        logger.info('No Support for Action: %s' % _conf.get('action'))
                except AssertionError as e:
                    continue
            _wait()
    except Exception as e:
        logger.error('[Error] ', traceback.format_exc())

def _enter_line():
    print(' ')

def _wait(sec=0.3):
    time.sleep(sec)

def _start_thread(func, args, deamon=True):
    t = Thread(target=func, args=args)
    t.setDeamon(deamon)
    t.start()

if __name__ == '__main__':
     start()