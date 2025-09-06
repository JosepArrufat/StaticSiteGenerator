import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.LINK)
        node4 = TextNode("This is a text node", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/d105e9f9-ffe6-4e94-871a-1774d186b5d3.png")
        node5 = TextNode("This is a text node", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/d105e9f9-ffe6-4e94-871a-1774d186b5d3.png")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)
        self.assertEqual(node5, node4)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node4 = TextNode("This is a link node", TextType.LINK, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/d105e9f9-ffe6-4e94-871a-1774d186b5d3.png")
        html_node4 = node4.text_node_to_html_node()
        self.assertEqual(html_node4.tag, "a")
        self.assertEqual(html_node4.value, "This is a link node")



if __name__ == "__main__":
    unittest.main()
