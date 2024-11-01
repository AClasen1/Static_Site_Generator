from htmlnode import *
from textnode import *
import re

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

def extract_markdown_images(text):
    markdown_images = []
    image_markdowns = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for image_markdown in image_markdowns:
        markdown_images.append(image_markdown)
    return markdown_images

def extract_markdown_links(text):
    markdown_links = []
    link_markdowns = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for link_markdown in link_markdowns:
        markdown_links.append(link_markdown)
    return markdown_links

def split_node_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            split_nodes.append(node)
        else:
            images_in_node = extract_markdown_images(node.text)
            if images_in_node != []:
                split_node = split_out_image([node], images_in_node)
                split_nodes.extend(split_node)
            else:
                split_nodes.append(node)
    return split_nodes

def split_out_image(nodes,images_in_node):
    if images_in_node == []:
        return nodes
    else:
        first_image_markdown = f"![{images_in_node[0][0]}]({images_in_node[0][1]})"
        split_final_node = nodes[-1].text.split(first_image_markdown, 1)
        nodes_with_image_split_out = nodes[:-1]
        if split_final_node[0] != "":
            nodes_with_image_split_out.append(TextNode(split_final_node[0], TextType.TEXT))
        nodes_with_image_split_out.append(TextNode(images_in_node[0][0], TextType.IMAGE, images_in_node[0][1]))
        if split_final_node[1] != "":
            nodes_with_image_split_out.append(TextNode(split_final_node[1], TextType.TEXT))
        return split_out_image(nodes_with_image_split_out, images_in_node[1:])
    
def split_node_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            split_nodes.append(node)
        else:
            links_in_node = extract_markdown_links(node.text)
            if links_in_node != []:
                split_node = split_out_link([node], links_in_node)
                split_nodes.extend(split_node)
            else:
                split_nodes.append(node)
    return split_nodes

def split_out_link(nodes,links_in_node):
    if links_in_node == []:
        return nodes
    else:
        first_link_markdown = f"[{links_in_node[0][0]}]({links_in_node[0][1]})"
        split_final_node = nodes[-1].text.split(first_link_markdown, 1)
        nodes_with_link_split_out = nodes[:-1]
        if split_final_node[0] != "":
            nodes_with_link_split_out.append(TextNode(split_final_node[0], TextType.TEXT))
        nodes_with_link_split_out.append(TextNode(links_in_node[0][0], TextType.LINK, links_in_node[0][1]))
        if split_final_node[1] != "":
            nodes_with_link_split_out.append(TextNode(split_final_node[1], TextType.TEXT))
        return split_out_link(nodes_with_link_split_out, links_in_node[1:])