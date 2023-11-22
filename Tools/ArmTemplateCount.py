import os
import tkinter as tk
from tkinter import filedialog

def count_json_files(folder_path):
    json_count = {'Detections': 0, 'Hunting': 0, 'Playbooks': 0, 'Workbooks': 0, 'Total': 0}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                json_count['Total'] += 1

                # Categorize based on subdirectories
                subdirectory = os.path.relpath(root, folder_path)
                if subdirectory.startswith('Detections'):
                    json_count['Detections'] += 1
                elif subdirectory.startswith('Hunting'):
                    json_count['Hunting'] += 1
                elif subdirectory.startswith('Playbooks'):
                    json_count['Playbooks'] += 1
                elif subdirectory.startswith('Workbooks'):
                    json_count['Workbooks'] += 1

    return json_count

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        result = count_json_files(folder_path)
        print(f"Number of JSON files in {folder_path}:")
        print(f"Detections: {result['Detections']}")
        print(f"Hunting: {result['Hunting']}")
        print(f"Playbooks: {result['Playbooks']}")
        print(f"Workbooks: {result['Workbooks']}")
        print(f"Total: {result['Total']}")

# Create the main window
window = tk.Tk()
window.title("ARM Template Counter")

# Hide the main window
window.withdraw()

# Automatically open file dialog upon running
select_folder()

# Destroy the main window
window.destroy()
