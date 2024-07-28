import os
import shutil
import subprocess
import sys
import json

def get_flow_launcher_plugins_path():
    return os.path.join(os.getenv('APPDATA'), 'FlowLauncher', 'Plugins')

def get_plugin_name():
    with open('plugin.json', 'r') as f:
        data = json.load(f)
        return data['Name']

def copy_plugin_files(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Folders and files to exclude
    exclude = ['.git', '.github', 'venv', '.vscode', '__pycache__', 'lib']

    # Copy main plugin files
    for item in os.listdir(source_dir):
        if item not in exclude:
            s = os.path.join(source_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, ignore=shutil.ignore_patterns(*exclude))
            else:
                shutil.copy2(s, d)

    # Install dependencies to lib folder
    lib_dir = os.path.join(dest_dir, 'lib')
    os.makedirs(lib_dir, exist_ok=True)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-t', lib_dir])

def main():
    source_dir = os.getcwd()
    plugin_name = get_plugin_name()
    flow_launcher_plugins_path = get_flow_launcher_plugins_path()
    dest_dir = os.path.join(flow_launcher_plugins_path, plugin_name)

    print(f"Copying plugin files to: {dest_dir}")
    copy_plugin_files(source_dir, dest_dir)
    print("Done! Please restart Flow Launcher to load the updated plugin.")

if __name__ == "__main__":
    main()