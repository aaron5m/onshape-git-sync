from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

def get_latest_version(json_path):

    """
    Reads a JSON file of Onshape versions and returns the latest version object.
    Args:
        json_path (Path or str): Path to the JSON file.
    Returns:
        dict: The latest version (with fields like id, name, createdAt, description).
    """
    
    # Ensure we have a Path object
    json_path = Path(json_path)
    
    # Load the JSON
    with open(json_path) as f:
        versions = json.load(f)
    
    # Find the latest version based on createdAt timestamp
    latest = max(
        versions,
        key=lambda v: v.get("createdAt", "")
    )
    
    return latest




DATA_FILE = BASE_DIR / "tmp" / "tmp.json"

latest = get_latest_version(DATA_FILE)

print("Latest version:")
print("ID:", latest.get("id"))
print("Name:", latest.get("name"))
print("Created:", latest.get("createdAt"))
print("Notes:", latest.get("description"))

