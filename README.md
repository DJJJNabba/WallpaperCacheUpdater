# WallpaperChanger

WallpaperChanger is a Python-based application that allows you to change your Windows wallpaper via a system tray icon. It includes a built-in updater that checks GitHub for new releases, runs on system startup, and preserves your selected wallpaper and configuration across updates.

## Features

- **Built-in Updater:** Checks GitHub for updates on launch and offers to update the program.
- **System Startup:** Automatically runs on system startup.
- **System Tray Icon:** Runs in the system tray with options to change the wallpaper or exit.
- **Persistent Configuration:** Remembers the selected wallpaper and reapplies it on startup.
- **Modular Design:** Code is organized into modules for ease of maintenance and scalability.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
