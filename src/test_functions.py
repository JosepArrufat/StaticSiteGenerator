import unittest
import textwrap
from textnode import TextNode, TextType
from functions import (
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links, split_nodes_image,
    split_nodes_link, 
    text_to_text_nodes, 
    markdown_to_blocks,
    markdown_to_block_type,
    BlockType, 
    markdown_to_html_node
)
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splits(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        node3 = TextNode("This is alink node", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/d105e9f9-ffe6-4e94-871a-1774d186b5d3.png")
        node4 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes4 = split_nodes_delimiter([node4], "`", TextType.CODE)
        compare_nodes4 = [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ]
        self.assertEqual(new_nodes4, compare_nodes4)
        node5 = TextNode("This is text with a **bold** word and even more **bold**", TextType.TEXT)
        compare_nodes5 = [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word and even more ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                        ]
        new_nodes5 = split_nodes_delimiter([node5], "**", TextType.BOLD)
        self.assertEqual(new_nodes5, compare_nodes5)
        node6 = TextNode("**This** is text with a **bold** word and even more **bold**", TextType.TEXT)
        new_nodes6 = split_nodes_delimiter([node6], "**", TextType.BOLD)
        compare_nodes6 = [
                            TextNode("This", TextType.BOLD),
                            TextNode(" is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word and even more ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                        ]
        self.assertEqual(new_nodes6, compare_nodes6)

class TestTextPattern(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdownh_linjks(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class SplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_multiple_images(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes1 = split_nodes_image([node1])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes1,
        )

    def test_no_image(self):
        node2 = TextNode("This is a string with no images.", TextType.TEXT)
        new_nodes2 = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This is a string with no images.", TextType.TEXT, None),
            ],
            new_nodes2,
        )

    def test_start_with_image(self):
        node3 = TextNode("![first image](https://i.imgur.com/zjjcJKZ.png) and some text.", TextType.TEXT)
        new_nodes3 = split_nodes_image([node3])
        self.assertListEqual(
            [
                TextNode("first image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text.", TextType.TEXT, None),
            ],
            new_nodes3,
        )

    def test_end_with_image(self):
        node4 = TextNode("Some text and an image at the end ![end image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes4 = split_nodes_image([node4])
        self.assertListEqual(
            [
                TextNode("Some text and an image at the end ", TextType.TEXT, None),
                TextNode("end image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes4,
        )

    def test_multiple_images_no_text(self):
        node5 = TextNode("![image1](https://url1.com)![image2](https://url2.com)", TextType.TEXT)
        new_nodes5 = split_nodes_image([node5])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://url1.com"),
                TextNode("image2", TextType.IMAGE, "https://url2.com"),
            ],
            new_nodes5,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links(self):
        node1 = TextNode(
            "This is text with a [link](https://www.google.com) and another [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes1 = split_nodes_link([node1])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes1,
        )

    def test_no_link(self):
        node2 = TextNode("This is a string with no links.", TextType.TEXT)
        new_nodes2 = split_nodes_link([node2])
        self.assertListEqual(
            [
                TextNode("This is a string with no links.", TextType.TEXT, None),
            ],
            new_nodes2,
        )

    def test_start_with_link(self):
        node3 = TextNode("[first link](https://www.google.com) and some text.", TextType.TEXT)
        new_nodes3 = split_nodes_link([node3])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://www.google.com"),
                TextNode(" and some text.", TextType.TEXT, None),
            ],
            new_nodes3,
        )

    def test_end_with_link(self):
        node4 = TextNode("Some text and a link at the end [end link](https://www.example.com)", TextType.TEXT)
        new_nodes4 = split_nodes_link([node4])
        self.assertListEqual(
            [
                TextNode("Some text and a link at the end ", TextType.TEXT, None),
                TextNode("end link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes4,
        )

    def test_multiple_links_no_text(self):
        node5 = TextNode("[link1](https://link1.com)[link2](https://link2.com)", TextType.TEXT)
        new_nodes5 = split_nodes_link([node5])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://link1.com"),
                TextNode("link2", TextType.LINK, "https://link2.com"),
            ],
            new_nodes5,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_full_markdown(self):
        text = "This is **bold** and _italic_ and `code`. It also has an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)."
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(". It also has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_no_markdown(self):
        text = "This is just a regular string with no special formatting."
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is just a regular string with no special formatting.", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_consecutive_types(self):
        text = "Here is **bold**_italic_`code`![image](https://url1.com)[link](https://url2.com)."
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("image", TextType.IMAGE, "https://url1.com"),
            TextNode("link", TextType.LINK, "https://url2.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_start_and_end_with_markdown(self):
        text = "**Starts bold** and _ends italic_."
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("Starts bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("ends italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_only_images_and_links(self):
        text = "![image](https://url1.com)[link](https://url2.com)"
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://url1.com"),
            TextNode("link", TextType.LINK, "https://url2.com"),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_duplicate_markdown(self):
        # Test case: Repeated markdown elements
        text = "This is a **bold** word and another **bold** word."
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_with_extra_leading_and_trailing_newlines(self):
        md = """
This is a paragraph.

This is another.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another.",
            ]
        )

    def test_multiple_blank_lines(self):
        md = """# This is a heading


This is a paragraph.


And another paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph.",
                "And another paragraph.",
            ]
        )

    def test_no_blank_lines(self):
        md = "This is a single line with no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single line with no blank lines.",
            ]
        )

    def test_only_whitespace(self):
        md = "   \n\n\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
    
    def test_list_with_blank_line(self):
        md = """- This is the first item
- This is the second item

- This is the third item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is the first item\n- This is the second item",
                "- This is the third item",
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(markdown_to_block_type("This is a simple paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(markdown_to_block_type("This is a paragraph.\nWith a new line."), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(markdown_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(markdown_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(markdown_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(markdown_to_block_type("This is a paragraph\n# This is a heading"), BlockType.PARAGRAPH)

    def test_heading_invalid(self):
        self.assertNotEqual(markdown_to_block_type("###No space after hash"), BlockType.HEADING)
        self.assertNotEqual(markdown_to_block_type("####### Too many hashes"), BlockType.HEADING)
        self.assertNotEqual(markdown_to_block_type(" # Has leading spaces"), BlockType.HEADING)

    def test_code(self):
        code_block = """```
This is a code block
```"""
        self.assertEqual(markdown_to_block_type(code_block), BlockType.CODE)
        
    def test_code_invalid(self):
        # Missing closing backticks
        self.assertNotEqual(markdown_to_block_type("```\nThis is not a code block"), BlockType.CODE)
        # Not a code block because of text after opening backticks
        self.assertNotEqual(markdown_to_block_type("``` python\nThis is not a valid code block"), BlockType.CODE)

    def test_quote(self):
        quote_block = """> This is a quote.
> This is the second line."""
        self.assertEqual(markdown_to_block_type(quote_block), BlockType.QUOTE)

    def test_quote_invalid(self):
        # Missing `>` on a line
        self.assertNotEqual(markdown_to_block_type("> Line 1\nLine 2"), BlockType.QUOTE)
        # Leading spaces before `>`
        self.assertNotEqual(markdown_to_block_type(" > Line 1"), BlockType.QUOTE)

    def test_unordered_list(self):
        list_block = """- First item
- Second item
* Third item"""
        self.assertEqual(markdown_to_block_type(list_block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        # Missing space after `-`
        self.assertNotEqual(markdown_to_block_type("-No space after dash"), BlockType.UNORDERED_LIST)
        # Empty line in between items
        self.assertNotEqual(markdown_to_block_type("- Item 1\n\n- Item 2"), BlockType.UNORDERED_LIST)
        # A line without a marker
        self.assertNotEqual(markdown_to_block_type("- Item 1\nJust a normal line"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        list_block = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(markdown_to_block_type(list_block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid(self):
        # Missing `.`
        self.assertNotEqual(markdown_to_block_type("1 First item"), BlockType.ORDERED_LIST)
        # Incorrect sequence
        self.assertNotEqual(markdown_to_block_type("1. First\n2. Second\n4. Third"), BlockType.ORDERED_LIST)
        # Not starting at 1
        self.assertNotEqual(markdown_to_block_type("2. First item"), BlockType.ORDERED_LIST)
        # Missing space after `.`
        self.assertNotEqual(markdown_to_block_type("1.No space"), BlockType.ORDERED_LIST)
        
class TestMardownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = textwrap.dedent("""
        # This is an H1
        ## This is an H2
        ### This is an H3
        #### This is an H4
        ##### This is an H5
        ###### This is an H6
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an H1</h1><h2>This is an H2</h2><h3>This is an H3</h3><h4>This is an H4</h4><h5>This is an H5</h5><h6>This is an H6</h6></div>",
        )

    def test_unordered_lists(self):
        md = textwrap.dedent("""
        - This is the first item
        - This is the **second** item
        * And this is the _third_ one
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the first item</li><li>This is the <b>second</b> item</li><li>And this is the <i>third</i> one</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = textwrap.dedent("""
        1. This is the first item
        2. This is the second item
        3. This is the third item
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first item</li><li>This is the second item</li><li>This is the third item</li></ol></div>",
        )
    
    def test_ordered_lists_edge_cases(self):
        md = textwrap.dedent("""
        1. First item
        2. Second item
        3. Tenth item
        4. Eleventh item
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Tenth item</li><li>Eleventh item</li></ol></div>",
        )

    def test_quotes(self):
        md = textwrap.dedent("""
        > This is a quote block.
        > It can span multiple lines.
        > And can also include **inline** formatting.
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block. It can span multiple lines. And can also include <b>inline</b> formatting.</blockquote></div>",
        )
    
    def test_quotes_edge_case(self):
        md = textwrap.dedent("""
        >This is a quote with no space
        > And this line has a space
        > 
        > This line has a blank line above it
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with no space\nAnd this line has a space\n\nThis line has a blank line above it</blockquote></div>",
        )
  
if __name__ == "__main__":
    unittest.main()
