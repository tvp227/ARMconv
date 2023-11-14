import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess  # For running external processes

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        master.title("GUI Example")
        master.geometry("250x195")
        master.resizable(False, False)

        self.background_image = Image.open("Background.png")
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.convert_playbook_button = tk.Button(master, text="Convert Playbook", command=self.launch_playbook_application)
        self.convert_playbook_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.convert_workbook_button = tk.Button(master, text="Convert Workbook", command=self.launch_workbook_application)
        self.convert_workbook_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.exit_button = tk.Button(master, text="Exit", command=master.destroy)
        self.exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def launch_playbook_application(self):
        # Replace "playbook_script.py" with the name of your Playbook script
        subprocess.run(["python", "PlayBookConv.py"])

    def launch_workbook_application(self):
        # Replace "workbook_script.py" with the name of your Workbook script
        subprocess.run(["python", "WorkBookConv.py"])


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
