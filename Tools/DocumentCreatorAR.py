import json
import tkinter as tk
from tkinter import filedialog

def process_files(files):
    rules_data = {}
    for file_path in files:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                if 'resources' in data and isinstance(data['resources'], list):
                    for resource in data['resources']:
                        if 'properties' in resource and 'displayName' in resource['properties']:
                            title = resource['properties']['displayName']
                            description = resource['properties']['description'] if 'description' in resource['properties'] else 'N/A'
                            rules_data[title] = {'title': title, 'description': description}
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {file_path}")

    return rules_data

def generate_readme_md(rules_data):
    readme_content = "# Sentinel Rules Documentation\n\n"
    readme_content += "| **Rule Title** | **Description** |\n"
    readme_content += "|----------------|-----------------|\n"

    for title, details in rules_data.items():
        # Keep the original formatting for the title and description
        original_title = details['title']
        original_description = details['description']
        
        # Replace line breaks and double quotes in the displayed title and description
        formatted_title = original_title.replace('\n', '\\r\\n').replace('"', '\\"')
        formatted_description = original_description.replace('\n', '\\r\\n').replace('"', '\\"')
        readme_content += f"| **{formatted_title}** | {formatted_description} |\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

def browse_AnalyticRules():
    files = filedialog.askopenfilenames(
        title="Select Playbook JSON Files",
        filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
    )
    if files:
        playbooks_data = process_files(files)
        generate_readme_md(playbooks_data)
        print("readme.md generated successfully.")

# Run the Tkinter event loop
root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt user to select playbook files
browse_AnalyticRules()
