import unittest
from transformation import *

class TestTransformation(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
