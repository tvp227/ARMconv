import os
import json
import tkinter as tk
from tkinter import filedialog

def merge_arm_templates(directory):
    merged_template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {},
        "resources": []
    }

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r") as file:
                    template = json.load(file)
                    merged_template["resources"].extend(template["resources"])

    return merged_template

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory = filedialog.askdirectory(title="Select ARM Template Directory")
    if directory:
        return directory
    else:
        print("No directory selected.")
        return None

def main():
    directory = select_directory()
    if directory:
        merged_template = merge_arm_templates(directory)
        with open("merged_template.json", "w") as output_file:
            json.dump(merged_template, output_file, indent=4)
        print("ARM templates merged successfully.")

if __name__ == "__main__":
    main()
