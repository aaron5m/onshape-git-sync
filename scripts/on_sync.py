import os
import json
from pathlib import Path
from utils import *
from datetime import datetime
import requests

# CONFIGURATION
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"
DOCUMENT_ID = "c7d8e47c243d8bf4bb749415"
OFFLINE_MODE = False

# -----------------------------
# Step 0: Read API keys
# -----------------------------
def read_key(name):
    """Read a secret from the keys folder."""
    KEY_DIR = Path(__file__).resolve().parents[2] / "keys"
    return (KEY_DIR / name).read_text().strip()
    
# -----------------------------
# Step 1a: Fetch versions from API
# -----------------------------
def fetch_versions_from_api(document_id):
    """
    Fetch all versions for a given Onshape document and workspace using the API.
    Returns JSON as a Python object.
    """
    API_KEY = read_key("onshape-api-access.txt")
    API_SECRET = read_key("onshape-api-secret.txt")

    # Example endpoint (adjust to real Onshape API docs):
    url = f"https://cad.onshape.com/api/v10/documents/d/{document_id}/versions?offset=0&limit=0"

    # Basic authentication with key/secret
    response = requests.get(url, auth=(API_KEY, API_SECRET))
    response.raise_for_status()  # stop if the request failed

    return response.json()

# -----------------------------
# Step 1b: Use Fetch to Archive
# -----------------------------
def fetch_and_archive_versions(document_id):
    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        data = fetch_versions_from_api(document_id)

        log_path = LOG_DIR / f"{timestamp}.json"
        with open(log_path, "w") as f:
            json.dump(data, f, indent=2)

        return log_path

    except Exception as e:
        error_path = LOG_DIR / f"{timestamp}.error.json"
        with open(error_path, "w") as f:
            json.dump(
                {
                    "error": str(e),
                    "timestamp": timestamp
                },
                f,
                indent=2
            )

        return None

# -----------------------------
# Step 2: Read last good archive
# -----------------------------
def get_latest_valid_log():
    LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
    if not LOG_DIR.exists():
        return None

    valid_logs = sorted(
        [f for f in LOG_DIR.iterdir() if f.suffix == ".json" and not f.name.endswith(".error.json")]
    )

    if not valid_logs:
        return None

    return valid_logs[-1]

# -----------------------------
# Step 3: Archive with snapshot of each version by its timestamp
# -----------------------------
def archive_versions_to_local_snapshots(all_versions):
    """
    For each version in all_versions:
      - Create a timestamped folder based on current time
      - If folder already exists, skip (idempotent)
      - Save snapshot.json inside the folder with the full version data
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    for version in all_versions:
    
        # Extract Onshape's version creation timestamp
        created_at = version.get("createdAt")
        if not created_at:
            print(f"Warning: version {version.get('name')} missing 'createdAt'; skipping")
            continue

        # Convert ISO 8601 timestamp to folder-friendly format
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))  # handle UTC Z
            timestamp_folder_name = dt.strftime("%Y%m%d_%H%M%S")
        except Exception as e:
            print(f"Error parsing timestamp for version {version.get('name')}: {e}")
            continue
            
        # Build folder path
        version_folder = os.path.join(SNAPSHOT_DIR, timestamp_folder_name)
        
        # Skip if folder already exists
        if not os.path.exists(version_folder):
            os.makedirs(version_folder, exist_ok=True)

            snapshot_file = os.path.join(version_folder, "snapshot.json")
            with open(snapshot_file, "w") as f:
                json.dump(version, f, indent=2)
            
            print(f"Archived in {timestamp_folder_name} snapshot for version: {version.get('name')}")
        else:
            print(f"Snapshot {timestamp_folder_name} already exists as version: {version.get('name')}")
            pass


# -----------------------------
# MAIN ORCHESTRATION
# -----------------------------
def main():

    # Step 1: Try to fetch & archive

    if not OFFLINE_MODE:
        print("Attempting API fetch from Onshape…")
        log_written = fetch_and_archive_versions(DOCUMENT_ID)

        if log_written:
            print(f"Fetched and archived new API data: {log_written}")
        else:
            print("API fetch failed; falling back to last known good log")
    else:
        print("OFFLINE_MODE enabled; skipping API fetch")

    # Step 2: Load last valid log
    last_good_log = get_latest_valid_log()

    if not last_good_log:
        raise RuntimeError("No valid logs available to continue")

    print(f"Using log file: {last_good_log}")

    # Step 3: Load versions and archive
    all_versions = get_all_versions(last_good_log)
    archive_versions_to_local_snapshots(all_versions)

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
