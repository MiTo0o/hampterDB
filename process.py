import os
import hashlib
import json
import shutil
from PIL import Image

SOURCE_DIR = "gallery-dl"
OUTPUT_DIR = "images"
MANIFEST_FILE = "manifest.json"
MAX_SIZE = (400, 400)

def sync():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    print("🚀 Moving and resizing hamsters...")
    
    # Walk through gallery-dl
    for root, dirs, files in os.walk(SOURCE_DIR, topdown=False):
        for filename in files:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): 
                continue
            
            source_path = os.path.join(root, filename)
            
            # Generate Unique ID
            with open(source_path, "rb") as f:
                file_id = hashlib.md5(f.read()).hexdigest()
            
            target_path = os.path.join(OUTPUT_DIR, f"{file_id}.png")
            
            # If it's a new image, resize and save it
            if not os.path.exists(target_path):
                try:
                    with Image.open(source_path) as img:
                        img.thumbnail(MAX_SIZE)
                        img.save(target_path, "PNG")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            
            # MOVE logic: delete the source regardless (if processed or already exists)
            os.remove(source_path)

        # Cleanup empty subfolders in gallery-dl
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Update the manifest list
    all_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(all_files, f)
        
    print(f"✅ Sync Complete. Total images in collection: {len(all_files)}")

if __name__ == "__main__":
    sync()