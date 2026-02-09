from pathlib import Path
from utils import get_latest_version

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "tmp" / "tmp.json"

latest_version = get_latest_version(DATA_FILE)

print("Latest version:", latest_version.get("name"))

