"""
Author: Sweegi
"""
import win32api, win32gui, win32con, win32ui
from PIL import Image

import ocr

# 选择窗户，与用户交互
def enum_windows(name):
    winlist = []
    win32gui.EnumWindows(lambda _w, param: param.append(_w), winlist)

    windlist = []
    for _win_id in winlist:
        _win_txt = win32gui.GetWindowText(_win_id)
        _win_clsname = win32gui.GetClassName(_win_id)
        if _win_txt.find(name) < 0: continue

        windlist.append({'id': _win_id, 'title': _win_txt, 'clsname': _win_clsname})

    return  windlist

# 窗口截图
def window_capture(win):

    print(win)
    # wind = win32gui.FindWindow(win.get('id'), None)
    win_id = win.get('id')

    # 窗口大小
    r = win32gui.GetWindowRect(win_id)
    print(r)
    left, top, right, bot = r

    width = right - left
    height = bot - top
    print(width, height)

    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwin = win32gui.GetWindowDC(win_id)

    # 图片最左边距离主屏左上角的水平距离
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    # 图片最上边距离主屏左上角的垂直距离
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    srcdc = win32ui.CreateDCFromHandle(hwin)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, r[2] - r[0], r[3] - r[1])
    memdc.SelectObject(bmp)
    memdc.BitBlt((-r[0], top - r[1]), (r[2], r[3] - top), srcdc, (left, top), win32con.SRCCOPY)

    bmpFileName = 'screenshot.bmp'
    bmp.SaveBitmapFile(memdc, bmpFileName)

    # im = Image.open(bmpFileName)
    # im = im.convert('RGB')

    # jpgFileName = 'screenshot.jpg'
    # im.save(jpgFileName)

    # return

# 选择截图中需要识别的区域
def select_area():
    return

# 图片二值化
def point(filename):
    img = Image.open(filename)
    print(type(img))

    img = img.convert('L')

    threshold = 200

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    photo = img.point(table, '1')
    # _photo = photo.save('t3.jpg', format="jpeg")
    print(type(photo))

    return photo

if __name__ == '__main__':
    # filename = "E://handofgod/src/images/1.png"

    # _img = point(filename)
    # ocr.recognize_text(_img)

    l = enum_windows('Microsoft​ Edge')
    for i in l:
        window_capture(i)