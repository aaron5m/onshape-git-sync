from pathlib import Path
from datetime import datetime
import json
from config import *

# -----------------------------
# Fetch / read all versions
# -----------------------------
def get_all_versions(json_input):
    """
    Accepts either a JSON file path or a Python object (dict/list),
    and returns a normalized list of version objects.
    """
    # Load from file if a path is given
    if isinstance(json_input, (str, Path)):
        with open(json_input) as f:
            data = json.load(f)
    else:
        data = json_input  # assume already loaded JSON

    # Normalize: either list at top level, or dict with 'items'
    if isinstance(data, list):
        versions = data
    elif isinstance(data, dict) and "items" in data:
        versions = data["items"]
    else:
        raise ValueError("Unexpected JSON structure")

    return versions

# -----------------------------
# Pick the latest version
# -----------------------------
def get_latest_version(versions):
    """
    Accepts a list of version objects and returns the latest one.
    """
    latest = max(versions, key=lambda v: v.get("createdAt", ""))
    return latest

# -----
# Get timestamp from version to create snapshot folder
# -----
def get_version_timestamp_folder_name(version):
    # Extract Onshape's version creation timestamp
    created_at = version.get("createdAt")
    if not created_at:
        print(f"Warning: version {version.get('name')} missing 'createdAt'; cannot generate images")
        return None

    # Convert ISO 8601 timestamp to folder-friendly format
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))  # handle UTC Z
        timestamp_folder_name = dt.strftime("%Y%m%d_%H%M%S")
        return timestamp_folder_name
        
    except Exception as e:
        print(f"Error parsing timestamp for version {version.get('name')}: {e}")
        return None

# -----
# Count subdirectories (for comparing if there has been a change)
# -----
def count_files(dir_path):
    total_files = 0
    for root, dirs, files in os.walk(dir_path):
        total_files += len(files)
    return total_files
