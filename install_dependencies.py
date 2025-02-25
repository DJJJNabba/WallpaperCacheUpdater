#!/usr/bin/env python
"""
install_dependencies.py

Reads required dependencies from `requirements.txt`, installs missing ones,
notifies the user, and restarts the application if necessary.
"""

import sys
import subprocess
import os
import importlib.util
import tkinter as tk
from tkinter import messagebox

# Path to requirements.txt
REQUIREMENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

def read_requirements():
    """Read the required packages from requirements.txt and return them as a list."""
    if not os.path.exists(REQUIREMENTS_FILE):
        messagebox.showerror("Error", "requirements.txt file not found! Please create one.")
        sys.exit(1)  # Exit if the file is missing

    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        # Read and strip whitespace/newlines, ignoring empty lines and comments
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

def is_package_installed(package_name):
    """Check if a package is installed using importlib.util.find_spec()."""
    # Some packages have different install names, define mapping here:
    PACKAGE_MAPPING = {
        "pywin32": "win32api",  # pywin32 installs win32api
        "Pillow": "PIL",        # Pillow installs under PIL
        "winshell": "winshell"
    }

    module_name = PACKAGE_MAPPING.get(package_name, package_name)

    return importlib.util.find_spec(module_name) is not None

def check_and_install_packages():
    """Check for missing packages and install them if necessary."""
    required_packages = read_requirements()
    missing_packages = [pkg for pkg in required_packages if not is_package_installed(pkg.split("==")[0])]

    if missing_packages:
        root = tk.Tk()
        root.withdraw()  # Hide the Tkinter root window

        messagebox.showinfo("Installing Dependencies", 
                            f"Missing packages detected: {', '.join(missing_packages)}\n\nInstalling now...")

        # Install missing packages
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

        messagebox.showinfo("Installation Complete", 
                            "All required packages have been installed.\nRestarting the application.")

if __name__ == "__main__":
    check_and_install_packages()
