from htmlnode import *

def markdown_to_blocks(markdown):
    whitespace_stripped_markdown_blocks = []
    markdown_blocks = markdown.split("\n\n")
    for block in markdown_blocks:
        if block != "":
            whitespace_stripped_markdown_blocks.append(block.strip(" \n"))
    return whitespace_stripped_markdown_blocks