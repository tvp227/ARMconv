import tkinter as tk
from tkinter import ttk, PhotoImage
import subprocess
import getpass
import sys
import os

# Function to install required packages
def install_packages(requirements_file):
    try:
        with open(requirements_file, 'r') as file:
            packages = file.read().splitlines()
            for package in packages:
                os.system(f"{sys.executable} -m pip install {package}")
                print(f"Installed {package}")
    except FileNotFoundError:
        print("Requirements file not found.")

# Main function
def main():
    # Your main script code here
    print("Running main script...")

if __name__ == "__main__":
    # Path to requirements.txt
    requirements_file = "requirements.txt"
    
    # Check and install required packages
    install_packages(requirements_file)
    
    # Run main script
    main()


##Main
def execute_script_py(script):
    subprocess.Popen(["python", script])
    sys.exit()

def execute_script_ps1(script):
    subprocess.Popen(["powershell", script])
    sys.exit()

def create_main_window():
    window = tk.Tk()
    window.title("ARMConv by Tom Porter")
    window.geometry("300x650")
    window.resizable(False, False)

    # Load background image
    background_image = PhotoImage(file="Prereqs/background.png")

    # Create a canvas for the background
    canvas = tk.Canvas(window, width=300, height=650)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    # Load picture
    picture_image = PhotoImage(file="Prereqs/logo.png")
    resized_picture_image = picture_image.subsample(5, 5)
    picture_label = tk.Label(window, image=resized_picture_image)
    picture_label.place(x=75, y=10)

    # Add a label for grouping related buttons
    tk.Label(window, text="Toolbox", font=("Helvetica", 12, "bold"), fg="white", bg="black").place(x=110, y=80)

    buttons = [
        ("ARM Template Conversion", lambda: execute_script_py("Tk/ArmTemplateConvertion.py")),
        ("JSON Decompress", lambda: execute_script_py("Tk/JsonDecompress.py")),
        ("Azure CLI", lambda: execute_script_ps1("Powershell/Playbook_ARM_Template_Generator.ps1")),
        ("Documentation Aid", lambda: execute_script_py("Tk/DocumentationAID.py")),
        ("API", lambda: execute_script_py("API/GetRequest.py")),
        ("KQL Crowbar", lambda: execute_script_py("Tools/KQLConv.py")),
        ("Content Summary", lambda: execute_script_py("Tools/ArmTemplateCount.py")),
        ("CamelCase", lambda: execute_script_py("Tools/CamelCaseConv.py")),
        ("AR Tactics Summary", lambda: execute_script_py("Tools/TacticsExtraction.py")),
        ("Rule Enablement", lambda: execute_script_py("Tools/RuleEnablement.py"))
    ]

    # Add styled buttons
    for i, (text, command) in enumerate(buttons):
        button = ttk.Button(window, text=text, command=command)
        button.place(x=50, y=120 + i * 50, width=200, height=40)

    window.mainloop()

if __name__ == "__main__":
    username = getpass.getuser()
    print(f"Welcome, {username}, to ARMConv by Tom Porter.")
    print("Please review ReadMe for context on tooling")
    create_main_window()
