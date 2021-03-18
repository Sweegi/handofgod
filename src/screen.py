"""
Author: Sweegi
"""
import time

import tkinter
import ctypes
import win32api, win32gui, win32con, win32ui

from PIL import Image, ImageGrab

# 选择窗户，用户交互
def enum_windows(name):
    _enumWindows = []
    win32gui.EnumWindows(lambda _w, param: param.append(_w), _enumWindows)

    winlist = []
    for _win_id in _enumWindows:
        _win_txt = win32gui.GetWindowText(_win_id)
        if not _win_txt: continue

        _win_clsname = win32gui.GetClassName(_win_id)
        if name and _win_txt.find(name) < 0: continue

        winlist.append({'id': _win_id, 'title': _win_txt, 'clsname': _win_clsname})

    return  winlist

def get_window(win_dict):
    return win32gui.FindWindow(win_dict.get('clsname'), win_dict.get('title'))

# 激活显示窗口，使其成为置顶活动窗口
def set_window_to_top(win_obj):
    win32gui.SetForegroundWindow(win_obj)  #show window

# 窗口识别区域捕获 
def capture(win_obj, bbox):
    # 置顶窗口
    set_window_to_top(win_obj)
    # 窗口大小
    r = win32gui.GetWindowRect(win_obj)
    left, top, right, bot = r

    pic = ImageGrab.grab(bbox=bbox)
    # pic.save('./images/orginal.jpg', quality=95, subsampling=0)

    return pic

class CTkPrScrn:
    def __init__(self, startX=0, startY=0):
        self.__start_x = startX
        self.__start_y = startY
        self.__scale = 1

        self.__end_x = None
        self.__end_y = None

        self.__win = tkinter.Tk()
        self.__win.attributes("-alpha", 0.5)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层

        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.__win, width=self.__width, height=self.__height, bg="gray")

        self.__win.bind('<Button-1>', self.click)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.click_release)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.move)  # 绑定鼠标左键点击移动事件
        self.__win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale

        self.__win.mainloop()  # 窗口持久化

        print(self.__width, self.__height, widthScale, heightScale, width, height, self.__scale)

    def click(self, event): # 鼠标左键按下
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        self.__start_x, self.__start_y = event.x, event.y

    def click_release(self, event): # 鼠标左键释放
        if event.x == self.__start_x or event.y == self.__start_y:
            return

        self.__end_x, self.__end_y = event.x, event.y
        print('x:', event.x, ', y:', event.y)
        # im = ImageGrab.grab((self.__scale * self.__start_x, self.__scale * self.__start_y,
                                # self.__scale * event.x, self.__scale * event.y))
        # imgName = 'tmp.png'
        # im.save(imgName)

        print('获取成功!')
        self.__win.update()
        time.sleep(0.5)
        self.__win.destroy()

    def move(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='white', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

    @property
    def start_x(self):
        return self.__scale * self.__start_x

    @property
    def start_y(self):
        return self.__scale * self.__start_y

    @property
    def end_x(self):
        return self.__scale * self.__end_x

    @property
    def end_y(self):
        return self.__scale * self.__end_y

    @property
    def width(self):
        return self.__scale * self.__width

    @property
    def height(self):
        return self.__scale * self.__height

# def window_capture(win):

#     print(win)
#     # wind = win32gui.FindWindow(win.get('id'), None)
#     win_id = win.get('id')

#     # 窗口大小
#     r = win32gui.GetWindowRect(win_id)
#     print(r)
#     left, top, right, bot = r

#     width = right - left
#     height = bot - top
#     print(width, height)

#     # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
#     hwin = win32gui.GetWindowDC(win_id)

#     # 图片最左边距离主屏左上角的水平距离
#     left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
#     # 图片最上边距离主屏左上角的垂直距离
#     top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

#     srcdc = win32ui.CreateDCFromHandle(hwin)
#     memdc = srcdc.CreateCompatibleDC()

#     bmp = win32ui.CreateBitmap()
#     bmp.CreateCompatibleBitmap(srcdc, r[2] - r[0], r[3] - r[1])

#     memdc.SelectObject(bmp)
#     memdc.BitBlt((-r[0], top - r[1]), (r[2], r[3] - top), srcdc, (left, top), win32con.SRCCOPY)

#     bmpFileName = 'screenshot.bmp'
#     bmp.SaveBitmapFile(memdc, bmpFileName)

#     memdc.DeleteDC()
#     srcdc.DeleteDC()

if __name__ == '__main__':
    img = Image.open("E://handofgod/src/orginal.jpg")
    print(type(img))

    # win_dict = {'id': 12518504, 'title': 'E:\\handofgod\\src\\images\\1.png - Internet Explorer', 'clsname': 'IEFrame'}
    # win_dict = {'id': 656514, 'title': 'New tab - Personal - Microsoft\u200b Edge', 'clsname': 'Chrome_WidgetWin_1'}
    # win_obj = get_window(win_dict)
    # capture(win_obj, 769.0, 498.0, 1674.0, 1222.0)
    # set_window_to_top(win_obj)
    # capture(win_obj, 83, 64, 1112, 735)
    # window_capture(win_dict)
