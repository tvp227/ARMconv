import tkinter as tk
import subprocess
import getpass
import sys

username = getpass.getuser()

def execute_script_py(script):
    subprocess.Popen(["python3", script])
    sys.exit()
def execute_script_ps1(script):
    subprocess.Popen(["powershell", script])
    sys.exit()

def create_main_window():
    window = tk.Tk()
    window.title("")
    window.geometry("250x500")
    window.resizable(False, False)

    ARM_Template_Convertion = tk.Button(window, text="ARM Template Convertion", command=lambda: execute_script_py("Tk/ArmTemplateConvertion.py"))
    ARM_Template_Convertion.place(x=50, y=50, width=150, height=40)

    Azure_CLI = tk.Button(window, text="Azure CLI", command=lambda: execute_script_ps1("Powershell/Playbook_ARM_Template_Generator.ps1"))
    Azure_CLI.place(x=50, y=100, width=120, height=40)

    Documentation_Aid = tk.Button(window, text="Documentation Aid", command=lambda: execute_script_py("Tk/DocumentationAID.py"))
    Documentation_Aid.place(x=50, y=150, width=120, height=40)

    API_get = tk.Button(window, text="API", command=lambda: execute_script_py("API/GetRequest.py"))
    API_get.place(x=50, y=200, width=120, height=40)

    KQL_conv = tk.Button(window, text="KQL Crowbar", command=lambda: execute_script_py("Tools/KQLConv.py"))
    KQL_conv.place(x=50, y=250, width=120, height=40)

    ARM_count = tk.Button(window, text="Content Summary", command=lambda: execute_script_py("Tools/ArmTemplateCount.py"))
    ARM_count.place(x=50, y=300, width=120, height=40)

    CamelCase = tk.Button(window, text="CamelCase", command=lambda: execute_script_py("Tools/CamelCaseConv.py"))
    CamelCase.place(x=50, y=350, width=120, height=40)

    Tactics_Summary = tk.Button(window, text="AR Tactics Summary", command=lambda: execute_script_py("Tools/TacticsExtraction.py"))
    Tactics_Summary.place(x=50, y=400, width=120, height=40)

    Rule_Enablement = tk.Button(window, text="Rule Enablement", command=lambda: execute_script_py("Tools/RuleEnablement.py"))
    Rule_Enablement.place(x=50, y=450, width=120, height=40)

    window.mainloop()

print(f"Welcome, {username}, to ARMConv by Tom Porter.")
print("Please review ReadMe for context on tooling")

create_main_window()
