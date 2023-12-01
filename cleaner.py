# Create .exe : pyinstaller --onefile cleaner.py

import os
import shutil
from tqdm import tqdm

def clean_pc():
    temp_paths = [
        os.path.join(os.environ.get('TEMP'), ''),
        os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
        os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Temp'),
    ]

    total_deleted = 0

    for path in temp_paths:
        try:
            for root, dirs, files in os.walk(path):
                file_count = sum(len(files) for _, _, files in os.walk(root))
                with tqdm(total=file_count, desc=f'Cleaning {path}') as pbar:
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                            total_deleted += 1
                            pbar.update(1)
                        except Exception as e:
                            print(f"Failed to delete {file_path}: {e}")
                            pbar.update(1)
        except Exception as e:
            print(f"Error while cleaning {path}: {e}")

    recycle_bin_path = "C:/$Recycle.Bin"
    try:
        shutil.rmtree(recycle_bin_path, ignore_errors=True)
        total_deleted += 1
        print("Recycle Bin cleaned successfully")
    except Exception as e:
        print(f"Failed to clean Recycle Bin: {e}")

    return total_deleted

if __name__ == "__main__":
    print("Starting cleaning process...")
    deleted_count = clean_pc()
    print(f"Total files deleted: {deleted_count}")