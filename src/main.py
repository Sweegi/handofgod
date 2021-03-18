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

        win = {}
        # multi-process
        window_name = conf.get('window_name')
        print(conf)

        _func(window_name, conf)
    finally:
        _enter_line()
        logger.info('*** Over! ***')
        _wait(2)
        sys.exit(0)

def _func(window_name, conf):
    try:
        # 游戏窗口
        _current_win = None
        
        logger.info('- Step 1 - 选择当前游戏窗口, 请输入 y or n :\n')
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

        logger.info('- Step 3 - 开始扫描 ( 第一次识别比较耗时，请不要切换游戏视角或调整游戏窗口 ) ... ')

        # 图片二值化步长初始值
        start_threshold = 200
        end_threshold = 240

        # 初次识别标志位
        first_flag = True 

        # 点击位置
        _x, _y = mouse.getClickLocation(sc.start_x, sc.start_y, sc.end_x, sc.end_y)

        while True:
            logger.info('wait 抛竿...')
            _img = screen.capture(_current_win, sc.start_x, sc.start_y, sc.end_x, sc.end_y)
            _img.save('./images/pg1.jpg')

            logger.info('recognizing start ...')
            s_res = ocr.recognize_text(_img, '抛竿', start_threshold)
            logger.info('recognizing end ...')
            if s_res is not None:
                # mouse.click(_x, _y)
                logger.info('click 抛竿 x: %d, y: %d' % (_x, _y))
                if first_flag:
                    _img.save('./images/pg.jpg')
                    # 更新抛竿二值化步长
                    start_threshold = s_res
                    logger.info('start threshold: %d' % s_res)

                # 记录次数，超出2分钟，约1200次，跳出循环
                # _times = 0
                # logger.info('wait 提竿...')
                # while _times < 1200:
                #     _times += 1

                #     _img2 = screen.capture(_current_win, sc.start_x, sc.start_y, sc.end_x, sc.end_y)

                #     _check_color = ocr.recognize_color(_img2, "152-179,188-231,95-128")
                #     if _check_color == False:
                #         _wait(0.1)
                #         continue

                #     e_res = ocr.recognize_text(_img2, '提竿', end_threshold)
                #     if e_res is not None:
                #         if first_flag:
                #             _img2.save('./images/tg.jpg')
                #             end_threshold = e_res
                #             first_flag = False
                #             logger.info('end threshold: %d' % e_res)
                #             logger.info('- Step 4 - 扫描完毕')

                #         else:
                #             # 单击
                #             mouse.click(_x, _y)
                #             logger.info('click 提竿 x: %d, y: %d' % (e_res, _x, _y))

                #         break

                # if first_flag:
                #     logger.info('- Step 4 - 扫描失败，请重试')
                #     break

            _wait(0.2)

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