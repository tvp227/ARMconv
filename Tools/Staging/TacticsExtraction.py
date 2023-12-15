import os
import json
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def extract_tactics(arm_template):
    tactics_list = []

    resources = arm_template.get("resources", [])

    for resource in resources:
        properties = resource.get("properties", {})
        tactics = properties.get("tactics", [])

        tactics_list.extend(tactics)

    return tactics_list

def process_directory(directory_path):
    tactics_count = {}

    for subdir, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(subdir, file)

                with open(file_path, "r") as json_file:
                    arm_template = json.load(json_file)
                    tactics = extract_tactics(arm_template)

                    for tactic in tactics:
                        if tactic in tactics_count:
                            tactics_count[tactic] += 1
                        else:
                            tactics_count[tactic] = 1

    return tactics_count

def load_directory():
    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askdirectory(title="Select Directory Containing JSON Files")

    if directory_path:
        return directory_path
    else:
        print("Directory selection canceled.")
        return None

def write_to_excel(tactics_count, output_file="tactics_summary.xlsx"):
    df = pd.DataFrame(list(tactics_count.items()), columns=["Tactic", "Count"])
    df.to_excel(output_file, index=False)
    print(f"Data written to {output_file}")

def main():
    directory_path = load_directory()

    if directory_path:
        tactics_count = process_directory(directory_path)

        if tactics_count:
            write_to_excel(tactics_count)
        else:
            print("No tactics found in the JSON files.")

if __name__ == "__main__":
    main()
