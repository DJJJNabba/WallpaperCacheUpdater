import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub raw content URL (update this with your actual username & repo)
GITHUB_USER = "DJJJNabba"
GITHUB_REPO = "WallpaperCacheUpdater"
GITHUB_BRANCH = "main"  # Change if using a different branch
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/"

# List of files to update (modify if needed)
FILES_TO_UPDATE = [
    "main.py",
    "updater.py",
    "config.py",
    "wallpaper.py",
    "tray.py",
    "utils.py"
]

LOCAL_VERSION_FILE = "version.txt"
REMOTE_VERSION_URL = f"{GITHUB_RAW_BASE}version.txt"

def get_local_version():
    """ Reads the local version from version.txt. """
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"  # Default version if no version file exists
    with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()
    
def get_remote_version():
    """ Fetches the latest version from GitHub. """
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=10, verify=False)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"Failed to fetch remote version: {e}")
    return None

def download_file(filename):
    """ Fetches the latest version of a file from GitHub raw and saves it locally. """
    url = f"{GITHUB_RAW_BASE}{filename}"
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content.replace(b"\r\n", b"\n"))  # Fix line spacing issue
            print(f"Updated: {filename}")
        else:
            print(f"Failed to download {filename}. HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def update_files():
    """ Updates files only if a new version is detected. """
    local_version = get_local_version()
    remote_version = get_remote_version()

    if not remote_version:
        print("Could not check for updates. Skipping.")
        return

    if local_version == remote_version:
        print("No updates available.")
        return  # Exit if already up to date

    print(f"New version detected! Updating from {local_version} to {remote_version}...")
    for file in FILES_TO_UPDATE:
        download_file(file)

    # Update local version file
    with open(LOCAL_VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(remote_version)

    print("Update complete!")

if __name__ == "__main__":
    update_files()
