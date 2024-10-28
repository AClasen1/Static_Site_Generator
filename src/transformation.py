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
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            split_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError("Odd number of delimiters in text node to be split")
        else:
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if len(split_node[i]) != 0:
                    new_node_type = TextType.TEXT
                    if i % 2 == 1:
                        new_node_type = text_type
                    split_nodes.append(TextNode(split_node[i], new_node_type))
    return split_nodes