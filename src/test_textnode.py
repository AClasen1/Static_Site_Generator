import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none_html(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.NORMAL, "url")
        self.assertNotEqual(node, node2)

    def test_different_text_not_equal(self):
        node = TextNode("This is a text node", TextType.ITALIC, "url")
        node2 = TextNode("This is a different text node", TextType.ITALIC, "url")
        self.assertNotEqual(node, node2)
    


if __name__ == "__main__":
    unittest.main()
