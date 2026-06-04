from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False

        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(len(split_text)):
                if split_text[i]:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
    
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if matches:
            text_tmp = node.text
            for match in matches:
                image_alt = match[0]
                image_link = match[1]
                split_text = text_tmp.split(f"![{image_alt}]({image_link})")
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(split_text) > 1:
                    text_tmp = split_text[1]
                else:
                    text_tmp = ""
            
            if text_tmp:
                new_nodes.append(TextNode(text_tmp, TextType.TEXT))
        
        else:
            new_nodes.append(node)


    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if matches:
            text_tmp = node.text
            for match in matches:
                link_text = match[0]
                link_url = match[1]
                split_text = text_tmp.split(f"[{link_text}]({link_url})")
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                if len(split_text) > 1:
                    text_tmp = split_text[1]
                else:
                    text_tmp = ""
            
            if text_tmp:
                new_nodes.append(TextNode(text_tmp, TextType.TEXT))
        
        else:
            new_nodes.append(node)


    return new_nodes


def text_to_textnodes(text):
    nodes_list = [TextNode(text, TextType.TEXT)]
    nodes_list = split_nodes_delimiter(nodes_list, "**",TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_",TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`",TextType.CODE)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)

    return nodes_list
