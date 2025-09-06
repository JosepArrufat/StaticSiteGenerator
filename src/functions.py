import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    inline_text_type = ""
    if delimiter == "**":
        inline_text_type = TextType.BOLD
    elif delimiter == "_":
        inline_text_type = TextType.ITALIC
    elif delimiter == "`":
        inline_text_type = TextType.CODE
    else:
        raise ValueError("Delimiter must be a valid markdown syntax")
    escaped_delimiter = re.escape(delimiter)
    pattern = f'{escaped_delimiter}(.*?){escaped_delimiter}'
    new_nodes_text = []
    for node in old_nodes:
        splitted_node = re.split(pattern, node.text)
        new_nodes_text.append(splitted_node)
    text_nodes = []
    for text in new_nodes_text:
        for i in range(0, len(text)):
            if text[i] == "":
               continue 
            elif i % 2 == 0 or i == 0:
                text_node = TextNode(text[i], TextType.TEXT)
            else:
                text_node = TextNode(text[i], inline_text_type)
            text_nodes.append(text_node)
    return text_nodes

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    new_nodes_text = []
    for node in old_nodes:
        splitted_node = re.split(pattern, node.text)
        new_nodes_text.append(splitted_node)
    text_nodes = []
    for text in new_nodes_text:
        i = 0
        while i < len(text):
            block_text = text[i]
            if i + 2 < len(text):
                alt_text = text[i + 1]
                url = text[i + 2]
                if block_text != "":
                    text_nodes.append(TextNode(block_text, TextType.TEXT))
                text_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                i += 3 
            else:
                if block_text != "":
                    text_nodes.append(TextNode(block_text, TextType.TEXT))
                break
    return text_nodes

def split_nodes_link(old_nodes):
    pattern = r'\[(.*?)\]\((.*?)\)'
    new_nodes_text = []
    for node in old_nodes:
        splitted_node = re.split(pattern, node.text)
        new_nodes_text.append(splitted_node)
    text_nodes = []
    for text in new_nodes_text:
        i = 0
        while i < len(text):
            block_text = text[i]
            if i + 2 < len(text):
                alt_text = text[i + 1]
                url = text[i + 2]
                if block_text != "":
                    text_nodes.append(TextNode(block_text, TextType.TEXT))
                text_nodes.append(TextNode(alt_text, TextType.LINK, url))
                i += 3 
            else:
                if block_text != "":
                    text_nodes.append(TextNode(block_text, TextType.TEXT))
                break
    return text_nodes

def text_to_text_nodes(text):
    






            
            
            
        

