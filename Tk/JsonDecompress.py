import tkinter as tk
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Script Launcher")

        # Create buttons
        self.create_button("Decompress Analytic Rules", self.launch_AnalyticR_Decompress)
        self.create_button("Decompress Automation Rules", self.launch_AutoR_Decompress)


    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack(pady=5)

    def launch_AnalyticR_Decompress(self):
        subprocess.run(["python", "Tools/AnalyticRuleDecompress.py"])
    def launch_AutoR_Decompress(self):
        subprocess.run(["python", "Tools/AutomationRuleDecompress.py"])


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
