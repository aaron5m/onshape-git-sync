import os
from pathlib import Path
import json
import sys
import re

from datetime import datetime
from utils import *
from config import *

def update_snapshots_readme():

    # Initialize appropriate README for snapshots
    README_FILE = os.path.join(SNAPSHOT_DIR, "README.md")
    
    # Check if the README is already in use
    try:
        with open(README_FILE, "r") as f:
            readme_txt = f.read()
                        
    except FileNotFoundError:
        print("The README file for snapshots will be now be created")
        readme_txt = ""

    # Keep the TOP section of README if exists
    delimiter_pattern = r'\n-{3,}'  # newline followed by three or more dashes
    match = re.search(delimiter_pattern, readme_txt)
    if match:
        preserved = readme_txt[:match.start()]
    else:
        preserved = ""
    readme_lines = []
    readme_lines.append(f"{preserved}")
    readme_lines.append(f"\n---\n\n*Everything below this line will be overwritten/rewritten with next snapshot.*\n\n---\n")
    

    # Iterate through each identifier folder
    for identifier in sorted(os.listdir(SNAPSHOT_DIR), reverse=True):
        snapshot_path = os.path.join(SNAPSHOT_DIR, identifier)
        
        # Make sure it's a directory (skip the README)
        if not os.path.isdir(snapshot_path):
            continue
        
        # Read snapshot.json
        json_file = os.path.join(snapshot_path, "snapshot.json")
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} does not exist.")
            continue
            
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract descriptors from each snapshot
        name = data.get("name", identifier)
        description = data.get("description", identifier)
        modified_at = data.get("modifiedAt", identifier)
        human_time = datetime.fromisoformat(modified_at).strftime("%Y-%m-%d %H:%M:%S")
 
        readme_lines.append(f"### {name}  \n")
        readme_lines.append(f"### {human_time}  \n")
        
        # Collect images from img folder
        img_folder = os.path.join(snapshot_path, "img")
        if os.path.exists(img_folder) and os.path.isdir(img_folder):
            for img_file in sorted(os.listdir(img_folder)):
                if img_file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    img_path = os.path.relpath(os.path.join(img_folder, img_file), SNAPSHOT_DIR)
                    readme_lines.append(f"![{img_file}]({img_path})\n")
        else:
            readme_lines.append("_No images found_\n")
        
        readme_lines.append("\n---\n")
        
    # Write the README.md
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))

    print(f"README.md generated in /snapshots")

