import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import subprocess

def count_json_files(folder_path):
    # Function to count JSON files in the specified folder_path
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

def display_results_on_treeview(folder_path, tree):
    # Function to display JSON file count information in the treeview
    result = count_json_files(folder_path)

    # Clear existing items in the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert new items in the treeview
    tree.insert("", "end", values=["Detections", result['Detections']])
    tree.insert("", "end", values=["Hunting", result['Hunting']])
    tree.insert("", "end", values=["Playbooks", result['Playbooks']])
    tree.insert("", "end", values=["Workbooks", result['Workbooks']])
    tree.insert("", "end", values=["Total", result['Total']])

class MyGUI:
    def __init__(self, master):
        # GUI initialization method
        self.master = master
        master.title("ARM Templating Tool")
        master.geometry("680x380")
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
                        background="black",  
                        foreground="white"  
                        )

        # Configure exit button style separately
        style.configure("Exit.TButton",
                        font=("Helvetica", 10),
                        padding=5,  
                        background="red",  
                        foreground="white"  
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
        self.folder_path_entry = ttk.Entry(master, textvariable=self.folder_path_var, state='readonly')
        self.folder_path_entry.place(relx=0.92, rely=0.5, anchor=tk.CENTER)

        # Create a Browse button to select the folder_path
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.place(relx=0.92, rely=0.55, anchor=tk.CENTER)

        # Create an exit button
        self.exit_button = ttk.Button(master, text="Exit", command=master.destroy, style="Exit.TButton")
        self.exit_button.place(relx=0.1, rely=0.9, anchor=tk.W)

        # Create a treeview to display JSON file count information
        self.tree = ttk.Treeview(master, columns=("Category", "Count"), show="headings", height=5)
        self.tree.heading("Category", text="Category")
        self.tree.heading("Count", text="Count")
        self.tree.place(relx=0.4, rely=0.37, anchor=tk.W)

        # Create a button to refresh the JSON file count information
        self.refresh_button = ttk.Button(master, text="Refresh", command=self.refresh_json_count, style="TButton")
        self.refresh_button.place(relx=0.92, rely=0.6, anchor=tk.CENTER)

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
            display_results_on_treeview(folder_path, self.tree)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()
