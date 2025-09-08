import os
import shutil

def copy_content_from_dir(origin, destination):
    if not os.path.exists(origin):
        raise ValueError("Please provide a proper path")
    if os.path.exists(destination):
        print(f"Deleting previous content of {destination}")
        shutil.rmtree(destination)
    print("Blank folder, we proceed")
    os.mkdir(destination)
    copy_recursive(origin, destination)

def copy_recursive(origin, destination):
    origin_items = os.listdir(origin)
    for item in origin_items:
        item_path = os.path.join(origin, item)
        if os.path.isfile(item_path):
            print(f"Copying file: {item_path} to {destination}")
            shutil.copy(item_path, destination)
        if os.path.isdir(item_path):
            print(f"Entering directory: {item_path}")
            new_path = os.path.join(destination, item)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            copy_recursive(item_path, new_path)

        
