from htmlnode import *

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