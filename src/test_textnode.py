import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        self.assertEqual(node, node3)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text ode", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.PLAIN)
        node4 = TextNode("This is a text node", TextType.BOLD, url="www.bacon.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

if __name__ == "__main__":
    unittest.main()