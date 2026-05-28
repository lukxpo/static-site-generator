import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images


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
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD, url="www.bacon.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("bacon", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "bacon")

    def test_split(self):
        node = TextNode("This is a text with **bacon** and it's good", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with ", TextType.TEXT),
                TextNode("bacon", TextType.BOLD),
                TextNode(" and it's good", TextType.TEXT),
            ],
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
    unittest.main()