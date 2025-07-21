import os
import shutil
import subprocess
import sys

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

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

def check_dependencies():
    #Verify all required files exist in the vpk_creator directory
    required_files = {
        'vpk.exe': "VPK tool not found",
        'Create vpk-archive from pak01_dir folder.bat': "Batch file not found"
    }
    
    script_dir = get_script_dir()
    vpk_creator_dir = os.path.join(script_dir, "vpk_creator")
    
    missing_files = []
    for file, error in required_files.items():
        if not os.path.exists(os.path.join(vpk_creator_dir, file)):
            missing_files.append(error)
    
    if missing_files:
        print("Setup error:")
        for error in missing_files:
            print(f"- {error}")
        print(f"Please check folder: {vpk_creator_dir}")
        return False
    return True

def main():
    # Verify all required files exist
    if not check_dependencies():
        sys.exit(1)
    
    print("Dota 2 Panorama Editor - VPK Creator")
    print("-----------------------------------")
    
    # Get validated user inputs
    path_to_webm = get_valid_input(
        "1. Enter full path to your .webm file: ",
        lambda x: os.path.exists(x)
    )
    
    path_to_steam = find_steam_path()
    
    try:
        # ========== DOTA 2 FILE OPERATIONS ==========
        # Prepare Dota 2 paths
        path_to_dota = os.path.join(path_to_steam, "steamapps", "common", "dota 2 beta")
        dota_russian_path = os.path.join(path_to_dota, "game", "dota_russian")
        
        # Replacement `pak01_dir.vpk` with `pak01_000.vpk`
        os.chdir(dota_russian_path)
        if os.path.exists("pak01_000.vpk"):
            os.remove("pak01_000.vpk")
        if os.path.exists("pak01_dir.vpk"):
            os.rename("pak01_dir.vpk", "pak01_000.vpk")  

        # ========== VPK CREATION ==========
        script_dir = get_script_dir()
        vpk_creator_dir = os.path.join(script_dir, "vpk_creator")
        
        # Moving the target webm file to the vpk creator directory
        # Rename target webm to `123`
        target_webm_dir = os.path.join(vpk_creator_dir, "pak01_dir", "123")
        os.makedirs(target_webm_dir, exist_ok=True)
        shutil.copy2(path_to_webm, target_webm_dir)
        os.chdir(target_webm_dir)
        os.replace(os.path.basename(path_to_webm), "123.webm")

        # Execute VPK creation batch file
        bat_path = os.path.join(vpk_creator_dir, "Create vpk-archive from pak01_dir folder.bat")
        print("\nCreating VPK archive...")
        
        # Run with proper working directory and quoted path
        result = subprocess.run(
            f'"{bat_path}"',  # Quotes handle spaces in path
            shell=True,
            cwd=vpk_creator_dir,  # Critical for finding vpk.exe
            check=True
        )
        
        # ========== FINALIZATION ==========
        # Copy resulting VPK back to Dota
        created_vpk = os.path.join(vpk_creator_dir, "pak01_dir.vpk")
        if os.path.exists(created_vpk):
            shutil.copy(created_vpk, dota_russian_path)
            print("\nSuccess! VPK file has been updated.")
        else:
            print("\nError: VPK file was not created")
            sys.exit(1)
            
    except subprocess.CalledProcessError:
        print("\nError: VPK creation failed")
        sys.exit(1)
    except Exception as e:
        print(f"\nCritical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()