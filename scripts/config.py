import os
from pathlib import Path

# Directories for logs and snapshots
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"

# Toggle mode for debugging
OFFLINE_MODE = False

# Change to your Document ID
DOCUMENT_ID = "c7d8e47c243d8bf4bb749415"

# Change the path to your keys
KEY_DIR = Path(__file__).resolve().parents[2] / "keys"

