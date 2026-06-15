from pywinauto import Desktop
import win32gui

while True:
    hwnd = win32gui.GetForegroundWindow()
    window = Desktop(backend="uia").window(handle=hwnd)

    window.print_control_identifiers(depth=5)