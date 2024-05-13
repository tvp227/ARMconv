import os
import json
import tkinter as tk
from tkinter import filedialog

def merge_json_files(directory_path, output_file_name):
    merged_data = []
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    merged_data.extend(data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON file: {file_path}")

    # Write merged data to output file
    with open(output_file_name, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

def select_directory():
    directory_path = filedialog.askdirectory(title="Select Directory")
    if directory_path:
        output_file_name = os.path.join(directory_path, "merged_AnalyticRules.json")
        merge_json_files(directory_path, output_file_name)
        print("JSON files merged successfully.")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    select_directory()

if __name__ == "__main__":
    main()
