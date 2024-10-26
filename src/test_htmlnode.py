import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
