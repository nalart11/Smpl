import os
import shutil
import json
import zipfile
import atexit
import signal
import sys


os.system('cls' if os.name == 'nt' else 'clear')

paths = {
    '1.20.1': 'C:\\Users\\nalart11\\AppData\\Roaming\\.minecraft\\1.20.1\\mods\\',
    '1.20.2': 'C:\\Users\\nalart11\\AppData\\Roaming\\.minecraft\\1.20.2\\mods\\',
    '1.20.4': 'C:\\Users\\nalart11\\AppData\\Roaming\\.minecraft\\1.20.4\\mods\\',
    '4videos': 'C:\\Users\\nalart11\\AppData\\Roaming\\.minecraft\\4videos\\mods\\',
    'SP': 'C:\\Users\\nalart11\\AppData\\Roaming\\.minecraft\\SP\\mods\\'
}


def get_mod_info(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        if 'fabric.mod.json' in zip_ref.namelist():
            with zip_ref.open('fabric.mod.json') as f:
                data = json.load(f)
                name = data.get('name', '')
                version = data.get('version', '')
                if version.startswith('>'):
                    version = version[1:] + '+'
                elif version.startswith('='):
                    version = version[1:]
                return name, version
    return None, None


def get_file_name(usefull):
    files = [f for f in os.listdir(path = usefull) if f.endswith('.jar') or f.endswith('.jar.disabled')]
    number = len(files)
    if number == 0:
        print("There're no mods ._.")
    else:
        mods = {}
        for file in files:
            name, version = get_mod_info(os.path.join(usefull, file))
            if name and version:
                mods[name] = {'file': file, 'version': version}
        with open('mods.json', 'w') as f:
            json.dump(mods, f)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('All mods:')
        sorted_mods = sorted(mods.items(), key=lambda x: x[0])
        for i, (name, info) in enumerate(sorted_mods):
            color = '\033[92m' if info['file'].endswith('.jar') else '\033[90m'
            print(f"{color}{i}: {name}\033[0m")
        print(f"There're {number} mods, a lot!")
        print("To exit program type 'exit'")
        toggle_mod(usefull, sorted_mods)


def toggle_mod(usefull, sorted_mods):
    while True:
        mod_index = input('Enter the number or name of the mod: ')
        if mod_index.lower() == 'exit':
            break
        if mod_index.isdigit() and int(mod_index) < len(sorted_mods):
            mod_index = int(mod_index)
            mod_name, mod_info = sorted_mods[mod_index]
        else:
            matches = [mod for mod in sorted_mods if mod[0].lower().startswith(mod_index.lower())]
            if len(matches) == 1:
                mod_name, mod_info = matches[0]
            elif len(matches) > 1:
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Multiple mods match your input:")
                    for i, (name, info) in enumerate(matches):
                        color = '\033[92m' if info['file'].endswith('.jar') else '\033[90m'
                        print(f"{color}{i}: {name}\033[0m")
                    choice = input("Please enter the number of the mod you want to toggle or 'down' to go back: ")
                    if choice.lower() == 'down':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        get_file_name(usefull)
                        break
                    elif choice.isdigit() and int(choice) < len(matches):
                        mod_name, mod_info = matches[int(choice)]
                        if mod_info['file'].endswith('.jar'):
                            os.rename(os.path.join(usefull, mod_info['file']), os.path.join(usefull, mod_info['file'] + '.disabled'))
                            mod_info['file'] += '.disabled'
                            os.system('cls' if os.name == 'nt' else 'clear')
                        else:
                            os.rename(os.path.join(usefull, mod_info['file']), os.path.join(usefull, mod_info['file'].replace('.disabled', '')))
                            mod_info['file'] = mod_info['file'].replace('.disabled', '')
                            os.system('cls' if os.name == 'nt' else 'clear')
                    else:
                        print("Invalid input. Please enter a valid number.")
                continue
            else:
                print("No mods match your input.")
                continue
        if mod_info['file'].endswith('.jar'):
            os.rename(os.path.join(usefull, mod_info['file']), os.path.join(usefull, mod_info['file'] + '.disabled'))
            mod_info['file'] += '.disabled'
        else:
            os.rename(os.path.join(usefull, mod_info['file']), os.path.join(usefull, mod_info['file'].replace('.disabled', '')))
            mod_info['file'] = mod_info['file'].replace('.disabled', '')
        print(f"Mod {mod_name} has been {'disabled' if mod_info['file'].endswith('.disabled') else 'enabled'}")
        os.system('cls' if os.name == 'nt' else 'clear')
        print('All mods:')
        for i, (name, info) in enumerate(sorted_mods):
            color = '\033[92m' if info['file'].endswith('.jar') else '\033[90m'
            print(f"{color}{i}: {name}\033[0m")
        print("To exit program type 'exit'")


def cleanup():
    if os.path.exists('mods.json'):
        os.remove('mods.json')
    if os.path.exists('files.json'):
        os.remove('files.json')


atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))


print('What u want to see?')
hz = input()
usefull = paths.get(hz)
if usefull:
    get_file_name(usefull)
else:
    print('Do u want to use ur own path?')
    ppap = input()
    if ppap == 'yes':
        usefull = input('Place it here: ')
        get_file_name(usefull)
    else:
        print('Ok, closing programm', end='')