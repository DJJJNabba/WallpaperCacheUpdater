"""
utils.py

Contains utility functions such as adding the application to system startup.
For Windows, this can be done by creating a registry entry or placing a shortcut
in the startup folder.
"""

import os
import sys
import shutil
import winreg

def add_to_startup():
    """
    Adds the application to the Windows startup.
    This implementation creates a registry entry under HKCU\Software\Microsoft\Windows\CurrentVersion\Run.
    """
    exe_path = sys.executable  # Path to the Python interpreter or your compiled exe
    script_path = os.path.abspath(__file__)
    # If you have compiled to an exe with tools like PyInstaller, use that path instead.
    run_command = f'"{exe_path}" "{script_path}"'
    

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WallpaperCacheUpdater", 0, winreg.REG_SZ, run_command)
    winreg.CloseKey(key)