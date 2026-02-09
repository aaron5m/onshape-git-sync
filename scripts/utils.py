# utils.py
from pathlib import Path
import json

def get_latest_version(json_path):
    """
    Reads a JSON file of Onshape versions and returns the latest version object.
    """
    json_path = Path(json_path)
    with open(json_path) as f:
        versions = json.load(f)
    latest = max(
        versions,
        key=lambda v: v.get("createdAt", "")
    )
    return latest

