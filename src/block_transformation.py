from htmlnode import *
from transformation import *

def markdown_to_blocks(markdown):
    whitespace_stripped_markdown_blocks = []
    markdown_blocks = markdown.split("\n\n")
    for block in markdown_blocks:
        if block != "":
            whitespace_stripped_markdown_blocks.append(block.strip(" \n\t"))
    return whitespace_stripped_markdown_blocks

def block_to_block_type(markdown_block):
    block_type = "paragraph"
    markdown_block_lines = markdown_block.split("\n")
    unordered_list_lines = 0
    ordered_list_lines = 0
    quote_lines = 0
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        block_type = "code"
    elif (len(markdown_block.lstrip("#")) < len(markdown_block)
          and len(markdown_block.lstrip("#")) >= len(markdown_block) - 6
          and markdown_block.lstrip("#").startswith(" ")):
        block_type = "heading"
    else: 
        for i in range(len(markdown_block_lines)):
            line_number = i + 1
            if markdown_block_lines[i].startswith(">"):
                quote_lines += 1
            if markdown_block_lines[i].startswith("* ") or markdown_block_lines[i].startswith("- "):
                unordered_list_lines += 1
            if markdown_block_lines[i].startswith(f"{line_number}. "):
                ordered_list_lines += 1
        if len(markdown_block_lines) == unordered_list_lines:
            block_type = "unordered_list"
        elif len(markdown_block_lines) == ordered_list_lines:
            block_type = "ordered_list"
        elif len(markdown_block_lines) == quote_lines:
            block_type = "quote"
    return block_type

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    markdown_html_child_nodes = []
    htmlnode_to_append = None
    for markdown_block in markdown_blocks:
        markdown_block_type = block_to_block_type(markdown_block)
        match markdown_block_type:
            case "paragraph":
                text_nodes = text_to_textnodes(markdown_block.replace("\n", " "))
                leaf_htmlnodes = list(map(text_node_to_html_node, text_nodes))
                htmlnode_to_append = ParentNode(leaf_htmlnodes, "p")
            case "code":
                text_nodes = text_to_textnodes(markdown_block[3:-3])
                leaf_htmlnodes = list(map(text_node_to_html_node, text_nodes))
                code_htmlnode = ParentNode(leaf_htmlnodes, "code")
                htmlnode_to_append = ParentNode([code_htmlnode], "pre")
            case "heading":
                header_tag = get_header_tag(markdown_block)
                text_nodes = text_to_textnodes(deprefix_string(markdown_block))
                leaf_htmlnodes = list(map(text_node_to_html_node, text_nodes))
                htmlnode_to_append = ParentNode(leaf_htmlnodes, header_tag)
            case "quote":
                markdown_block_without_quotes = " ".join(list(map(lambda x: x[1:], markdown_block.split("\n"))))
                text_nodes = text_to_textnodes(markdown_block_without_quotes)
                leaf_htmlnodes = list(map(text_node_to_html_node, text_nodes))
                htmlnode_to_append = ParentNode(leaf_htmlnodes, "blockquote")
            case "unordered_list":
                htmlnode_to_append = list_to_htmlnode(markdown_block, markdown_block_type)
            case "ordered_list":
                htmlnode_to_append = list_to_htmlnode(markdown_block, markdown_block_type)
            case _:
                print(markdown_block_type)
                raise ValueError("Invalid block type")
        markdown_html_child_nodes.append(htmlnode_to_append)
    markdown_doc_html_node = ParentNode(markdown_html_child_nodes,"div")
    return markdown_doc_html_node

def deprefix_string(string):
    return " ".join(string.split(" ")[1:])

def get_header_tag(header_markdown):
    hash_count = len(header_markdown.split(" ")[0])
    return f"h{hash_count}"

def list_to_htmlnode(markdown_block, markdown_block_type):
    list_tag = ""
    if markdown_block_type == "unordered_list":
        list_tag = "ul"
    elif markdown_block_type == "ordered_list":
        list_tag = "ol"
    else:
        raise ValueError("Invalid list type")
    list_markdown_block_without_bullets = list(map(deprefix_string, markdown_block.split("\n")))
    list_markdown_block_item_textnodes = list(map(text_to_textnodes, list_markdown_block_without_bullets))
    list_markdown_block_item_htmlnodes = list(map(lambda x: map(text_node_to_html_node, x), list_markdown_block_item_textnodes))
    list_markdown_block_htmlnodes = list(map(lambda x: ParentNode(x, "li"), list_markdown_block_item_htmlnodes))
    return ParentNode(list_markdown_block_htmlnodes, list_tag)

def extract_title(markdown):
    header_block = markdown_to_html_node(markdown).children[0]
    if header_block.tag != "h1":
        raise ValueError("Header block not represent")
    return header_block.children[0].value