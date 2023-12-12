import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class JsonFileUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON File Updater")

        self.folder_path = tk.StringVar()
        self.json_files = []
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        # Select Folder Button
        select_folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        select_folder_button.pack(pady=10)

        # Display JSON File Information
        self.display_label = tk.Label(self.root, text="")
        self.display_label.pack(pady=10)

        # Treeview to display JSON files
        self.tree = ttk.Treeview(self.root, selectmode="extended", columns=("DisplayName", "Enabled"))
        self.tree.heading("DisplayName", text="Display Name")
        self.tree.heading("Enabled", text="Enabled")
        self.tree.pack(pady=10)

        # Change Enabled Status Button for selected rules
        change_enabled_button = tk.Button(self.root, text="Change Selected Enabled Status", command=self.change_selected_enabled_status)
        change_enabled_button.pack(pady=10)

        # Quit Button
        quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.pack(pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.scan_json_files()

    def scan_json_files(self):
        self.json_files = []
        self.tree.delete(*self.tree.get_children())  

        for root, dirs, files in os.walk(self.folder_path.get()):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    self.json_files.append(file_path)

                    with open(file_path, "r") as file:
                        json_data = json.load(file)
                        display_name = json_data["resources"][0]["properties"]["displayName"]
                        enabled_status = json_data["resources"][0]["properties"]["enabled"]

                    self.tree.insert("", "end", values=(display_name, enabled_status), iid=file_path)

        if not self.json_files:
            messagebox.showinfo("No JSON Files", "No JSON files found in the selected folder.")
            return

        self.current_index = 0
        self.display_json_info()

    def display_json_info(self):
        if self.json_files:
            current_file = self.json_files[self.current_index]
            with open(current_file, "r") as file:
                json_data = json.load(file)

            display_name = json_data["resources"][0]["properties"]["displayName"]
            enabled_status = json_data["resources"][0]["properties"]["enabled"]

            self.display_label.config(text=f"Display Name: {display_name}\nEnabled: {enabled_status}")

    def change_selected_enabled_status(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "No rules selected. Please select one or more rules.")
            return

        for item in selected_items:
            with open(item, "r") as file:
                json_data = json.load(file)

            new_enabled_status = not json_data["resources"][0]["properties"]["enabled"]
            json_data["resources"][0]["properties"]["enabled"] = new_enabled_status

            with open(item, "w") as file:
                json.dump(json_data, file, indent=4)

            self.tree.item(item, values=(json_data["resources"][0]["properties"]["displayName"], new_enabled_status))

        messagebox.showinfo("Updated", f"Enabled status updated for selected rules.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonFileUpdater(root)
    root.mainloop()
