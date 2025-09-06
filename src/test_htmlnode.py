import unittest 
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 =  HTMLNode(tag="img", props={"src":"img_girl.jpg","width":"500","height":"600"})
        node3 =  HTMLNode("div", None, [node, node2])
        node.props_to_html()
        node2.props_to_html()
        node3.props_to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Go to Google", {"href":"https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f"})
        self.assertEqual(node2.to_html(), "<a href='https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f'>Go to Google</a>")
        node3 = LeafNode("button", "Submit", {"type":"submit"})
        self.assertEqual(node3.to_html(), "<button type='submit'>Submit</button>")

class TestParentnode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Go to Google", {"src":"https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f"})
        node3 = LeafNode("button", "Submit", {"type":"submit"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node, node, node2, node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p>Hello, world!</p><a src='https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f'>Go to Google</a><button type='submit'>Submit</button></div>",
        )


if __name__ == "__main__":
    unittest.main()