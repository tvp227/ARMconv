import requests
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# Define your environment ##ESENTIAL 
SubscriptionID = "981c926c-5460-4443-b3d8-7650646f8a13"
ResourceGroup = "sentinel-prod"
Workspace = "sentinel-prod"

def make_authenticated_request(bearer_token, url):
    full_url = url.format(SubscriptionID=SubscriptionID, ResourceGroup=ResourceGroup, Workspace=Workspace)

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            # Print the response content in pretty JSON format
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def on_button_click(bearer_token, url):
    try:
        make_authenticated_request(bearer_token, url)
        messagebox.showinfo("Request Completed", f"{url} request completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # input box foor the barer token
    bearer_token = simpledialog.askstring("Input", "Please enter your Bearer token:")

    if bearer_token:
        # Create the main window
        window = tk.Tk()
        window.title("Sentinel Overview")

        # Create buttons for each URL request
        buttons = [
            ("Get Automation Rules", f"https://management.azure.com/subscriptions/{SubscriptionID}/resourceGroups/{ResourceGroup}/providers/Microsoft.OperationalInsights/workspaces/{Workspace}/providers/Microsoft.SecurityInsights/automationRules?api-version=2023-02-01"),
            ("Get Analytic Rules", f"https://management.azure.com/subscriptions/{SubscriptionID}/resourceGroups/{ResourceGroup}/providers/Microsoft.OperationalInsights/workspaces/{Workspace}/providers/Microsoft.SecurityInsights/alertRules?api-version=2023-02-01"),
            ("Get Data Connectors", f"https://management.azure.com/subscriptions/{SubscriptionID}/resourceGroups/{ResourceGroup}/providers/Microsoft.OperationalInsights/workspaces/{Workspace}/providers/Microsoft.SecurityInsights/dataConnectors?api-version=2023-02-01"),
            ("Get Incidents", f"https://management.azure.com/subscriptions/{SubscriptionID}/resourceGroups/{ResourceGroup}/providers/Microsoft.OperationalInsights/workspaces/{Workspace}/providers/Microsoft.SecurityInsights/incidents?api-version=2023-02-01"),
            ("Get MetaData", f"https://management.azure.com/subscriptions/{SubscriptionID}/resourceGroups/{ResourceGroup}/providers/Microsoft.OperationalInsights/workspaces/{Workspace}/providers/Microsoft.SecurityInsights/metadata/?api-version=2023-02-01"),
        ]

        # buttons 
        for button_text, url in buttons:
            button = tk.Button(window, text=button_text, command=lambda url=url: on_button_click(bearer_token, url))
            button.pack(pady=5)

        #Mainloop
        window.mainloop()
