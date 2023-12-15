import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  
import subprocess

def process_json_file(file_path, tree, parent, missing_title_count, missing_description_count):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            metadata = data.get('metadata', {})
            title = metadata.get('title', '').strip()
            description = metadata.get('description', '').strip()
            
            if not title:
                missing_title_count[0] += 1
                tree.insert(parent, 'end', text=f"{file_path} - Missing Title")
                
            if not description:
                missing_description_count[0] += 1
                tree.insert(parent, 'end', text=f"{file_path} - Missing Description")
                
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")

def process_folder(folder_path, tree):
    missing_title_count = [0]
    missing_description_count = [0]
    
    for root, dirs, files in os.walk(folder_path):
        parent = tree.insert('', 'end', text=root, open=True)
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_json_file(file_path, tree, parent, missing_title_count, missing_description_count)
    
    print(f"Total Playbooks Missing or Empty Title: {missing_title_count[0]}")
    print(f"Total Playbooks Missing or Empty Description: {missing_description_count[0]}")

def browse_playbook():
   folder_path = filedialog.askdirectory(title="Select Folder with JSON Files")
   if folder_path:
       # Create the main window
       root = tk.Tk()
       root.title("Missing Titles and Descriptions")

       # Create a Treeview widget
       tree = ttk.Treeview(root)
       tree.heading('#0', text='Missing Titles and Descriptions')
       tree.pack(expand=True, fill='both')

       # Process the folder and update the tree
       process_folder(folder_path, tree)

       # Run the Tkinter event loop
       root.mainloop()

# Run the Tkinter event loop
root = tk.Tk()
root.withdraw()  
# Prompt user to select folder with JSON files
browse_playbook()
