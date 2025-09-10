from textnode import TextNode
from file_functions import copy_content_from_dir
from generate_page import generate_page_recursive, generate_page
import sys

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_content_from_dir("static", "public")
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()