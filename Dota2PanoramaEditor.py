#main
import os
import shutil
import subprocess
import utils

def fix_patch_7_39_d(vpk_creator_dir, dota_russian_path):
    fix_path = os.path.join(vpk_creator_dir, "pak02_dir.vpk")
    shutil.copy(fix_path, dota_russian_path)

def cleanup():
    panorama_path = os.path.join(utils.get_script_dir(), "vpk_creator", "pak01_dir", "123")
    shutil.rmtree(panorama_path, ignore_errors=True)

def check_dependencies():
    #Verify all required files exist in the vpk_creator directory
    required_files = {
        'vpk.exe': "VPK tool not found",
        'Create vpk-archive from pak01_dir folder.bat': "Batch file not found"
    }
    
    script_dir = utils.get_script_dir()
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
    # Restarts as administrator
    utils.admin_check()

    # Verify all required files exist
    if not check_dependencies():
        utils.wait_exit(1)
    
    print("Dota 2 Panorama Editor - VPK Creator")
    print("-----------------------------------")
    
    # Get validated user inputs
    path_to_webm = utils.get_valid_input(
        "1. Enter full path to your .webm file: ",
        lambda x: os.path.exists(x)
    )
    
    # Prepare Dota 2 paths
    path_to_steam = utils.find_steam_path()
    path_to_dota = os.path.join(path_to_steam, "steamapps", "common", "dota 2 beta")
    dota_russian_path = os.path.join(path_to_dota, "game", "dota_russian")
    
    try:
        # ========== DOTA 2 FILE OPERATIONS ==========
        # Replacement `pak01_dir.vpk` with `pak01_000.vpk`
        os.chdir(dota_russian_path)
        if os.path.exists("pak01_000.vpk"):
            os.remove("pak01_000.vpk")
        if os.path.exists("pak01_dir.vpk"):
            os.rename("pak01_dir.vpk", "pak01_000.vpk")  

        # ========== VPK CREATION ==========
        script_dir = utils.get_script_dir()
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
        subprocess.run(
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
            fix_patch_7_39_d(vpk_creator_dir, dota_russian_path)
            print("\nSuccess! VPK file has been updated.")
            return 0
        else:
            print("\nError: VPK file was not created")
            return 1
            
    except subprocess.CalledProcessError:
        print("\nError: VPK creation failed")
        return 2
    except Exception as e:
        print(f"\nCritical error: {e}")
        return 3
    finally:
        cleanup()

if __name__ == "__main__":
    exit_code = main()
    utils.wait_exit(exit_code)