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

# Read Document ID, and API keys from environment (or fallback up to keys folder)
DOCUMENT_ID = os.environ.get("ONSHAPE_DOC_ID").strip()
API_KEY = os.environ.get("ONSHAPE_API_KEY").strip()
API_SECRET = os.environ.get("ONSHAPE_API_SECRET").strip()


