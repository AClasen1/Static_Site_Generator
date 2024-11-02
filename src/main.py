from textnode import TextNode, TextType
from transformation import *

def main():
	text_to_nodify = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
	print(text_to_textnodes(text_to_nodify))

main()
