import os
from pathlib import Path
import json
import requests
from utils import *
from config import *

def fetch_and_archive_elements_for_version(document_id, version):
    """
    Fetch elements for a specific Onshape version and archive them as elements.json
    inside the version's snapshot folder.
    """
    version_id = version.get("id")
    created_at = version.get("createdAt")

    if not version_id or not created_at:
        print("Version missing id or createdAt; cannot fetch elements")
        return

    # Convert createdAt to snapshot folder name
    timestamp_folder_name = get_version_timestamp_folder_name(version)
    snapshot_path = os.path.join(SNAPSHOT_DIR, timestamp_folder_name)

    # Ensure snapshot folder exists
    if not os.path.exists(snapshot_path):
        print(f"Snapshot folder {snapshot_path} does not exist; skipping elements fetch")
        return

    elements_file = os.path.join(snapshot_path, "elements.json")
    error_file = os.path.join(snapshot_path, "elements.error")

    # Idempotency: don't refetch if already archived
    if os.path.exists(elements_file):
        print(f"elements.json already exists for version {version.get('name')}; skipping")
        return

    url = (
        f"https://cad.onshape.com/api/v10/documents/"
        f"d/{document_id}/v/{version_id}/elements"
    )

    try:
        response = requests.get(
            url,
            auth=(API_KEY, API_SECRET),
            timeout=15
        )
        response.raise_for_status()

        with open(elements_file, "w") as f:
            json.dump(response.json(), f, indent=2)

        print(f"Archived elements.json → {elements_file}")

    except requests.exceptions.RequestException as e:
        # Write a marker file instead of crashing
        with open(error_file, "w") as f:
            f.write(str(e))

        print(f"Failed to fetch elements for version {version.get('name')}")

