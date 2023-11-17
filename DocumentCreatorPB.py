import json
import tkinter as tk
from tkinter import filedialog
import os

def get_last_segment(id_path):
    return id_path.split("/")[-1]

def get_connection_ids(json_data):
    connection_ids = []

    def traverse(obj):
        if isinstance(obj, dict):
            if "$connections" in obj:
                value = obj["$connections"].get("value")
                if value and isinstance(value, dict):
                    for connection_key, connection_value in value.items():
                        if isinstance(connection_value, dict) and "id" in connection_value:
                            connection_id = get_last_segment(connection_value["id"])
                            connection_ids.append(connection_id)
            for key, value in obj.items():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(json_data)
    return connection_ids

def process_playbooks(files):
    playbooks_data = {}
    for file_path in files:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                if 'metadata' in data and 'title' in data['metadata']:
                    title = data['metadata']['title']
                    description = data['metadata']['description'] if 'description' in data['metadata'] else 'N/A'
                    connection_ids = get_connection_ids(data)
                    playbooks_data[title] = {'title': title, 'description': description, 'connection_ids': connection_ids}
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {file_path}")

    return playbooks_data

def generate_playbooks_readme_md(playbooks_data):
    readme_content = "# Sentinel Playbooks Documentation\n\n"
    readme_content += "| **Playbook Title** | **Description** | **Connector IDs** |\n"
    readme_content += "|---------------------|-----------------|-------------------|\n"

    for title, details in playbooks_data.items():
        # Keep the original formatting for the title and description
        original_title = details['title']
        original_description = details['description']
        connection_ids = details['connection_ids']

        # Replace line breaks and double quotes in the displayed title and description
        formatted_title = original_title.replace('\n', '\\r\\n').replace('"', '\\"')
        formatted_description = original_description.replace('\n', '\\r\\n').replace('"', '\\"')
        formatted_connection_ids = ", ".join(connection_ids)
        readme_content += f"| **{formatted_title}** | {formatted_description} | {formatted_connection_ids} |\n"

    with open("readme.md", "w") as readme_file:
        readme_file.write(readme_content)

def browse_playbooks():
    files = filedialog.askopenfilenames(
        title="Select Playbook JSON Files",
        filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
    )
    if files:
        playbooks_data = process_playbooks(files)
        generate_playbooks_readme_md(playbooks_data)
        print("readme.md generated successfully.")

# Run the Tkinter event loop
root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt user to select playbook files
browse_playbooks()
