import json
import os
import tkinter as tk
from tkinter import filedialog

def extract_id_and_properties(json_data):
    id_number = json_data.get("name")
    if id_number:
        id_number = id_number.split("/")[-1]  # Extracting only the UUID part
    properties = json_data.get("properties", {})
    return id_number, properties

def select_json_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("JSON files", "*.json")])
    if file_paths:
        for file_path in file_paths:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                id_number, properties = extract_id_and_properties(json_data)
                generate_template(id_number, properties, file_path)

def generate_template(id_number, properties, file_path):
    template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "workspace": {
                "type": "String"
            }
        },
        "resources": [
            {
                "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/automationRules/', '{}')]".format(id_number),
                "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/', '{}')]".format(id_number),
                "type": "Microsoft.OperationalInsights/workspaces/providers/automationRules",
                "kind": "Scheduled",
                "apiVersion": "2019-01-01-preview",
                "properties": properties
            }
        ]
    }
    folder_name = "TemplatedAutoRules"
    os.makedirs(folder_name, exist_ok=True)
    output_file_path = os.path.join(folder_name, os.path.basename(file_path) + "_template.json")
    with open(output_file_path, "w") as output_file:
        json.dump(template, output_file, indent=4)
    print(f"Template generated and saved to: {output_file_path}")

# Create Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Select JSON files using file dialog
select_json_files()
