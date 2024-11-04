from textnode import TextNode, TextType
from transformation import *
from block_transformation import *

def main():
	text_to_blockify = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.







* This is the first list item in a list block
* This is a list item
* This is another list item"""
	print(markdown_to_blocks(text_to_blockify))

main()
