"""
utils.py

Creates a shortcut in the Windows Startup folder (`shell:startup`) to run the WallpaperCacheUpdater automatically.
Uses `pythonw.exe` for running Python scripts to prevent a console window from appearing.
"""

import os
import sys
import winshell
from win32com.client import Dispatch

def add_to_startup():
    """
    Adds the application to Windows startup by creating a shortcut in the Startup folder.
    """
    # Get the Startup folder path
    startup_folder = winshell.startup()

    # Define the shortcut path
    shortcut_path = os.path.join(startup_folder, "WallpaperCacheUpdater.lnk")

    # Get paths
    script_path = os.path.abspath("main.py")  # Ensure main.py is used
    exe_path = sys.executable  # Path to Python interpreter (or compiled .exe)

    # If running as a Python script, switch to pythonw.exe (for no console window)
    if exe_path.lower().endswith(("python.exe", "pythonw.exe")):
        pythonw_path = exe_path.replace("python.exe", "pythonw.exe")  # Change to pythonw.exe
        target = pythonw_path
        arguments = f'"{script_path}"'  # Pass `main.py` as an argument
    else:
        target = script_path  # If running as .exe, use it directly
        arguments = ""  # No extra arguments

    # Create a Windows shortcut
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target  # Set to pythonw.exe or the .exe
    shortcut.Arguments = arguments  # Pass script as argument (if needed)
    shortcut.WorkingDirectory = os.path.dirname(script_path)  # Set working directory
    shortcut.Description = "WallpaperCacheUpdater - Automatically runs on startup."
    shortcut.Save()

    print(f"Shortcut created: {shortcut_path}")

if __name__ == "__main__":
    add_to_startup()
