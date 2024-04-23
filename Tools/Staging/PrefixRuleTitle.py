import os
import json
import tkinter as tk
from tkinter import filedialog

RulePrefixTitle = "tom is cool" # Add you prefix here. Remember to add "-" at the end if you want it to be spaced

def process_json_files(folder_path):
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            # Load the JSON file
            with open(os.path.join(folder_path, filename), 'r') as file:
                arm_template = json.load(file)

            # Iterate over each resource in the "resources" array
            for resource in arm_template['resources']:
                # Check if the resource has a "properties" object
                if 'properties' in resource and 'displayName' in resource['properties']:
                    # Append "Entra-" to the beginning of the display name
                    resource['properties']['displayName'] = f"{RulePrefixTitle}{resource['properties']['displayName']}"

            # Write the modified ARM template back to the file
            with open(os.path.join(folder_path, filename), 'w') as file:
                json.dump(arm_template, file, indent=4)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_json_files(folder_path)
        print("Display names have been modified in all JSON files within the selected folder.")

# Create a Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Ask the user to select a folder
select_folder()
