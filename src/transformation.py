from htmlnode import *
from textnode import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value = text_node.text)
        case "bold":
            return LeafNode(value = text_node.text, tag = "b")
        case "italic":
            return LeafNode(value = text_node.text, tag = "i")
        case "code":
            return LeafNode(value = text_node.text, tag = "code")
        case "link":
            return LeafNode(value = text_node.text, tag = "a", props = {"href": text_node.url})
        case "image":
            return LeafNode(value = "", tag = "img", props = {"src": text_node.url, "alt": text_node.text})
        case _:
            raise TypeError("Inapplicable type supplied")