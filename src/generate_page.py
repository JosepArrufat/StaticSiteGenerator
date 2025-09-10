import re
import os
from functions import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        h1 = re.match(r"^# ", line.strip())
        if h1:
            return re.sub(r"^# ", "", line.strip())
    raise Exception("No h1 was found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as my_file:
        md = my_file.read()
    with open(template_path, "r") as template_file:
        template_text = template_file.read()
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    full_html = re.sub("{{ Title }}", title, template_text)
    full_html = re.sub("{{ Content }}", html, template_text)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_path)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("no content path found")
    content_path_items = os.listdir(dir_path_content)
    for item in content_path_items:
        if os.path.isfile(item) and item.endswith(".md"):
            new_dest = os.path.join(dest_dir_path, item)
            generate_page(os.path.join(dir_path_content, item), template_path, new_dest)
        elif os.path.isdir(item):
            generate_page_recursive(os.path.join(dir_path_content, item), template_path, dest_dir_path)
        
        
    


    
