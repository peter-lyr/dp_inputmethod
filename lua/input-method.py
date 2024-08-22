import sys

import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST

LANG = {"ZH": 0x0804, "EN": 0x0409}
try:
    hwnd = win32gui.GetForegroundWindow()
    win32api.PostMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, None, LANG[sys.argv[1]])
except Exception as e:
    print("change_language - Exception:", e)
