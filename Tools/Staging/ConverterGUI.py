import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import subprocess
from datetime import datetime

# Function to retrieve JSON schemas from a directory
def get_json_schemas(directory):
    schema_count = {}

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Check if the JSON has the "$schema" property
                        if "$schema" in data:
                            schema = data["$schema"]
                            schema_count[schema] = schema_count.get(schema, 0) + 1
                except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
                    pass

    return schema_count

# Function to retrieve JSON metadata from a directory
def get_json_metadata(directory):
    metadata_info = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                try:
                    # Get file creation and modification dates
                    created_time = os.path.getctime(file_path)
                    modified_time = os.path.getmtime(file_path)

                    created_date = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
                    modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')

                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Extract metadata information
                        metadata = {
                            'File Name': file_name,
                            'Creation Date': created_date,
                            'Modified Date': modified_date,
                            # Add more metadata fields as needed
                        }

                        metadata_info.append(metadata)
                except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
                    pass

    return metadata_info

# Function to count JSON files in the specified folder_path
def count_json_files(directory):
    json_count = {'Detections': 0, 'Hunting': 0, 'Playbooks': 0, 'Workbooks': 0, 'Total': 0}
    schema_count = {}

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Count based on subdirectories
                        subdirectory = os.path.relpath(root, directory)
                        json_count['Total'] += 1
                        if subdirectory.startswith('Detections'):
                            json_count['Detections'] += 1
                        elif subdirectory.startswith('Hunting'):
                            json_count['Hunting'] += 1
                        elif subdirectory.startswith('Playbooks'):
                            json_count['Playbooks'] += 1
                        elif subdirectory.startswith('Workbooks'):
                            json_count['Workbooks'] += 1

                        # Check if the JSON has the "$schema" property
                        if "$schema" in data:
                            schema = data["$schema"]
                            schema_count[schema] = schema_count.get(schema, 0) + 1
                except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
                    pass

    return json_count, schema_count

# Function to display JSON file and schema count information in the treeview
def display_results_on_treeview(directory, tree_json_count, tree_schema_count, tree_metadata_count):
    json_count, schema_count = count_json_files(directory)
    metadata_info = get_json_metadata(directory)

    # Clear existing items in the first treeview (JSON file count)
    for item in tree_json_count.get_children():
        tree_json_count.delete(item)

    # Clear existing items in the second treeview (schema count)
    for item in tree_schema_count.get_children():
        tree_schema_count.delete(item)

    # Clear existing items in the third treeview (metadata count)
    for item in tree_metadata_count.get_children():
        tree_metadata_count.delete(item)

    # Insert new items in the first treeview for JSON file count
    for category, count in json_count.items():
        tree_json_count.insert("", "end", values=[category, count])

    # Insert new items in the second treeview for schema count
    for schema, count in schema_count.items():
        tree_schema_count.insert("", "end", values=[schema, count])

    # Insert new items in the third treeview for metadata count
    for metadata in metadata_info:
        tree_metadata_count.insert("", "end", values=[metadata['File Name'], metadata['Creation Date'], metadata['Modified Date']])

#GUI config
class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sentinel DevOps Tooling")
        master.geometry("950x500")
        master.resizable(False, False)

        # Use a Frame to hold the background image
        self.background_frame = ttk.Frame(master)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Background image
        self.background_image = Image.open("Prereqs/Background.png")
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.background_frame, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #Titles
        title_label = ttk.Label(master, text="Sentinel DevOps Tooling", font=("Helvetica", 16))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        author_label = ttk.Label(master, text="By Tom Porter", font=("Helvetica", 10))
        author_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        #Styling
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Helvetica", 10),
                        padding=5,
                        background="black",
                        foreground="white"
                        )
        style.configure("PS.TButton",
                        font=("Helvetica", 10),
                        padding=5,
                        background="blue2",
                        foreground="white"
                        )

        style.configure("Exit.TButton",
                        font=("Helvetica", 10),
                        padding=5,
                        background="red",
                        foreground="white"
                        )

        button_spacing = 0.1
        button_y = 0.25

        # Convert Playbook
        self.convert_playbook_button = ttk.Button(master, text="Convert Playbook", command=self.launch_playbook_application, style="TButton")
        self.convert_playbook_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # Convert Workbook
        self.convert_workbook_button = ttk.Button(master, text="Convert Workbook", command=self.launch_workbook_application, style="TButton")
        self.convert_workbook_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # Convert KQL button
        self.convert_KQL_button = ttk.Button(master, text="Convert KQL", command=self.launch_KQL_application, style="TButton")
        self.convert_KQL_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # Document Creator AR button
        self.convert_DCAR_button = ttk.Button(master, text="Document Creator AR", command=self.launch_DCAR_application, style="TButton")
        self.convert_DCAR_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # Document Creator PB button
        self.convert_DCPB_button = ttk.Button(master, text="Document Creator PB", command=self.launch_DCPB_application, style="TButton")
        self.convert_DCPB_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # PS Button
        self.convert_PS1_button = ttk.Button(master, text="AzureCLI", command=self.launch_PS1_application, style="PS.TButton")
        self.convert_PS1_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing
        # Dir Display Box
        self.folder_path_var = tk.StringVar()
        self.folder_path_entry = ttk.Entry(master, textvariable=self.folder_path_var, state='readonly', font=("Helvetica", 10))
        self.folder_path_entry.place(relx=0.86, rely=0.18, anchor=tk.CENTER)
        # Browse Button
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_folder, style="TButton")
        self.browse_button.place(relx=0.8, rely=0.95, anchor=tk.CENTER)
        # Refresh Button
        self.refresh_button = ttk.Button(master, text="Refresh", command=self.refresh_json_count, style="TButton")
        self.refresh_button.place(relx=0.9, rely=0.95, anchor=tk.CENTER)
        self.refresh_json_count()
        # Exit Button
        self.exit_button = ttk.Button(master, text="Exit", command=master.destroy, style="Exit.TButton")
        self.exit_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing

        # Tree styling
        style.configure("Treeview",
                        background="white",
                        fieldbackground="grey"
                        )

        style.configure("Treeview.Heading",
                        font=("Helvetica", 10, "bold"),
                        background="black",
                        foreground="white"
                        )

        style.map("Treeview",
                  background=[("selected", "grey4")],
                  foreground=[("selected", "white")]
                  )
        # Json Count Tree
        self.tree_json_count = ttk.Treeview(master, columns=("Category", "Count"), show="headings", height=5)

        self.tree_json_count.heading("Category", text="Category", anchor=tk.CENTER)
        self.tree_json_count.heading("Count", text="Count", anchor=tk.CENTER)

        self.tree_json_count.place(relx=0.295, rely=0.32, anchor=tk.W, width=650, height=120)
        # Schema Count Tree
        self.tree_schema_count = ttk.Treeview(master, columns=("Schema", "Count"), show="headings", height=5)

        self.tree_schema_count.heading("Schema", text="Schema", anchor=tk.CENTER)
        self.tree_schema_count.heading("Count", text="Count", anchor=tk.CENTER)

        self.tree_schema_count.place(relx=0.295, rely=0.55, anchor=tk.W, width=650, height=120)
        # Meta Data Tree
        self.tree_MetaData_count = ttk.Treeview(master, columns=("File Name", "Creation Date", "Modified Date"), show="headings", height=5)

        self.tree_MetaData_count.heading("File Name", text="File Name", anchor=tk.CENTER)
        self.tree_MetaData_count.heading("Creation Date", text="Creation Date", anchor=tk.CENTER)
        self.tree_MetaData_count.heading("Modified Date", text="Modified Date", anchor=tk.CENTER)

        self.tree_MetaData_count.place(relx=0.295, rely=0.79, anchor=tk.W, width=650, height=120)

    # Launchers
    def launch_playbook_application(self):
        subprocess.run(["python", "Tools/PlayBookConv.py"])

    def launch_workbook_application(self):
        subprocess.run(["python", "Tools/WorkBookConv.py"])

    def launch_KQL_application(self):
        subprocess.run(["python", "Tools/KQLConv.py"])

    def launch_DCAR_application(self):
        subprocess.run(["python", "Tools/DocumentCreatorAR.py"])

    def launch_DCPB_application(self):
        subprocess.run(["python", "Tools/DocumentCreatorPB.py"])

    def launch_PS1_application(self):
        subprocess.run(["powershell", "Powershell/Playbook_ARM_Template_Generator.ps1"])

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)
            self.refresh_json_count()

    def refresh_json_count(self):
        folder_path = self.folder_path_var.get()

        if folder_path:
            schema_count = get_json_schemas(folder_path)
            json_count, _ = count_json_files(folder_path)
            metadata_info = get_json_metadata(folder_path)

            # Clear existing items in the treeviews
            for item in self.tree_json_count.get_children():
                self.tree_json_count.delete(item)

            for item in self.tree_schema_count.get_children():
                self.tree_schema_count.delete(item)

            for item in self.tree_MetaData_count.get_children():
                self.tree_MetaData_count.delete(item)

            # Insert new items in the treeview for JSON file count
            for category, count in json_count.items():
                self.tree_json_count.insert("", "end", values=[category, count])

            # Insert new items in the treeview for schema count
            for schema, count in schema_count.items():
                self.tree_schema_count.insert("", "end", values=[schema, count])

            # Insert new items in the treeview for metadata count
            for metadata in metadata_info:
                self.tree_MetaData_count.insert("", "end", values=[metadata['File Name'], metadata['Creation Date'], metadata['Modified Date']])


if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()
