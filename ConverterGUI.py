import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import subprocess  

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("ARM-Converter-Tool")
        master.geometry("300x400")
        master.resizable(False, False)

        # Create a label with the title
        title_label = ttk.Label(master, text="Welcome to My Tkinter GUI", font=("Helvetica", 16))
        title_label.pack(pady=20)

        # Use a Frame to hold the background image
        self.background_frame = ttk.Frame(master)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.background_image = Image.open("Prereqs/Background.png")
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.background_frame, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a custom style for the buttons
        style = ttk.Style()
        style.theme_use("clam")

        # Configure general button style
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=10,  
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
        self.convert_playbook_button = ttk.Button(master, text="Convert Playbook", command=self.launch_playbook_application, style="TButton")
        self.convert_playbook_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.convert_workbook_button = ttk.Button(master, text="Convert Workbook", command=self.launch_workbook_application, style="TButton")
        self.convert_workbook_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.convert_KQL_button = ttk.Button(master, text="Convert KQL", command=self.launch_KQL_application, style="TButton")
        self.convert_KQL_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        #===
        self.exit_button = ttk.Button(master, text="Exit", command=master.destroy, style="Exit.TButton")
        self.exit_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    # Launchers
    def launch_playbook_application(self):
        subprocess.run(["python", "Tools/PlayBookConv.py"])

    def launch_workbook_application(self):
        subprocess.run(["python", "Tools/WorkBookConv.py"])
    
    def launch_KQL_application(self):
        subprocess.run(["python", "Tools/KQLConv.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()
