import json
import uuid
import tkinter as tk
from tkinter import filedialog

json_conversion_depth = 50

def remove_properties_recursively(resource_obj):
    if isinstance(resource_obj, dict):
        for key, val in list(resource_obj.items()):
            if val is None or (isinstance(val, list) and not val):
                del resource_obj[key]
            else:
                resource_obj[key] = remove_properties_recursively(val)
    elif isinstance(resource_obj, list):
        resource_obj = [remove_properties_recursively(item) for item in resource_obj]
    return resource_obj

def convert_workbooks_to_arm(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            raw_data = file.read()
            # Handle non-ASCII characters (Emoji's)
            data = ''.join(char for char in raw_data if ord(char) < 128)
            json_data = json.loads(data)

            # Extract serializedData from the provided reference
            serialized_data = json_data.get("resources", [{}])[0].get("properties", {}).get("serializedData", {})
            # Remove empty properties
            serialized_data = remove_properties_recursively(serialized_data)
    except Exception as e:
        print(f"Failed to extract serializedData from {input_file_path}: {str(e)}")
        return

    basic_json = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "workspace": {
                "type": "String"
            }
        },
        "resources": []
    }

    # Add formattedTimeNow parameter since workbooks exist
    time_now_parameter = {
        "type": "string",
        "defaultValue": "[utcNow('g')]",
        "metadata": {
            "description": "Appended to workbook displayNames to make them unique"
        }
    }

    basic_json["parameters"]["formattedTimeNow"] = time_now_parameter

    workbook_id = str(uuid.uuid4())
    workbook_id_parameter_name = "workbook-id"
    workbook_name_parameter_name = "workbook-name"
    workbook_id_parameter = {
        "type": "string",
        "defaultValue": workbook_id,
        "minLength": 1,
        "metadata": {
            "description": "Unique id for the workbook"
        }
    }
    workbook_name_parameter = {
        "type": "string",
        "defaultValue": input_file_path.split('/')[-1].split('.')[0],
        "minLength": 1,
        "metadata": {
            "description": "Name for the workbook"
        }
    }

    # Create Workbook Resource Object
    new_workbook = {
        "type": "Microsoft.Insights/workbooks",
        "name": "[parameters('workbook-id')]",
        "location": "[resourceGroup().location]",
        "kind": "shared",
        "apiVersion": "2020-02-12",
        "properties": {
            "displayName": "[concat(parameters('workbook-name'), ' - ', parameters('formattedTimeNow'))]",
            "serializedData":(serialized_data),
            "version": "1.0",
            "sourceId": "[concat(resourceGroup().id, '/providers/Microsoft.OperationalInsights/workspaces/',parameters('workspace'))]",
            "category": "sentinel",
            "etag": "*"
        }
    }

    basic_json["resources"].append(new_workbook)
    basic_json["parameters"][workbook_id_parameter_name] = workbook_id_parameter
    basic_json["parameters"][workbook_name_parameter_name] = workbook_name_parameter

    with open(output_file_path, 'w') as output_file:
        json.dump(basic_json, output_file, indent=4)

def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        output_file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if output_file_path:
            convert_workbooks_to_arm(file_path, output_file_path)
            print(f"Conversion successful. Output saved to: {output_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    select_file()
