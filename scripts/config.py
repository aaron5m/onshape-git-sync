import os
from pathlib import Path

# Directories for logs and snapshots
BASE_DIR = Path(__file__).parent.parent.resolve()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # ensure folder exists
SNAPSHOT_DIR = BASE_DIR / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)  # ensure folder exists

# If environment variables are not found
def get_env_var(env_key):
    with open(BASE_DIR / "onsync.env") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, value = line.strip().split("=", 1)
            if key == env_key:
                return value

# Toggle mode for debugging
OFFLINE_MODE = False

# Read Document ID, and API keys from environment (or fallback)
DOCUMENT_ID = os.environ.get("ONSHAPE_DOC_ID", get_env_var("ONSHAPE_DOC_ID")).strip()
API_KEY = os.environ.get("ONSHAPE_API_KEY", get_env_var("ONSHAPE_API_KEY")).strip()
API_SECRET = os.environ.get("ONSHAPE_API_SECRET", get_env_var("ONSHAPE_API_SECRET")).strip()

