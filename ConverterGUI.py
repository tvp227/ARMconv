import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import subprocess

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
def display_results_on_treeview(directory, tree):
    json_count, schema_count = count_json_files(directory)

    # Clear existing items in the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert new items in the treeview for JSON file count
    for category, count in json_count.items():
        tree.insert("", "end", values=[category, count])

    # Insert new items in the treeview for schema count
    for schema, count in schema_count.items():
        tree.insert("", "end", values=[schema, count])

class MyGUI:
    def __init__(self, master):
        # GUI initialization method
        self.master = master
        master.title("ARM Templating Tool")
        master.geometry("800x600")
        master.resizable(False, False)

        # Use a Frame to hold the background image
        self.background_frame = ttk.Frame(master)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.background_image = Image.open("Prereqs/Background.png")
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.background_frame, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a label with the title
        title_label = ttk.Label(master, text="ARM Templating Tool", font=("Helvetica", 16))
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # Create a label with the author
        author_label = ttk.Label(master, text="By Tom Porter", font=("Helvetica", 10))
        author_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Create a custom style for the buttons
        style = ttk.Style()
        style.theme_use("clam")

        # Configure general button style
        style.configure("TButton",
                        font=("Helvetica", 10),
                        padding=5,
                        background="#4CAF50",  # Green background
                        foreground="white"  # White text
                        )

        # Configure exit button style separately
        style.configure("Exit.TButton",
                        font=("Helvetica", 10),
                        padding=5,
                        background="#FF5733",  # Red background
                        foreground="white"  # White text
                        )

        # Create buttons using the custom style
        button_spacing = 0.1
        button_y = 0.25

        self.convert_playbook_button = ttk.Button(master, text="Convert Playbook", command=self.launch_playbook_application, style="TButton")
        self.convert_playbook_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing

        self.convert_workbook_button = ttk.Button(master, text="Convert Workbook", command=self.launch_workbook_application, style="TButton")
        self.convert_workbook_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing

        self.convert_KQL_button = ttk.Button(master, text="Convert KQL", command=self.launch_KQL_application, style="TButton")
        self.convert_KQL_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing

        self.convert_DCAR_button = ttk.Button(master, text="Document Creator AR", command=self.launch_DCAR_application, style="TButton")
        self.convert_DCAR_button.place(relx=0.1, rely=button_y, anchor=tk.W)
        button_y += button_spacing

        self.convert_DCPB_button = ttk.Button(master, text="Document Creator PB", command=self.launch_DCPB_application, style="TButton")
        self.convert_DCPB_button.place(relx=0.1, rely=button_y, anchor=tk.W)

        # Create an Entry widget to display the selected folder_path
        self.folder_path_var = tk.StringVar()
        self.folder_path_entry = ttk.Entry(master, textvariable=self.folder_path_var, state='readonly', font=("Helvetica", 10))
        self.folder_path_entry.place(relx=0.815, rely=0.65, anchor=tk.CENTER)

        # Create a Browse button to select the folder_path
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_folder, style="TButton")
        self.browse_button.place(relx=0.78, rely=0.7, anchor=tk.CENTER)

        # Create an exit button
        self.exit_button = ttk.Button(master, text="Exit", command=master.destroy, style="Exit.TButton")
        self.exit_button.place(relx=0.1, rely=0.8, anchor=tk.W)

        # Create a treeview to display JSON file count information
        self.tree = ttk.Treeview(master, columns=("Category", "Count"), show="headings", height=10)

        # Configure column headings
        self.tree.heading("Category", text="Category", anchor=tk.CENTER)
        self.tree.heading("Count", text="Count", anchor=tk.CENTER)

        # Configure treeview style
        style.configure("Treeview",
                        background="#D3D3D3",  # Light gray background
                        fieldbackground="#D3D3D3"  # Light gray background for entry widgets
                        )

        # Configure treeview column style
        style.configure("Treeview.Heading",
                        font=("Helvetica", 10, "bold"),
                        background="#696969",  # Dim gray background for column headings
                        foreground="white"  # White text for column headings
                        )

        # Configure treeview item style
        style.map("Treeview",
                  background=[("selected", "#347083")],  # Darker color when selected
                  foreground=[("selected", "white")]
                  )

        # Place the treeview
        self.tree.place(relx=0.295, rely=0.42, anchor=tk.W, width=530, height=250)

        # Create a vertical scrollbar
       ## tree_scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
       ## tree_scrollbar.place(relx=0.9, rely=0.37, anchor=tk.E, height=200)                ## Cant get scroll bar working propely 
        # Configure treeview to use the scrollbar
       ## self.tree.configure(yscrollcommand=tree_scrollbar.set)

        # Create a button to refresh the JSON file count information
        self.refresh_button = ttk.Button(master, text="Refresh", command=self.refresh_json_count, style="TButton")
        self.refresh_button.place(relx=0.92, rely=0.7, anchor=tk.CENTER)

        # Display the initial JSON file count information
        self.refresh_json_count()

    # Launchers
    def launch_playbook_application(self):
        # Function to launch the Playbook application
        subprocess.run(["python", "Tools/PlayBookConv.py"])

    def launch_workbook_application(self):
        # Function to launch the Workbook application
        subprocess.run(["python", "Tools/WorkBookConv.py"])

    def launch_KQL_application(self):
        # Function to launch the KQL application
        subprocess.run(["python", "Tools/KQLConv.py"])

    def launch_DCAR_application(self):
        # Function to launch the Document Creator AR application
        subprocess.run(["python", "Tools/DocumentCreatorAR.py"])

    def launch_DCPB_application(self):
        # Function to launch the Document Creator PB application
        subprocess.run(["python", "Tools/DocumentCreatorPB.py"])

    def browse_folder(self):
        # Function to allow the user to select a folder and set the selected folder_path
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)
            self.refresh_json_count()

    def refresh_json_count(self):
        # Function to refresh the JSON file count information
        # Get the folder_path from the Entry widget
        folder_path = self.folder_path_var.get()

        # Check if folder_path is not empty before proceeding
        if folder_path:
            # Use the get_json_schemas function to count schemas
            schema_count = get_json_schemas(folder_path)

            # Use the count_json_files function to count JSON files
            json_count, _ = count_json_files(folder_path)

            # Clear existing items in the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new items in the treeview for JSON file count
            for category, count in json_count.items():
                self.tree.insert("", "end", values=[category, count])

            # Insert new items in the treeview for schema count
            for schema, count in schema_count.items():
                self.tree.insert("", "end", values=[schema, count])

if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()
