import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

if __name__ == "__main__":
    unittest.main()
