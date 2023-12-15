import os
import tkinter as tk
from tkinter import filedialog

def to_camel_case(s):
    words = s.split()
    return ''.join(word.capitalize() for word in words)

def rename_files_to_camel_case(directory):
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        if os.path.isfile(old_path):
            # Extract the file extension
            base, ext = os.path.splitext(filename)
            
            # Rename the file to camel case
            new_filename = to_camel_case(base) + ext
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} -> {new_filename}')

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        rename_files_to_camel_case(directory_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # select a directory
    select_directory()
