"""
utils.py

Creates a shortcut in both the Windows Startup folder (`shell:startup`) and the Desktop.
Uses a custom icon for the shortcut.
"""

import os
import sys
import winshell
from win32com.client import Dispatch

# Define the icon path (must be an .ico file)
ICON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

def create_shortcut(shortcut_path, target, arguments, working_directory, description, icon_path):
    """
    Creates a Windows shortcut (.lnk) with the specified parameters.
    """
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target  # The program to run
    shortcut.Arguments = arguments  # Arguments (if any)
    shortcut.WorkingDirectory = working_directory  # Where the shortcut starts
    shortcut.Description = description  # Tooltip description
    if os.path.exists(icon_path):  # Only set the icon if it exists
        shortcut.IconLocation = icon_path
    shortcut.Save()

    print(f"Shortcut created: {shortcut_path}")

def add_to_startup():
    """
    Adds the application to Windows startup by creating a shortcut in the Startup folder.
    Also creates a shortcut on the Desktop.
    """
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "main.py")  # Ensure main.py is used

    # Get the paths for Startup and Desktop
    startup_folder = winshell.startup()
    desktop_folder = winshell.desktop()

    startup_shortcut = os.path.join(startup_folder, "WallpaperCacheUpdater.lnk")
    desktop_shortcut = os.path.join(desktop_folder, "WallpaperCacheUpdater.lnk")

    # Determine the correct executable
    exe_path = sys.executable  # Python interpreter or compiled .exe

    # Use pythonw.exe for scripts to avoid a console window
    if exe_path.lower().endswith(("python.exe", "pythonw.exe")):
        pythonw_path = exe_path.replace("python.exe", "pythonw.exe")
        target = pythonw_path  # Run with pythonw.exe
        arguments = f'"{script_path}"'  # Pass script as an argument
    else:
        target = script_path  # If running as an .exe, use it directly
        arguments = ""  # No arguments needed

    # Create shortcuts in both Startup and Desktop
    create_shortcut(startup_shortcut, target, arguments, script_dir, "WallpaperCacheUpdater - Automatically runs on startup.", ICON_FILE)
    create_shortcut(desktop_shortcut, target, arguments, script_dir, "WallpaperCacheUpdater - Quick access to the app.", ICON_FILE)

if __name__ == "__main__":
    add_to_startup()
