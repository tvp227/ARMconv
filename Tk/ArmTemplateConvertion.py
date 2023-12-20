import tkinter as tk
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Script Launcher")

        # Create buttons
        self.create_button("Playbook Convertion", self.launch_playbook_application)
        self.create_button("Workbook Convertion", self.launch_workbook_application)

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack(pady=5)

    def launch_playbook_application(self):
        subprocess.run(["python", "Tools/PlayBookConv.py"])

    def launch_workbook_application(self):
        subprocess.run(["python", "Tools/WorkBookConv.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
