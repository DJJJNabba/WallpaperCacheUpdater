"""
wallpaper.py

Contains functions for selecting an image, copying it to the correct location,
and applying it as the desktop wallpaper.
"""

import os
import shutil
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from config import load_config, save_config

def select_image():
    """
    Opens a file dialog for the user to select an image.
    Returns the path to the selected image or None if cancelled.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")]
    )
    if not file_path:
        messagebox.showinfo("Cancelled", "No file was selected.")
        return None
    return file_path

def update_wallpaper(new_image_path):
    """
    Copies the new image to the system's wallpaper location and refreshes the desktop wallpaper.
    Saves the selected wallpaper path in the configuration.
    """
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise EnvironmentError("APPDATA environment variable not found.")

    dest_dir = os.path.join(appdata, "Microsoft", "Windows", "Themes")
    dest_path = os.path.join(dest_dir, "TranscodedWallpaper")

    if not os.path.isdir(dest_dir):
        raise FileNotFoundError(f"Destination directory does not exist: {dest_dir}")

    try:
        # Copy the selected image over the current wallpaper
        shutil.copy2(new_image_path, dest_path)

        # Force Windows to refresh the desktop wallpaper
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 1
        SPIF_SENDCHANGE = 2
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, dest_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        if not result:
            raise ctypes.WinError()

        # Save the selected wallpaper in config so it can be reapplied on startup.
        config = load_config()
        config["wallpaper_path"] = new_image_path
        save_config(config)

        messagebox.showinfo("Success", "Wallpaper updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update wallpaper:\n{e}")

def apply_saved_wallpaper(wallpaper_path):
    """
    Apply the saved wallpaper if it exists.
    """
    if not os.path.isfile(wallpaper_path):
        raise FileNotFoundError("Saved wallpaper file does not exist.")
    update_wallpaper(wallpaper_path)