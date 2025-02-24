#!/usr/bin/env python
"""
main.py

Entry point for the WallpaperChanger application.
Initializes configuration, checks for updates, sets the wallpaper on startup,
and sets up the system tray icon.
"""

import sys
import threading
from config import load_config, save_config, CONFIG_FILE_PATH
from updater import check_for_updates, perform_update
from wallpaper import apply_saved_wallpaper
from tray import start_tray_icon
from utils import add_to_startup

# Current version of the application.
CURRENT_VERSION = "1.0.0"

def update_check():
    """
    Check if there is an update available on GitHub.
    If so, prompt the user and perform the update if accepted.
    """
    try:
        update_info = check_for_updates(CURRENT_VERSION)
        if update_info["update_available"]:
            # Using a simple Tkinter popup to ask the user about updating.
            # (You can also integrate this into the system tray interface if preferred.)
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            if messagebox.askyesno("Update Available", "An update is available. Install now?"):
                # Perform update. This may require the application to restart.
                perform_update(update_info["download_url"])
                messagebox.showinfo("Update", "Update installed. Please restart the application.")
                sys.exit(0)
    except Exception as e:
        # Log the error or handle as needed
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
