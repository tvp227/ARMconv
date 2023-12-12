import requests
import json

def export_az_sentinel_automation_rule_to_json():
    # Prompt the user for input
    workspace_name = input("Enter Log Analytics workspace name: ")
    resource_group_name = input("Enter resource group name: ")
    automation_rule_id = input("Enter Microsoft Sentinel Automation rule ID (optional, press Enter to skip): ")
    subscription_id = input("Enter Azure subscription ID: ")
    access_token = input("Enter Azure access token: ")

    # Setup the Authentication header needed for the REST calls
    auth_header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    if automation_rule_id:
        # Export a single automation rule
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/automationRules/{automation_rule_id}?api-version=2021-10-01-preview'
        response = requests.get(url, headers=auth_header)

        result_json = response.json()
        result_display_name = result_json['properties']['displayName']

        with open(f'{result_display_name}.json', 'w') as json_file:
            json.dump(result_json, json_file, indent=4)
    else:
        # Export all automation rules
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/automationRules/?api-version=2021-10-01-preview'
        response = requests.get(url, headers=auth_header)

        results = response.json()['value']

        for result in results:
            result_json = json.dumps(result, indent=4)
            result_display_name = result['properties']['displayName']

            with open(f'{result_display_name}.json', 'w') as json_file:
                json_file.write(result_json)

# Call the function
export_az_sentinel_automation_rule_to_json()
