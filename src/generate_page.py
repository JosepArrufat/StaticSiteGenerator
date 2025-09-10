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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as my_file:
        md = my_file.read()
    with open(template_path, "r") as template_file:
        template_text = template_file.read()
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    full_html = template_text.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_path)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    content_path_items = os.listdir(dir_path_content)
    for item in content_path_items:
        if os.path.isfile(os.path.join(dir_path_content, item)) and item.endswith(".md"):
            new_item_ext = item.replace(".md", ".html")
            new_dest = os.path.join(dest_dir_path, new_item_ext)
            generate_page(os.path.join(dir_path_content, item), template_path, new_dest, basepath)
        if os.path.isdir(os.path.join(dir_path_content, item)):
            new_dest = os.path.join(dest_dir_path, item)
            generate_page_recursive(os.path.join(dir_path_content, item), template_path, new_dest, basepath)
        
        
    


    
