import json
import os
from tkinter import filedialog
import tkinter as tk

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def segment_json(file_path):
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the list of automation rules
    automation_rules = data.get("value", [])

    # Check if the data is a list of objects
    if isinstance(automation_rules, list):
        # Create the output directory if it doesn't exist
        output_directory = "DecompressedAutoRules"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        for item in automation_rules:
            # Extract the displayName to use as the file name
            display_name = item.get("properties", {}).get("displayName", "unknown")

            # Sanitize the display name to be a valid file name
            display_name = display_name.replace(" ", "_").replace("/", "_")

            # Write each JSON object to a separate file named by the display name
            with open(os.path.join(output_directory, f"{display_name}.json"), 'w') as output_file:
                json.dump(item, output_file, indent=4)
    else:
        print("The 'value' key does not contain a list of objects")

# Use Tkinter to select the input JSON file
input_file_path = select_file()

# Segment the JSON payloads
if input_file_path:
    segment_json(input_file_path)
