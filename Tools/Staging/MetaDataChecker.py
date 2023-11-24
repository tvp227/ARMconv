import os
import json
import tkinter as tk
from tkinter import filedialog
import subprocess

def process_json_file(file_path, missing_title_count, missing_description_count):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            metadata = data.get('metadata', {})
            title = metadata.get('title', '').strip()
            description = metadata.get('description', '').strip()
            
            if not title:
                missing_title_count[0] += 1
                
            if not description:
                missing_description_count[0] += 1
                
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

def process_folder(folder_path):
    missing_title_count = [0]
    missing_description_count = [0]
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_json_file(file_path, missing_title_count, missing_description_count)
    
    print(f"Total Playbooks Missing or Empty Title: {missing_title_count[0]}")
    print(f"Total Playbooks Missing or Empty Description: {missing_description_count[0]}")

def browse_playbook():
   folder_path = filedialog.askdirectory(title="Select Folder with JSON Files")
   if folder_path:
       playbooks_data = process_folder(folder_path)

# Run the Tkinter event loop
root = tk.Tk()
root.withdraw()  
# Prompt user to select folder with JSON files
browse_playbook()

