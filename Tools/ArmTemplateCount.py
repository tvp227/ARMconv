import os
import tkinter as tk
from tkinter import filedialog
def count_json_files(folder_path):
   json_count = 0
   for root, dirs, files in os.walk(folder_path):
       for file in files:
           if file.endswith(".json"):
               json_count += 1
   return json_count
def select_folder():
   folder_path = filedialog.askdirectory()
   if folder_path:
       result = count_json_files(folder_path)
       print(f"The number of JSON files in {folder_path} and its subfolders is: {result}")
# Create the main window
window = tk.Tk()
window.title("JSON File Counter")
# Hide the main window
window.withdraw()
# Automatically open file dialog upon running
select_folder()
# Destroy the main window
window.destroy()