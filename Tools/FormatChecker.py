import os
import json

def get_json_schemas(directory):
    schema_count = {}

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Check if the JSON has the "$schema" property
                        if "$schema" in data:
                            schema = data["$schema"]
                            schema_count[schema] = schema_count.get(schema, 0) + 1
                except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
                    pass

    return schema_count

if __name__ == "__main__":
    directory_path = "C:\Dev\ztf-sentinel"  # Change this to the directory path containing your JSON files
    schema_count = get_json_schemas(directory_path)

    if schema_count:
        print("\nCount of each $schema value in JSON files:")
        for schema, count in schema_count.items():
            print(f"{schema}: {count} occurrences")
    else:
        print("No $schema values found in JSON files.")
