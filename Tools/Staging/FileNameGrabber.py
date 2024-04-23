import os
import tkinter as tk
from tkinter import filedialog

def list_folders(folder_path):
    try:
        # Get list of all items in the folder
        items = os.listdir(folder_path)
        folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
        if folders:
            print("Folders in '{}' folder:".format(folder_path))
            for folder in folders:
                print(folder)
        else:
            print("No folders found in '{}' folder.".format(folder_path))
    except FileNotFoundError:
        print("Folder '{}' not found.".format(folder_path))
    except PermissionError:
        print("Permission denied for folder '{}'.".format(folder_path))

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        list_folders(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    select_folder()
