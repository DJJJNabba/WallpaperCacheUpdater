import os
import requests

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

def download_file(filename):
    """
    Fetches the latest version of a file from the GitHub raw content URL.
    Overwrites the local file with the new version.
    """
    url = f"{GITHUB_RAW_BASE}{filename}"
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content.replace(b"\r\n", b"\n"))  # <- Fixes extra lines issue
            print(f"Updated: {filename}")
        else:
            print(f"Failed to download {filename}. HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def update_files():
    """
    Loops through all files and updates them from GitHub raw.
    """
    print("Checking for updates...")
    for file in FILES_TO_UPDATE:
        download_file(file)
    print("Update complete!")

if __name__ == "__main__":
    update_files()
