import os
import requests 
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from dotenv import load_dotenv

# Load environment variables from .env in the 'prereqs' folder
dotenv_path = os.path.join("prereqs", ".env")
load_dotenv(dotenv_path)

# Retrieve environment variables
SubscriptionID = os.getenv('SUBSCRIPTION_ID')
ResourceGroup = os.getenv('RESOURCE_GROUP')
Workspace = os.getenv('WORKSPACE')
TenantID = os.getenv('TENANTID')
ClientID = os.getenv('CLIENTID')
ClientSecret = os.getenv('SECRET')

def get_bearer_token(tenant_id, client_id, client_secret):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "resource": "https://management.azure.com",
        "client_secret": client_secret
    }
    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.HTTPError as err:
        raise Exception(f"HTTP error occurred while fetching bearer token: {err}")
    except Exception as e:
        raise Exception(f"Failed to fetch bearer token: {str(e)}")

def make_authenticated_request(bearer_token, url):
    full_url = url.format(SubscriptionID=SubscriptionID, ResourceGroup=ResourceGroup, Workspace=Workspace)

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()

        # Print the response content in pretty JSON format
        print("Response:", json.dumps(response.json(), indent=2))
    except requests.exceptions.HTTPError as err:
        raise Exception(f"HTTP error occurred: {err}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def on_button_click(url):
    try:
        bearer_token = get_bearer_token(TenantID, ClientID, ClientSecret)
        make_authenticated_request(bearer_token, url)
        messagebox.showinfo("Request Completed", f"{url} request completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
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
        button = tk.Button(window, text=button_text, command=lambda url=url: on_button_click(url))
        button.pack(pady=5)

    #Mainloop
    window.mainloop()
