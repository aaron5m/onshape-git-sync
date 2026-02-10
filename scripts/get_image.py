import os
import requests
from utils import *


def generate_assembly_image(document_id, element_id, snapshot_root):
    """
    Generates an image (render preview) for the given assembly element,
    and saves it to a dedicated 'img' folder inside the element's snapshot directory.
    """
    # Path for saving images
    snapshot_folder = f"{snapshot_root}/{element_id}"
    img_folder = os.path.join(snapshot_folder, "img")

    # Ensure the 'img' folder exists
    os.makedirs(img_folder, exist_ok=True)
    
    # Define the path for the image file
    image_file_path = os.path.join(img_folder, f"{element_id}_assembly.png")

    # Check if the image already exists
    if os.path.exists(image_file_path):
        print(f"Image already exists for element {element_id}, skipping API call.")
        return

    # Prepeare the API Call
    API_KEY = read_key("onshape-api-access.txt")
    API_SECRET = read_key("onshape-api-secret.txt")

    url = f"https://cad.onshape.com/api/preview/elements/{element_id}"
    
    # Define parameters for the view (TRIMETRIC) and size (1024x1024)
    params = {
        "view": "TRIMETRIC",  # Set the view type
        "width": 1024,        # Set the width
        "height": 1024        # Set the height
    }

    # Send the POST request to generate the image
    response = requests.post(url, params=params, auth=(API_KEY, API_SECRET))

    if response.status_code == 200:
        # Save the image to the 'img' folder
        with open(image_file_path, "wb") as img_file:
            img_file.write(response.content)
        print(f"Image saved to: {image_file_path}")
    else:
        print(f"Failed to generate image for element {element_id}")

