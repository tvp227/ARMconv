import json
import tkinter as tk
from tkinter import filedialog
import threading

def get_last_segment(id_path):
    return id_path.split("/")[-1]

def get_connection_id_format(connection_id, subscription_id, resource_group_location):
    return f"[concat('/subscriptions/', '{subscription_id}', '/providers/Microsoft.Web/locations/', '{resource_group_location}', '/managedApis/{connection_id}')]"

def get_connection_ids(json_data):
    connection_ids = []

    def traverse(obj):
        if isinstance(obj, dict):
            if "$connections" in obj:
                value = obj["$connections"].get("value")
                if value and isinstance(value, dict):
                    for connection_key, connection_value in value.items():
                        if isinstance(connection_value, dict) and "id" in connection_value:
                            connection_id = get_last_segment(connection_value["id"])
                            connection_ids.append(connection_id)
            for key, value in obj.items():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(json_data)
    return connection_ids

def replace_connection_ids(json_data, formatted_connection_ids):
    def traverse(obj):
        if isinstance(obj, dict):
            if "$connections" in obj:
                value = obj["$connections"].get("value")
                if value and isinstance(value, dict):
                    for connection_key, connection_value in value.items():
                        if isinstance(connection_value, dict) and "id" in connection_value:
                            connection_id = get_last_segment(connection_value["id"])
                            formatted_connection_id = formatted_connection_ids.get(connection_id)
                            if formatted_connection_id:
                                connection_value["id"] = formatted_connection_id
            for key, value in obj.items():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(json_data)

def load_and_convert_template():
    file_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if file_path:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)

        connection_ids = get_connection_ids(json_data)
        formatted_connection_ids = {
            get_last_segment(id): get_connection_id_format(id, "subscription().subscriptionId", "resourceGroup().location")
            for id in connection_ids
        }

        replace_connection_ids(json_data, formatted_connection_ids)

        with open(file_path, "w") as modified_json_file:
            json.dump(json_data, modified_json_file, indent=2)

        return file_path, formatted_connection_ids

def show_changed_parameters(file_path, formatted_connection_ids):
    root = tk.Tk()
    root.title("Changed Parameters")

    connection_ids_text = tk.StringVar()
    label = tk.Label(root, textvariable=connection_ids_text, justify=tk.LEFT)
    label.pack(pady=10)

    connection_ids_text.set("Connection ID Formats:\n{}".format("\n".join(formatted_connection_ids.values())))

    def continue_script():
        root.destroy()

    button = tk.Button(root, text="Next", command=continue_script)
    button.pack(pady=20)

    root.mainloop()

def load_template_from_file():
    file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            template_json = file.read()
        return template_json
    else:
        return None

def extract_default_values(template_data):
    parameters = template_data.get("parameters", {})
    default_values = {}

    for param_name, param_details in parameters.items():
        default_value = param_details.get("defaultValue")
        last_segment = get_last_segment(default_value)
        default_values[param_name] = get_connection_id_format(
            last_segment,
            "subscription().subscriptionId",
            "resourceGroup().location"
        )

    return default_values

def update_template(template_data, default_values):
    updated_template_data = template_data.copy()

    parameters = updated_template_data.get("parameters", {})
    for param_name, param_details in parameters.items():
        if param_name in default_values:
            param_details["defaultValue"] = default_values[param_name]

    return updated_template_data

def save_updated_template(updated_template_data, output_path):
    with open(output_path, "w") as output_file:
        json.dump(updated_template_data, output_file, indent=2)

def display_default_values(default_values):
    window = tk.Tk()
    window.title("Default Values")

    label = tk.Label(window, text="Default Values:")
    label.pack()

    for param_name, concat_expression in default_values.items():
        entry_label = tk.Label(window, text=f"{param_name}: {concat_expression}")
        entry_label.pack()

    window.mainloop()

if __name__ == "__main__":
    # For the ARM template conversion
    file_path, formatted_connection_ids = load_and_convert_template()
    show_changed_parameters(file_path, formatted_connection_ids)

    # For the final parameters
    template_json = load_template_from_file()

    if template_json:
        template_data = json.loads(template_json)
        default_values = extract_default_values(template_data)
        display_default_values(default_values)

        output_path = filedialog.asksaveasfilename(title="Save Updated JSON File", defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if output_path:
            updated_template_data = update_template(template_data, default_values)
            save_updated_template(updated_template_data, output_path)
            print(f"Updated template saved to {output_path}")
