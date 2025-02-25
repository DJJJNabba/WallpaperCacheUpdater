#!/usr/bin/env python
"""
install_dependencies.py

Reads required dependencies from `requirements.txt`, installs missing ones,
notifies the user, and restarts the application.
"""

import sys
import subprocess
import os
import tkinter as tk
from tkinter import messagebox

# Path to requirements.txt
REQUIREMENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

def read_requirements():
    """Read the required packages from requirements.txt and return as a list."""
    if not os.path.exists(REQUIREMENTS_FILE):
        messagebox.showerror("Error", "requirements.txt file not found! Please create one.")
        sys.exit(1)  # Exit if the file is missing

    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        # Read and strip whitespace/newlines, ignoring empty lines and comments
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

def check_and_install_packages():
    """Check for missing packages and install them if necessary."""
    required_packages = read_requirements()
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.split("==")[0])  # Handle package names with versions (e.g., requests==2.26.0)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        root = tk.Tk()
        root.withdraw()  # Hide the Tkinter root window

        messagebox.showinfo("Installing Dependencies", 
                            f"Missing packages detected: {', '.join(missing_packages)}\n\nInstalling now...")

        # Install missing packages
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

        messagebox.showinfo("Installation Complete", 
                            "All required packages have been installed.\nRestarting the application.")

        # Restart the main script
        restart_application()

def restart_application():
    """Restarts the main application after dependencies are installed."""
    python_executable = sys.executable
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

    subprocess.Popen([python_executable, script_path], start_new_session=True)
    os._exit(0)  # Exit current script to avoid conflicts

if __name__ == "__main__":
    check_and_install_packages()
