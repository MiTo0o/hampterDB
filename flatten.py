import os
import shutil

def flatten_directory(source_dir, target_dir):
    # Ensure target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"Flattening {source_dir} into {target_dir}...")

    # os.walk goes through every subfolder recursively
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            # Construct the full path to the file
            source_path = os.path.join(root, filename)
            target_path = os.path.join(target_dir, filename)

            # Handle Name Collisions
            # If a file with the same name exists, we append a number to it
            if os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(target_dir, f"{name}_{counter}{ext}")):
                    counter += 1
                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")

            # Move the file
            shutil.move(source_path, target_path)
            print(f"Moved: {filename}")

    print("Done! Everything is now in one folder.")


SOURCE = 'gallery-dl' 
TARGET = 'temp_hamster'

flatten_directory(SOURCE, TARGET)