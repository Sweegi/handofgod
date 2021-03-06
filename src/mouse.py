"""
Author Sweegi

鼠标事件

"""
import win32api, win32con

def getClickLocation(location):
    start_x, start_y, end_x, end_y = location

    x = (end_x - start_x) / 2 + start_x
    y = (start_y - end_y) / 2 + end_y

    return int(x), int(y)

# 单击
def click(x, y):
    # move to 
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)