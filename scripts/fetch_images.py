import os
import re
from utils import *
# from onshape_client.client import Client

# --- AUTHENTICATION SETUP ---
ACCESS_KEY = read_key("onshape-api-access.txt")
SECRET_KEY = read_key("onshape-api-secret.txt")

client = Client(configuration={
    "base_url": "https://cad.onshape.com",
    "access_key": ACCESS_KEY,
    "secret_key": SECRET_KEY
})

# --- THE GENERATOR FUNCTION ---
def sanitize_filename(name):
    return re.sub(r'[^\w\-_\. ]', '', name).replace(' ', '_')

def generate_version_assets(did, vid, eid, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Note: Using client.assemblies_api directly
    explodes_response = client.assemblies_api.get_exploded_views(did, 'v', vid, eid)
    views = [{"id": None, "name": "Assembled_Final"}]
    
    if 'explodedViews' in explodes_response:
        for view in explodes_response['explodedViews']:
            views.append({"id": view['id'], "name": view.get('name', 'Unnamed_Explode')})

    trimetric_matrix = "0.612,-0.354,0.707,0,0.612,0.707,-0.354,0,-0.5,0.612,0.612,0,0,0,0,1"

    for view in views:
        safe_name = sanitize_filename(view['name'])
        params = {
            "viewMatrix": trimetric_matrix,
            "outputFormat": "png",
            "pixelSize": "0.003",
            "edges": "generate"
        }
        if view['id']:
            params["explodedViewId"] = view['id']

        print(f"Capturing: {view['name']}...")
        image_data = client.assemblies_api.get_shaded_views(did, 'v', vid, eid, **params)
        
        with open(os.path.join(target_dir, f"{safe_name}.png"), "wb") as f:
            f.write(image_data)

# --- RUN THE TEST ---
# Plug in your IDs from your URL: /documents/[DID]/v/[VID]/e/[EID]
test_did = "YOUR_DOC_ID"
test_vid = "YOUR_VER_ID"
test_eid = "YOUR_ELEMENT_ID"

generate_version_assets(test_did, test_vid, test_eid, "test_output")
