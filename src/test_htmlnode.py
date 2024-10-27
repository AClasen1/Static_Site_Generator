import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        test_props = {"key1": "lorem", "key2": "ipsum"}
        node = HTMLNode(props = test_props)
        props_to_html = node.props_to_html()
        self.assertEqual(props_to_html, ' key1="lorem" key2="ipsum"')

    def test_node_to_string(self):
        test_children = ["child1", "child2"]
        test_props = {"key1": "lorem", "key2": "ipsum"}
        node = HTMLNode("p", "This is a test value", test_children, test_props)
        self.assertEqual(str(node), f"HTMLNode: tag = p,\nvalue = This is a test value,\n children = ['child1', 'child2'],\n props = {{'key1': 'lorem', 'key2': 'ipsum'}}")

    def test_empty_props_to_html(self):
        test_props = {}
        node = HTMLNode(props = test_props)
        props_to_html = node.props_to_html()
        self.assertEqual(props_to_html, "")

class TestLeafNode(unittest.TestCase):
    def test_bold_to_html(self):
        node = LeafNode(value = "Test bold text", tag = "b")
        self.assertEqual(node.to_html(), "<b>Test bold text</b>")

    def test_link_to_html(self):
        node = LeafNode(value = "Test link text", tag = "a", props = {"href": "mylink.com"})
        self.assertEqual(node.to_html(), '<a href="mylink.com">Test link text</a>')

    def test_no_tag(self):
        node = LeafNode(value = "I have no tag and I must scream")
        self.assertEqual(node.to_html(), "I have no tag and I must scream")
    
    def test_no_value(self):
        node = LeafNode(value = "This is getting nulled", tag = "p")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
