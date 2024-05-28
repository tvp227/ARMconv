import json
import os

def segment_json(file_path):
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the list of automation rules
    automation_rules = data.get("value", [])

    # Check if the data is a list of objects
    if isinstance(automation_rules, list):
        for item in automation_rules:
            # Extract the displayName to use as the file name
            display_name = item.get("properties", {}).get("displayName", "unknown")

            # Sanitize the display name to be a valid file name
            display_name = display_name.replace(" ", "_").replace("/", "_")

            # Write each JSON object to a separate file named by the display name
            with open(f"{display_name}.json", 'w') as output_file:
                json.dump(item, output_file, indent=4)
    else:
        print("The 'value' key does not contain a list of objects")

# Path to the input JSON file
input_file_path = r"C:\Users\ThomasPorter\Downloads\autorules.json"

# Segment the JSON payloads
segment_json(input_file_path)
