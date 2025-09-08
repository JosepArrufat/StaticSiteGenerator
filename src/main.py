from textnode import TextNode
from file_functions import copy_content_from_dir

def main():
    copy_content_from_dir("static", "public")
    

if __name__ == "__main__":
    main()