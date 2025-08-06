#restore
import utils
import os

def restore_default_background():
    try:
        utils.admin_check()

        path_to_dota = os.path.join(utils.find_steam_path(), "steamapps", "common", "dota 2 beta")
        dota_russian_path = os.path.join(path_to_dota, "game", "dota_russian")
    
        original_backup = os.path.join(dota_russian_path, "pak01_000.vpk")
        current_file = os.path.join(dota_russian_path, "pak01_dir.vpk")
        fix_file = os.path.join(dota_russian_path, "pak02_dir.vpk")
    
        if not os.path.exists(original_backup):
            print("Error: Backup not found!")
            print("Try verifying game files in Steam")
            return False

        for file_path in [current_file, fix_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.rename(original_backup, current_file)
        print("Default wallpaper successfully restored!")
        return True

    except Exception as e:
        print(f"Restore Error: {e}")
        return False

if __name__ == "__main__":
    success = restore_default_background()
    utils.wait_exit(0 if success else 1)