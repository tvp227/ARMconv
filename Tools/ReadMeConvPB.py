import os
import json
import tkinter as tk
from tkinter import filedialog

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

def process_playbooks(folder_path):
    playbooks_data = {}
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                        if 'metadata' in data and 'title' in data['metadata']:
                            title = data['metadata']['title']
                            description = data['metadata'].get('description', 'N/A')
                            connection_ids = get_connection_ids(data)
                            playbooks_data[title] = {'title': title, 'description': description, 'connection_ids': connection_ids}
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")
    return playbooks_data

def generate_playbooks_readme_md(playbooks_data):
    readme_content = "# Playbook Readme\n\n"
    readme_content += "| **Playbook Title** | **Description** | **Connector IDs** |\n"
    readme_content += "|---------------------|-----------------|-------------------|\n"
    for title, details in playbooks_data.items():
        formatted_title = details['title'].replace('\n', ' ').replace('|', '-')
        formatted_description = details['description'].replace('\n', ' ').replace('|', '-')
        formatted_connection_ids = ", ".join(details['connection_ids'])
        readme_content += f"| {formatted_title} | {formatted_description} | {formatted_connection_ids} |\n"
    with open("playbook_readme.md", "w") as readme_file:
        readme_file.write(readme_content)

def browse_playbooks():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder with Playbook JSON Files")
    if folder_path:
        playbooks_data = process_playbooks(folder_path)
        if playbooks_data:
            generate_playbooks_readme_md(playbooks_data)
            print("playbook_readme.md generated successfully.")
        else:
            print("No valid playbook JSON files found.")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    browse_playbooks()
