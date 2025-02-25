#!/usr/bin/env python
"""
main.py

Entry point for the WallpaperChanger application.
Initializes configuration, checks for updates, sets the wallpaper on startup,
and sets up the system tray icon.
"""

import sys
import os
import threading
import time
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
    Restart the application after an update.
    """
    print("Restarting application...")
    python = sys.executable  # Get path to pythonw.exe or main executable
    script = os.path.abspath(__file__)  # Path to main.py (or .exe)

    # Restart the application
    os.execv(python, [python, script])  # This replaces the current process

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
        update_files()

        # Wait a moment to ensure updates are applied properly
        time.sleep(2)

        # Restart the application automatically
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
