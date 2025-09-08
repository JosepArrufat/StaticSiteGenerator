import os

def copy_content_from_dir(origin, destination):
    if not os.path.exists(orign) or os.path.exists(destination):
        raise ValueError("Please provide a proper path")
    origin_items = os.listdir(origin)
    for item in origin_items:
        item_path = os.path.join(origin, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination)
        if os.path.isdir(item_path):
            new_path = os.path.join(destination, item)
            new_dir = os.mkdir(new_path)
            copy_content_from_dir(item_path, new_dir)
    

