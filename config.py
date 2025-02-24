"""
config.py

Handles loading and saving of the application's configuration data.
Configuration is stored in a JSON file. The file is kept in the user's APPDATA folder
(or a similar location) to preserve settings across updates.
"""

import os
import json

def get_config_dir():
    """
    Get the directory where the config file should be stored.
    Uses the APPDATA environment variable on Windows, or falls back to the home directory.
    """
    appdata = os.environ.get("APPDATA")
    if appdata:
        config_dir = os.path.join(appdata, "WallpaperCacheUpdater")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".wallpapercacheupdater")
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    return config_dir

CONFIG_FILE_PATH = os.path.join(get_config_dir(), "config.json")

def load_config():
    """
    Load configuration from a JSON file.
    If the file does not exist, returns a default configuration.
    """
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
    except Exception:
        config = {"wallpaper_path": None}
    return config

def save_config(config):
    """
    Save the configuration dictionary to a JSON file.
    """
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)