import os

def rename_json_files(base_folder):
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file == 'azuredeploy.json':
                folder_name = os.path.basename(root)
                new_name = os.path.join(root, f'{folder_name}.json')
                
                # Rename the file
                os.rename(os.path.join(root, file), new_name)
                print(f'Renamed: {file} to {new_name}')

# Specify the path to the parent folder
parent_folder_path = r'C:\Dev\ztf-sentinel\Playbooks'

# Call the function to rename the json files
rename_json_files(parent_folder_path)
