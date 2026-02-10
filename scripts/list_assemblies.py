import json

def load_elements_json(elements_file_path):
    """
    Load elements.json from disk and return it as a Python object.
    """
    with open(elements_file_path, "r") as f:
        return json.load(f)

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


# -----
# MAIN
# -----

elements = load_elements_json(
    "snapshots/20260209_120527/elements.json"
)

assemblies = extract_assemblies(elements)

print(f"Found {len(assemblies)} assembly(s):")
for assembly in assemblies:
    print(f"- {assembly['name']} ({assembly['id']})")

