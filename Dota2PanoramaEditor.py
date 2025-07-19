import os
import shutil
import subprocess
import sys

def check_dependencies():
    #Verify all required files exist in the vpk_creator directory
    required_files = {
        'vpk.exe': "VPK tool not found",
        'Create vpk-archive from pak01_dir folder.bat': "Batch file not found"
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
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
    
    path_to_steam = get_valid_input(
        "2. Enter full path to Steam folder: ",
        lambda x: os.path.exists(os.path.join(x, "steamapps", "common", "dota 2 beta"))
    )
    
    try:
        # ========== DOTA 2 FILE OPERATIONS ==========
        # Prepare Dota 2 paths
        path_to_dota = os.path.join(path_to_steam, "steamapps", "common", "dota 2 beta")
        dota_russian_path = os.path.join(path_to_dota, "game", "dota_russian")
        
        # Backup current VPK file
        os.chdir(dota_russian_path)
        if os.path.exists("pak01_000.vpk"):
            os.remove("pak01_000.vpk")  # Remove old backup
        if os.path.exists("pak01_dir.vpk"):
            os.rename("pak01_dir.vpk", "pak01_000.vpk")  # Create new backup

        # ========== VPK CREATION ==========
        script_dir = os.path.dirname(os.path.abspath(__file__))
        vpk_creator_dir = os.path.join(script_dir, "vpk_creator")
        
        # Prepare target directory structure
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