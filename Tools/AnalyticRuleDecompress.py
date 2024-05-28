import os
import json
import tkinter as tk
from tkinter import filedialog

def extract_rules(template_file):
    output_folder = "Decompressed rules"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(template_file, "r") as file:
        template = json.load(file)
        resources = template.get("resources", [])

        for resource in resources:
            display_name = resource.get("properties", {}).get("displayName", "")
            if display_name:
                filename = display_name.replace(" ", "_") + ".json"
                output_path = os.path.join(output_folder, filename)
                with open(output_path, "w") as output_file:
                    json.dump(resource, output_file, indent=4)
                print(f"Rule '{display_name}' extracted to '{output_path}'.")

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Select ARM Template JSON File", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if file_path:
        return file_path
    else:
        print("No file selected.")
        return None

def main():
    template_file = select_file()
    if template_file:
        extract_rules(template_file)

if __name__ == "__main__":
    main()
