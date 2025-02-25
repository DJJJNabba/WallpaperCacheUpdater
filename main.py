#!/usr/bin/env python
"""
main.py

Entry point for the WallpaperChanger application.
Initializes configuration, checks for updates, sets the wallpaper on startup,
and sets up the system tray icon.
"""

import install_dependencies

import sys
import os
import threading
import time
import subprocess
import tkinter as tk
from tkinter import messagebox
from config import load_config, save_config, CONFIG_FILE_PATH
from updater import update_files, get_local_version, get_remote_version
from wallpaper import apply_saved_wallpaper
from tray import start_tray_icon
from utils import add_to_startup

# Path to version file
VERSION_FILE = "version.txt"

def get_current_version():
    """
    Reads the current version from version.txt.
    """
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "0.0.0"  # Default version if file doesn't exist

def restart_application():
    """
    Restart the application after an update, ensuring the old process is fully terminated.
    """
    print("Restarting application...")

    python_executable = sys.executable  # Path to pythonw.exe or compiled .exe
    script_path = os.path.abspath(__file__)  # Path to main.py (or the .exe)

    # Ensure the command is in a list format to properly handle spaces
    command = [python_executable, script_path]

    # Start a new process
    subprocess.Popen(command, start_new_session=True)

    # Wait a bit to ensure the new process starts properly
    time.sleep(1)

    # Forcefully exit the current process to avoid duplicates
    os._exit(0)  # This immediately terminates the script without cleanup delays

def update_check():
    """
    Fetch the latest code from GitHub and apply the update.
    If an update is installed, restart the application automatically.
    """
    try:
        local_version = get_local_version()
        remote_version = get_remote_version()
        
        if not remote_version or local_version == remote_version:
            print("No updates available.")
            return  # Exit if already up to date

        print(f"New version detected! Updating from {local_version} to {remote_version}...")

        # Ask the user if they want to install the update
        root = tk.Tk()
        root.withdraw()  # Hide Tkinter window

        if messagebox.askyesno("Update Available", f"A new version ({remote_version}) is available. Install now?"):
            update_files()
            messagebox.showinfo("Update", "Update installed. Restarting...")
            restart_application()

    except Exception as e:
        print(f"Update check failed: {e}")

def main():
    # Load configuration (or create default config if none exists)
    config = load_config()

    # Add program to startup (so it runs when the user logs in)
    try:
        add_to_startup()
    except Exception as e:
        print(f"Failed to add to startup: {e}")

    # If a wallpaper is saved in config, apply it on startup
    if config.get("wallpaper_path"):
        try:
            apply_saved_wallpaper(config["wallpaper_path"])
        except Exception as e:
            print(f"Failed to apply saved wallpaper: {e}")

    # Run the update check in a separate thread to avoid blocking
    update_thread = threading.Thread(target=update_check)
    update_thread.start()

    # Start the system tray icon (blocking call)
    start_tray_icon()

if __name__ == "__main__":
    main()
