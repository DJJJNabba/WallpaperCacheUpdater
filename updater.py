"""
updater.py

This module checks GitHub for available updates and performs self-update.
It uses the GitHub Releases API to compare the current version with the latest release.
"""

import os
import sys
import shutil
import requests
import zipfile
import tempfile

GITHUB_USER = "DJJJNabba"
GITHUB_REPO = "WallpaperCacheUpdater"

def get_latest_release_info():
    """
    Query the GitHub API to get the latest release information.
    """
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch release info from GitHub.")
    return response.json()

def check_for_updates(current_version):
    """
    Compare the current version with the latest version on GitHub.
    Returns a dictionary with update_available (bool) and download_url (str) keys.
    """
    release_info = get_latest_release_info()
    latest_version = release_info.get("tag_name", "0.0.0")
    update_available = latest_version != current_version

    # Get the asset download URL (assuming a zip file is attached)
    download_url = None
    for asset in release_info.get("assets", []):
        if asset["name"].endswith(".zip"):
            download_url = asset["browser_download_url"]
            break

    return {"update_available": update_available, "download_url": download_url, "latest_version": latest_version}

def perform_update(download_url):
    """
    Download the update zip file from GitHub, extract it, and replace current files.
    This function should preserve user data like config and saved wallpaper.
    """
    if not download_url:
        raise Exception("No download URL available for the update.")

    # Create a temporary directory to download and extract the update
    tmp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(tmp_dir, "update.zip")

    # Download the update
    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download the update.")
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract the update
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(tmp_dir)

    # Copy over the new files.
    # IMPORTANT: Ensure that you preserve user data such as config and saved wallpaper.
    # For example, assume the update folder structure mirrors the current project.
    project_root = os.path.dirname(os.path.abspath(__file__))
    updated_root = os.path.join(tmp_dir, "WallpaperCacheUpdater")  # Adjust if needed

    if not os.path.isdir(updated_root):
        raise Exception("Update package structure is invalid.")

    # Here we copy over all files from updated_root to project_root,
    # skipping the config file (or any user data folder).
    for item in os.listdir(updated_root):
        s = os.path.join(updated_root, item)
        d = os.path.join(project_root, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            # Skip config file if you want to preserve user settings
            if os.path.basename(s) == "config.json":
                continue
            shutil.copy2(s, d)

    # Clean up temporary directory
    shutil.rmtree(tmp_dir)
    # Optionally, you can trigger a restart here.
    # For this demo, we just exit and prompt the user to restart.
    sys.exit(0)
