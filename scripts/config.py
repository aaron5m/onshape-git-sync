import os
from pathlib import Path

# Directories for logs and snapshots
BASE_DIR = Path(__file__).parent.parent.resolve()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # ensure folder exists
SNAPSHOT_DIR = BASE_DIR / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)  # ensure folder exists

# Toggle mode for debugging
OFFLINE_MODE = False

# Change to your Document ID
DOCUMENT_ID = "c7d8e47c243d8bf4bb749415"

# Change the path to your keys
KEY_DIR = Path(__file__).resolve().parents[2] / "keys"

