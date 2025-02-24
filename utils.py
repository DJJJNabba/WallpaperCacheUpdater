"""
utils.py

Creates a shortcut in the Windows Startup folder (`shell:startup`) to run the application on startup.
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

    # Get the executable path
    exe_path = sys.executable  # Path to Python interpreter or compiled .exe
    script_path = os.path.abspath(__file__)  # Path to the current script

    # If running as a Python script, we need to include the script as an argument
    if exe_path.lower().endswith(("python.exe", "pythonw.exe")):
        target = exe_path  # Target is Python itself
        arguments = f'"{script_path}"'  # The script is passed as an argument
    else:
        target = script_path  # Running as an .exe, so use script_path directly
        arguments = ""  # No arguments needed

    # Create a Windows shortcut
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.Description = "WallpaperCacheUpdater - Automatically applies saved wallpaper on startup."
    shortcut.Save()

    print(f"Shortcut created: {shortcut_path}")

if __name__ == "__main__":
    add_to_startup()
