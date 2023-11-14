import json
import tkinter as tk
from tkinter import filedialog, simpledialog

# Instructions
instructions = "Please select the JSON file from which you want to extract data. Enter the name of the workbook, and a new JSON file will be created with the provided name."
print(instructions)

# Create a tkinter root window (Silenced)
root = tk.Tk()
root.withdraw()

# GUI wuth fileddiag to select file
file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON Files", "*.json")])

if not file_path:
    print("No file selected. Exiting.")
else:
    # Read the JSON data from the selected file
    with open(file_path, "r") as file:
        json_data = file.read()

    # Parse the JSON data
    data = json.loads(json_data)

    # Grab the 'serializedData' property
    serialized_data = data["resources"][0]["properties"]["serializedData"]

    # Prompt the user for the workbook name
    workbook_name = simpledialog.askstring("Workbook Name", "Enter the name of the workbook:")

    if workbook_name:
        # Load the working template
        template = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "workspace": {
                    "type": "String"
                },
                "formattedTimeNow": {
                    "type": "string",
                    "defaultValue": "[utcNow('g')]",
                    "metadata": {
                        "description": "Appended to workbook displayNames to make them unique"
                    }
                },
                "workbook-id": {
                    "type": "string",
                    "defaultValue": "7a1a0d57-3161-4521-9e76-fdfc04ddc76f",
                    "minLength": 1,
                    "metadata": {
                        "description": "Unique id for the workbook"
                    }
                },
                "workbook-name": {
                    "type": "string",
                    "defaultValue": workbook_name,  # User input variable 
                    "minLength": 1,
                    "metadata": {
                        "description": "Name for the workbook"
                    }
                }
            },
            "resources": [
                {
                    "type": "Microsoft.Insights/workbooks",
                    "name": "[parameters('workbook-id')]",
                    "location": "[resourceGroup().location]",
                    "kind": "shared",
                    "apiVersion": "2020-02-12",
                    "properties": {
                        "displayName": "[concat(parameters('workbook-name'), ' - ', parameters('formattedTimeNow'))]",
                        "serializedData": serialized_data,  # Replace the value here
                        "version": "1.0",
                        "sourceId": "[concat(resourceGroup().id, '/providers/Microsoft.OperationalInsights/workspaces/',parameters('workspace'))]",
                        "category": "sentinel",
                        "etag": "*"
                    }
                }
            ]
        }

        # Create a new file in the same directory with workbook name 
        new_file_path = rf"{workbook_name}_workbook.json"

        with open(new_file_path, "w") as new_file:
            json.dump(template, new_file, indent=4)

        print(f"New JSON file saved as '{new_file_path}' with the workbook name: {workbook_name}")

    else:
        print("No workbook name entered. Exiting.")
