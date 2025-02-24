"""
tray.py

Implements the system tray icon using pystray.
Provides menu options for 'Change Wallpaper' and 'Exit'.
"""

import threading
import sys
import tkinter as tk
from tkinter import messagebox
import pystray
import os
from PIL import Image, ImageDraw
from wallpaper import select_image, update_wallpaper
from config import load_config, save_config

def create_image():
    """
    Load the correct icon for the system tray.
    """
    from PIL import Image
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

    try:
        if os.path.exists(icon_path):
            return Image.open(icon_path).convert("RGBA")  # Ensure proper format
        else:
            print("Icon file not found! Using default icon.")
    except Exception as e:
        print(f"Error loading system tray icon: {e}")

    # Fallback: Generate a default icon if icon.ico is missing
    image = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    d = ImageDraw.Draw(image)
    d.rectangle((16, 16, 48, 48), fill=(0, 120, 215))
    return image


def on_change_wallpaper(icon, item):
    """
    Opens the file dialog to select a new wallpaper in a separate Tkinter window,
    ensuring the tray icon remains responsive.
    """
    def select_and_update():
        # Create a new Tkinter instance
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        new_image = select_image()
        if new_image:
            update_wallpaper(new_image)

        root.destroy()  # Destroy the Tkinter instance after selection

    # Run file selection in a new thread to avoid freezing the system tray
    threading.Thread(target=select_and_update, daemon=True).start()


def on_exit(icon, item):
    """
    Callback for the 'Exit' menu item.
    Stops the tray icon and exits the application.
    """
    icon.stop()
    sys.exit(0)

def start_tray_icon():
    """
    Initializes and starts the system tray icon with menu items.
    This call is blocking.
    """
    icon = pystray.Icon("WallpaperChanger", create_image(), "Wallpaper Changer", menu=pystray.Menu(
        pystray.MenuItem("Change Wallpaper", on_change_wallpaper),
        pystray.MenuItem("Exit", on_exit)
    ))
    icon.run()