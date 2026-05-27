import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_empty(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)
    
    def test_eq_full(self):
        node = HTMLNode("p", "bacon")
        node2 = HTMLNode("p", "bacon")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("p", "bacon")
        node2 = HTMLNode("a", "bacon")
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "BACON", {"href": "www.bacon.com"})
        self.assertEqual(node.to_html(), '<a href="www.bacon.com">BACON</a>')

if __name__ == "__main__":
    unittest.main()