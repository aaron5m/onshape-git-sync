from pathlib import Path
from utils import *
from datetime import datetime
import requests

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
    LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
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
# MAIN ORCHESTRATION
# -----------------------------
if __name__ == "__main__":
    DOCUMENT_ID = "c7d8e47c243d8bf4bb749415"

    # Step 1: Try to fetch & archive
    OFFLINE_MODE = False  # set to True to skip API fetch while developing

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

    # Step 3: Process as usual
    all_versions = get_all_versions(last_good_log)
    latest_version = get_latest_version(all_versions)

    print("Loaded", len(all_versions), "versions")
    print("Latest version:", latest_version.get("name"))

