from pathlib import Path
import json

# -----------------------------
# Step 1: Fetch / read all versions
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
# Step 2: Pick the latest version
# -----------------------------
def get_latest_version(versions):
    """
    Accepts a list of version objects and returns the latest one.
    """
    latest = max(versions, key=lambda v: v.get("createdAt", ""))
    return latest
