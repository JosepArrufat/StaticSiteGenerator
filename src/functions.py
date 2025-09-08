import re
import textwrap
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        escaped_delimiter = re.escape(delimiter)
        pattern = rf'{escaped_delimiter}(.*?){escaped_delimiter}'
        
        parts = re.split(pattern, node.text)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing delimiter for {delimiter}")
            
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = re.split(pattern, node.text)
        
        # Check for malformed markdown
        if len(parts) % 3 != 1:
            raise ValueError("Invalid markdown syntax for images: malformed tag")

        for i in range(0, len(parts), 3):
            if parts[i]:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            if i + 1 < len(parts):
                new_nodes.append(TextNode(parts[i+1], TextType.IMAGE, parts[i+2]))
    return new_nodes

def split_nodes_link(old_nodes):
    pattern = r'\[(.*?)\]\((.*?)\)'
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = re.split(pattern, node.text)
        
        # Check for malformed markdown
        if len(parts) % 3 != 1:
            raise ValueError("Invalid markdown syntax for links: malformed tag")

        for i in range(0, len(parts), 3):
            if parts[i]:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            if i + 1 < len(parts):
                new_nodes.append(TextNode(parts[i+1], TextType.LINK, parts[i+2]))
    return new_nodes

def text_to_text_nodes(text):
    """
    Converts a raw markdown string into a list of TextNode objects.
    """
    # Start with a single TextNode containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process images and links first as they have complex syntax
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Process inline delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def markdown_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    if re.match(r"^#{1,6}\s", markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = True
    for line in lines:
        if not (line.startswith("- ") or line.startswith("* ")):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i, line in enumerate(lines):
        m = re.match(r"^(\d+)\.\s", line)
        if not m or int(m.group(1)) != i + 1:
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    children = []
    block_type = markdown_to_block_type(text)
    if block_type == BlockType.PARAGRAPH:
        lines = text.split("\n")
        joined = " ".join(line.strip() for line in lines if line.strip() != "")
        inline_nodes = text_to_text_nodes(joined)
        children = [n.text_node_to_html_node() for n in inline_nodes]
        return children
    elif block_type == BlockType.HEADING:
        header_text = re.sub(r"^#{1,6}\s", "", text)
        nodes = text_to_text_nodes(header_text)
        for n in nodes:
            children.append(n.text_node_to_html_node())
        return children
    elif block_type == BlockType.QUOTE: 
        lines = text.split("\n")
        cleaned_lines = [line.strip().removeprefix(">").strip() for line in lines]
        if "" in cleaned_lines:
            quote_text = "\n".join(cleaned_lines)
        else:
            quote_text = " ".join(cleaned_lines)
        nodes = text_to_text_nodes(quote_text)
        for n in nodes:
            children.append(n.text_node_to_html_node())
        return children
    elif block_type == BlockType.UNORDERED_LIST:
        lines = text.split("\n")
        cleaned_lines = [line.strip().lstrip('-* ').strip() for line in lines]
        for l in cleaned_lines:
            child_nodes = text_to_text_nodes(l)
            li_childs = []
            for n in child_nodes:
                li_text_childs = li_childs.append(n.text_node_to_html_node())
            children.append(ParentNode(tag="li", children=li_childs))
        return children
    elif block_type == BlockType.ORDERED_LIST:
        lines = text.split("\n")
        for line in lines:
            content = re.sub(r"^\d+\.\s", "", line)
            child_nodes = text_to_text_nodes(content)
            li_children = [n.text_node_to_html_node() for n in child_nodes]
            children.append(ParentNode(tag="li", children=li_children))
        return children
    elif block_type == BlockType.CODE:
        open_i = text.find("```")
        after_fence = open_i + 3
        if after_fence < len(text) and text[after_fence] == "\n":
            start_i = after_fence + 1
        else:
            start_i = after_fence
        end_i = text.find("```", start_i)
        content = text[start_i:end_i]
        content = textwrap.dedent(content)
        code_node = TextNode(text=content, text_type=TextType.CODE).text_node_to_html_node()
        return [code_node]
    
    

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    HTML_nodes = []
    for block in markdown_blocks:
        children = text_to_children(block)
        block_type = markdown_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            HTML_nodes.append(ParentNode(tag="p", children=children))
        elif block_type == BlockType.QUOTE: 
            HTML_nodes.append(ParentNode(tag="blockquote", children=children))
        elif block_type == BlockType.HEADING:
            lines = block.splitlines()
            paragraph_lines = []
            for line in lines:
                line_blocktype = markdown_to_block_type(line)
                if line_blocktype == BlockType.HEADING:
                    children = text_to_children(line)
                    if len(paragraph_lines) >= 1:
                        joined = " ".join(p_line.strip() for p_line in paragraph_lines if p_line.strip() != "")
                        inline_nodes = text_to_text_nodes(joined)
                        p_children = [n.text_node_to_html_node() for n in inline_nodes]
                        HTML_nodes.append(ParentNode(tag="p", children=p_children))
                    paragraph_lines = []
                    hash_count = 0
                    for char in line:
                        if char == "#" and hash_count < 6:
                            hash_count += 1
                        else:
                            break
                    HTML_nodes.append(ParentNode(tag=f"h{hash_count}", children=children))
                else:
                    paragraph_lines.append(line)
        elif block_type == BlockType.UNORDERED_LIST:
            HTML_nodes.append(ParentNode(tag="ul", children=children))
        elif block_type == BlockType.ORDERED_LIST:
            HTML_nodes.append(ParentNode(tag="ol", children=children))
        elif block_type == BlockType.CODE:
            HTML_nodes.append(ParentNode(tag="pre", children=children))
        
    return ParentNode(tag="div", children=HTML_nodes)
        

    
        


       



