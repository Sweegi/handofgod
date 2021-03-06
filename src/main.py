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

import ocr
import mouse
import screen
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

        # multi-process
        window_name = conf.get('name')

        # 选择窗口
        logger.info('- Step 1 - 选择当前游戏窗口, 请输入 y or n :\n')
        win_obj = _select_window(window_name)
        if win_obj is None: return
        logger.info('窗口选择成功!\n')

        # 定位按钮位置
        logger.info('- Step 2 - 使用鼠标选择监视区域 ... ')
        screen.set_window_to_top(win_obj)
        sc = screen.CTkPrScrn() # absolute position for window

        # 主窗口的绝对定位 
        _location = (sc.start_x, sc.start_y, sc.end_x, sc.end_y)
        # TODO 窗口相对位置
        # 点击位置
        _click_x, _click_y = mouse.getClickLocation(_location)

        logger.info('- Step 3 - 开始扫描 ( 第一次识别比较耗时，请不要切换游戏视角或调整游戏窗口 ) ... ')

        # 获得抛竿&提竿图片二值化步长值 & 图片均值
        _pg, _tg = _prepare(win_obj, conf, _click_x, _click_y, _location)
        if _pg is None or _tg is None:
            logger.info('- Step 4 - 扫描失败，请重试')
            return

        logger.info('- Step 4 - 扫描完毕')

        conf['pg'].update(_pg)
        conf['tg'].update(_tg)

        logging.info(conf)
        _enter_line()
        logger.info('- Step 5 - 执行开始')
        _run(win_obj, conf, _click_x, _click_y, _location)

    except Exception as e:
        logger.error('[Error] ', traceback.format_exc())
    finally:
        _enter_line()
        logger.info('*** Over! ***')
        _wait(2)
        sys.exit(0)

def _select_window(window_name):
    # 游戏窗口
    _current_win = None

    winlist = screen.enum_windows(window_name)

    for w in winlist:
        k = input('   窗口名: %s > ' % w.get('title'))
        if k.lower() != 'y': continue

        _current_win = screen.get_window(w)
        _enter_line()
        _wait()
        break
    return _current_win

def _prepare(win, conf, click_x, click_y, location):
    # 图片二值化步长值
    pg = tg = None
   
    _pg = conf.get('pg')
    _tg = conf.get('tg')

    while True:
        logger.info('等待 %s...' % _pg['text'])
        _img = screen.capture(win, location)

        for i in range(_pg['threshold'], 256):
            if ocr.recognize_text(_img, _pg['text'], i):
                _r, _g, _b = ocr._rgb_mean_value(_img)
                pg = {
                    'threshold': i,
                    'r': _r,
                    'g': _g,
                    'b': _b
                }
                _img.save('./images/pg.jpg')
                #TODO sum
                logger.info('识别%s'% _pg['text'])
                mouse.click(click_x, click_y)
                break

        if pg is None: continue

        _times = 0
        while True:
            # 记录次数，超出 1分钟，约 600 次，跳出循环
            if _times > 100: break
            _times += 1

            _img2 = screen.capture(win, location)

            if ocr.recognize_color(_img2, _tg['color']) == False:
                _wait(0.1)
                continue

            logger.info('等待 %s...' % _tg['text'])
            _img2.save('./images/tg.jpg')
            for j in range(_tg['threshold'], 256):
                if ocr.recognize_text(_img2, _tg['text'], j):
                    _r, _g, _b = ocr._rgb_mean_value(_img2)
                    tg = {
                        'threshold': j,
                        'r': _r,
                        'g': _g,
                        'b': _b
                    }
                    logger.info('识别%s'%_tg['text'])
                    break

            if tg is not None: break

        if pg is not None and tg is not None: break

    return pg, tg

def _run(win, conf, click_x, click_y, location):
    pg = conf.get('pg')
    tg = conf.get('tg')
        
    pg_txt = pg.get('text')
    tg_txt = tg.get('text')
    tg_color = tg.get('color')

    while True:
        # logger.info('wait 抛竿...')
        _img = screen.capture(win, location)
        # 比较图片均值
        _r, _g, _b = ocr._rgb_mean_value(_img)
        if abs(pg['r']-_r) > 10 and abs(pg['g']-_g) > 10 and abs(pg['b']-_b) > 10:
            _wait(0.2)
            continue

        _start = time.time()
        res = ocr.recognize_text(_img, pg_txt, pg.get('threshold'))
        logger.info('costs %d sec ...' % int(time.time() - _start))

        if res == False:
            _wait(0.2)
            continue

        # 点击抛竿
        mouse.click(click_x, click_y)
        logger.info('click 抛竿 x: %d, y: %d' % (click_x, click_y))

        _times = 0
        logger.info('wait 提竿...')
        while True:
            # 记录次数，超出 1分钟，约 600 次，跳出循环
            if _times > 100: break
            _times += 1

            _img2 = screen.capture(win, location)

            # 比较图片均值
            _r, _g, _b = ocr._rgb_mean_value(_img2)
            if (ocr.recognize_color(_img2, tg_color) == False) or (abs(pg['r']-_r) > 20 and abs(pg['g']-_g) > 20 and abs(pg['b']-_b) > 20):
                _wait(0.1)
                continue

            _wait(0.2)
            mouse.click(click_x, click_y)
            logger.info('click 提竿 x: %d, y: %d' % (click_x, click_y))
            _wait(1)
            break
            '''
            if ocr.recognize_text(_img2, '提竿', tg.get('threshold')):
                mouse.click(click_x, click_y)
                logger.info('click 提竿 x: %d, y: %d' % (click_x, click_y))
                _wait(0.2)
                break
            '''

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