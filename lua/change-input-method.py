# # 第一版输入法切换，并不可靠
# # 在nvim-qt里，点击桌面时
# # 本来切换到搜狗输入法，但是并没有
# # 240823-13h49m
#
# import sys
#
# import win32api
# import win32gui
# from win32con import WM_INPUTLANGCHANGEREQUEST
#
# LANG = {"ZH": 0x0804, "EN": 0x0409}
# try:
#     hwnd = win32gui.GetForegroundWindow()
#     win32api.PostMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, None, LANG[sys.argv[1]])
# except Exception as e:
#     print("change_language - Exception:", e)


# # 第二版
# # 240823-13h49m
# # 测试解决第一版的问题
# # 按按键Win+Space切换输入法
# # 240823-13h55m
# # 存在误触情况
# import sys
# import ctypes
# import pyautogui
#
# user32 = ctypes.WinDLL("user32", use_last_error=True)
# curr_window = user32.GetForegroundWindow()
# thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
# klid = user32.GetKeyboardLayout(thread_id)
# lid = klid & (2**16 - 1)
# lid_hex = hex(lid)
#
# if lid_hex == "0x409": # en
#     if sys.argv[1] == 'ZH':
#         pyautogui.hotkey('win', 'space')
# elif lid_hex == "0x804": # zh
#     if sys.argv[1] == 'EN':
#         pyautogui.hotkey('win', 'space')


# 第三版
# 结合第一二版
# 解决第二版的问题
# 240823-14h03m
# 存在问题：
# 不能在多个地方去跑

import ctypes
import sys
import time

import pyautogui
import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST


def check_input_method():
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)
    if lid_hex == "0x409":  # en
        if sys.argv[1] == "ZH":
            pyautogui.hotkey("win", "space")
    elif lid_hex == "0x804":  # zh
        if sys.argv[1] == "EN":
            pyautogui.hotkey("win", "space")


LANG = {"ZH": 0x0804, "EN": 0x0409}
try:
    hwnd = win32gui.GetForegroundWindow()
    win32api.PostMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, None, LANG[sys.argv[1]])
    time.sleep(0.1)
    check_input_method()
except Exception as e:
    print("change_language - Exception:", e)
