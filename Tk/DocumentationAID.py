import tkinter as tk
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Script Launcher")

        # Create buttons
        self.create_button("Document Creator ReadMe AR", self.launch_ReadMeAR_application)
        self.create_button("Document Creator ReadMe PB", self.launch_ReadMePB_application)
        self.create_button("Document Creator EXCEL AR", self.launch_ExcelAR_application)
        self.create_button("Document Creator EXCEL PB", self.launch_ExcelPB_application)
        self.create_button("Document Creator EXCEL WB", self.launch_ExcelWB_application)

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack(pady=5)

    def launch_ReadMeAR_application(self):
        subprocess.run(["python", "Tools/ReadMeConvAR.py"])
    def launch_ReadMePB_application(self):
        subprocess.run(["python", "Tools/ReadMeConvPB.py"])
    def launch_ExcelAR_application(self):
        subprocess.run(["python", "Tools/ExcelConvAR.py"])
    def launch_ExcelPB_application(self):
        subprocess.run(["python", "Tools/ExcelConvPB.py"])
    def launch_ExcelWB_application(self):
        subprocess.run(["python", "Tools/ExcelConvWB.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
