import json
import tkinter as tk
from tkinter import filedialog

def extract_id_and_properties(json_data):
    id_number = json_data.get("name")
    if id_number:
        id_number = id_number.split("/")[-1]  # Extracting only the UUID part
    properties = json_data.get("properties", {})
    return id_number, properties

def select_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            json_data = json.load(file)
            id_number, properties = extract_id_and_properties(json_data)
            generate_template(id_number, properties)

def generate_template(id_number, properties):
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
    print(json.dumps(template, indent=4))

# Create Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Select JSON file using file dialog
select_json_file()
