from textnode import TextNode
from file_functions import copy_content_from_dir
from generate_page import generate_page_recursive

def main():
    copy_content_from_dir("static", "public")
    generate_page_recursive("content", "template.html", "public/index.html")

if __name__ == "__main__":
    main()