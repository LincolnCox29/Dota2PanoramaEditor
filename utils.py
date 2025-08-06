#utils
import os
import sys
import ctypes

def admin_check():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Restarts as administrator...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
        sys.exit()

def get_valid_input(prompt, validation_func):
    #Get and validate user input with retrya
    while True:
        try:
            value = input(prompt).strip()
            if validation_func(value):
                return value
            print("Invalid path, please try again")
        except Exception as e:
            print(f"Error: {e}")

def get_script_dir():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def find_steam_path():
    steam_dir_file = os.path.join(get_script_dir(), "steam_dir")
    def save_steam_path(path):
        with open(steam_dir_file, 'w', encoding='utf-8') as file:
            file.write(path)
        
    # Check if there is a saved Steam path
    if (os.path.getsize(steam_dir_file) != 0):
        with open(steam_dir_file, 'r', encoding='utf-8') as file:
            return file.readlines()[0]

    print("Searching Steam directories...")
    print("This might take several minutes, please wait")
    # Search standard directories
    possible_paths = [
        os.path.expandvars("%ProgramFiles(x86)%\\Steam"),
        os.path.expandvars("%ProgramFiles%\\Steam"),
        os.path.expandvars("%LOCALAPPDATA%\\Steam"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "steamapps")):
            save_steam_path(path)
            return path
    
    # If not found in standard locations, search all drives
    drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
    
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if "Steam" in dirs:
                steam_path = os.path.join(root, "Steam")
                if os.path.exists(os.path.join(steam_path, "steamapps")):
                    save_steam_path(steam_path)
                    return steam_path

    # If not found any way - enter manually
    path = get_valid_input(
        "2. Enter full path to Steam folder: ",
        lambda x: os.path.exists(os.path.join(x, "steamapps", "common", "dota 2 beta"))
    )
    save_steam_path(path)
    return path

def wait_exit(exit_code):
    import msvcrt
    print("\nPress any key to exit...")
    msvcrt.getch()
    sys.exit(exit_code)