import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog

def rename_json_files(folder_path):
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    # Get the displayName from the JSON structure if available
                    display_name = data.get('resources', [{}])[0].get('properties', {}).get('displayName')
                    if display_name:
                        # Construct the new file name
                        new_filename = display_name + '.json'
                        new_file_path = os.path.join(folder_path, new_filename)
                        # Make a copy of the file with the correct name
                        shutil.copyfile(file_path, new_file_path)
                        print(f'Copied {filename} to {new_filename}')
                    else:
                        print(f'No displayName found in {filename}. File not renamed.')
                except json.JSONDecodeError:
                    print(f'Error decoding JSON in {filename}. File not renamed.')

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if folder_path:
        rename_json_files(folder_path)

select_folder()
