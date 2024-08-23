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
# 优化（第四版）

import ctypes
import sys
import time

import psutil
import pyautogui
import win32api
import win32gui
import win32process
from win32con import WM_INPUTLANGCHANGEREQUEST

# 此py给nvim-qt.exe切换输入法用，
# emacs.exe也有一个输入法切换，
# 当nvim-qt.exe切换到emacs.exe时，不再切换
exclude_exes = ["emacs.exe"]


def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name().strip()
    except:
        return 'xx'


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
    time.sleep(0.01)
    if active_window_process_name() not in exclude_exes:
        check_input_method()
except Exception as e:
    print("change_language - Exception:", e)
