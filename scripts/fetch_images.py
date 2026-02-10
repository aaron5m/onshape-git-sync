import os
import requests
from pathlib import Path
from utils import *
from datetime import datetime
import json
import base64
import sys

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

# After fetch_elements has written elements.json

# ----------------------
# Step 1, load elements
# ----------------------

def load_elements_json(elements_file_path):
    """
    Load elements.json from disk and return it as a Python object.
    """
    with open(elements_file_path, "r") as f:
        return json.load(f)

# ----------------------
# Step 2, extract assembly elements
# ----------------------

def extract_assemblies(elements_json):
    """
    Given elements JSON (list of dicts),
    return a list of assemblies with id and name.
    """
    assemblies = []

    for element in elements_json:
        if element.get("elementType") == "ASSEMBLY":
            assemblies.append({
                "id": element.get("id"),
                "name": element.get("name")
            })

    return assemblies
    
# --------------------
# Step 3, with an assembly element id (and other) generate an image
# -----

def generate_assembly_image(document_id, version, element_id):
    """
    Generates an image (render preview) for the given assembly element,
    and saves it to a dedicated 'img' folder inside the element's snapshot directory.
    """
    # Get version id
    version_id = version.get("id")
    
    # Extract Onshape's version creation timestamp
    created_at = version.get("createdAt")
    if not created_at:
        print(f"Warning: version {version.get('name')} missing 'createdAt'; cannot generate images")
        return

    # Convert ISO 8601 timestamp to folder-friendly format
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))  # handle UTC Z
        timestamp_folder_name = dt.strftime("%Y%m%d_%H%M%S")
    except Exception as e:
        print(f"Error parsing timestamp for version {version.get('name')}: {e}")
        return
        
    # Build folder path
    version_folder = os.path.join(SNAPSHOT_DIR, timestamp_folder_name)
    img_folder = os.path.join(version_folder, "img")

    # Ensure the folder exists
    os.makedirs(img_folder, exist_ok=True)
    
    # Prepeare the API Call
    API_KEY = read_key("onshape-api-access.txt")
    API_SECRET = read_key("onshape-api-secret.txt")

    url = f"https://cad.onshape.com/api/v10/assemblies/d/{document_id}/v/{version_id}/e/{element_id}/shadedviews"
    
    # Define parameters for the view (TRIMETRIC) and size (1024x1024)
    #trimetric_matrix = "0.612,0.612,-0.5,0,-0.354,0.707,0.612,0,0.707,-0.354,0.612,0"
    trimetric_matrix = "trimetric"
    params = {
        "viewMatrix": trimetric_matrix,
        "useFrame": "true",
        "width": "1024",
        "height": "1024",
        "pixelSize": "0",
        "edges": "generate"
    }

    try:
        response = requests.get(url, params=params, auth=(API_KEY, API_SECRET))
        
        print(response.request.url)

        if response.status_code == 200:
            views = response.json()  # parse array of shaded view objects
            images = views.get("images", [])

            if not images:
                print(f"No images returned for element {element_id}")
                return

            for i, image_data in enumerate(images, start=1):
                file_path = os.path.join(img_folder, f"{element_id}_view{i}.png")
                decoded = base64.b64decode(image_data)
                with open(file_path, "wb") as f:
                    f.write(decoded)
                print(f"Saved {file_path}")
                    
        else:
            # Log the error details to a file for later inspection
            #log_folder = "logs/image_errors"
            #os.makedirs(log_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(LOG_DIR, f"{element_id}_error_{timestamp}.error.json")

            try:
                error_content = response.json()  # try JSON if possible
            except Exception:
                error_content = response.text  # fallback to raw text

            with open(log_file, "w") as f:
                json.dump({
                    "status_code": response.status_code,
                    "response": error_content
                }, f, indent=2)

            print(f"Failed to generate image for element {element_id}, status code: {response.status_code}")
            print(f"Error details logged to: {log_file}")

    except Exception as e:
        print(f"Exception occurred while generating image for element {element_id}: {e}")

# -----
# Step 4, loop for a version to get all iamges of assemblies (call steps 1-3)
# -----

def capture_assembly_images_for_version(document_id, version):
    """
    For the given version, fetch the assemblies and capture an image for each.
    """
    # Get version id
    version_id = version.get("id")

    if not version_id:
        print(f"No valid version ID found for version {version.get('name')}")
        return

    # Get all assemblies for the version
    elements_file_path = f"{SNAPSHOT_DIR}/{version_id}/elements.json"
    
    try:
        elements = load_elements_json(elements_file_path)
        assemblies = extract_assemblies(elements)

        # Now generate images for each assembly
        for assembly in assemblies:
            print(f"Generating image for assembly: {assembly['name']}")
            generate_assembly_image(document_id, version, assembly['id'])

    except Exception as e:
        print(f"Error processing version {version.get('name')}: {e}")



# TEST



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
# Pick the latest version
# -----------------------------
def get_latest_version(versions):
    """
    Accepts a list of version objects and returns the latest one.
    """
    latest = max(versions, key=lambda v: v.get("createdAt", ""))
    return latest



versions = get_all_versions(f"{LOG_DIR}/20260210_084929.json")
latest_version = get_latest_version(versions)
generate_assembly_image("c7d8e47c243d8bf4bb749415", latest_version, "67cc15177a87419bc84dbe56")
