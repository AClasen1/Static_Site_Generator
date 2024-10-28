import unittest
from transformation import *

class TestTextToLeaf(unittest.TestCase):
    def test_text(self):
        textnode = TextNode("Default text", TextType.TEXT)
        text_node_as_html = text_node_to_html_node(textnode).to_html()
        self.assertEqual(text_node_as_html, "Default text")

    def test_bold(self):
        textnode = TextNode("Bold text", TextType.BOLD)
        text_node_as_html = text_node_to_html_node(textnode).to_html()
        self.assertEqual(text_node_as_html, "<b>Bold text</b>")

    def test_link(self):
        textnode = TextNode("link text", TextType.LINK, url = "myurl.com")
        text_node_as_html = text_node_to_html_node(textnode).to_html()
        self.assertEqual(text_node_as_html, '<a href="myurl.com">link text</a>')

    def test_image(self):
        textnode = TextNode("alt text", TextType.IMAGE, url = "imgurl.png")
        text_node_as_html = text_node_to_html_node(textnode).to_html()
        self.assertEqual(text_node_as_html, '<img src="imgurl.png" alt="alt text"></img>')

class TestSplitDelimiter(unittest.TestCase):
    def test_no_text(self):
        styled_nodes = [TextNode("**bold text**", TextType.BOLD), TextNode("*italic text*", TextType.ITALIC)]
        split_styled_nodes = split_nodes_delimiter(styled_nodes,"*",TextType.ITALIC)
        for i in range(len(styled_nodes)):
            self.assertEqual(styled_nodes[i],split_styled_nodes[i])

    def test_no_matching_delimiters(self):
        styled_nodes = [TextNode("**bold text**", TextType.TEXT), TextNode("*italic text*", TextType.TEXT)]
        split_styled_nodes = split_nodes_delimiter(styled_nodes,"`",TextType.CODE)
        for i in range(len(styled_nodes)):
            self.assertEqual(styled_nodes[i],split_styled_nodes[i])

    def test_basic_bold_split(self):
        starter_node = [TextNode("Here's some **bold text** to split out", TextType.TEXT)]
        split_node = split_nodes_delimiter(starter_node,"**",TextType.BOLD)
        split_goal = [TextNode("Here's some ",TextType.TEXT), TextNode("bold text", TextType.BOLD), TextNode(" to split out", TextType.TEXT)]
        for i in range(len(split_node)):
            self.assertEqual(split_node[i], split_goal[i])

    def test_bold_italic_split(self):
        starter_node = [TextNode("Here's some **bold text** to split out, and then some *italic text*", TextType.TEXT)]
        bold_split_node = split_nodes_delimiter(starter_node,"**",TextType.BOLD)
        italic_split_node = split_nodes_delimiter(bold_split_node,"*",TextType.ITALIC)
        split_goal = [TextNode("Here's some ",TextType.TEXT), TextNode("bold text", TextType.BOLD), TextNode(" to split out, and then some ", TextType.TEXT), TextNode("italic text", TextType.ITALIC)]
        for i in range(len(italic_split_node)):
            self.assertEqual(italic_split_node[i], split_goal[i])

if __name__ == "__main__":
    unittest.main()
