import ctypes
import time

print("""5秒后本程序会开始运行，
请迅速将本程序置于后台，
然后到文本编辑器之类的软件的输入框切换输入法到需要的状态
    """)
time.sleep(5)

user32 = ctypes.WinDLL("user32", use_last_error=True)
curr_window = user32.GetForegroundWindow()
thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
klid = user32.GetKeyboardLayout(thread_id)
lid = klid & (2**16 - 1)
lid_hex = hex(lid)

print(lid_hex)
if lid_hex == "0x409":
    print("当前的输入法状态是英文输入模式\n\n")
elif lid_hex == "0x804":
    print("当前的输入法是中文输入模式\n\n")
else:
    print("当前的输入法既不是英文输入也不是中文输入\n\n")

input("请按回车键结束")
