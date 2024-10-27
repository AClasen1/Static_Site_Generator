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

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        child_node = LeafNode(value = "tagless value")
        node = ParentNode([child_node], tag = None, props = "test_props")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        child_node = LeafNode(value = "tagless value")
        node = ParentNode([child_node], tag = None, props = "test_props")
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_one_child(self):
        child_node = LeafNode(tag = "a", value = "link text", props = {"href": "mylink.url"})
        node = ParentNode(children= [child_node], tag = "p", props = {"type": "container"})
        self.assertEqual(node.to_html(),'<p type="container"><a href="mylink.url">link text</a></p>')

    def test_grand_children(self):
        grandchild_node = LeafNode(tag = "a", value = "link text", props = {"href": "mylink.url"})
        child_node = ParentNode(children= [grandchild_node], tag = "p", props = {"type": "subcontainer"})
        node = ParentNode(children= [child_node], tag = "p", props = {"type": "container"})
        self.assertEqual(node.to_html(),'<p type="container"><p type="subcontainer"><a href="mylink.url">link text</a></p></p>')

    def test_three_children(self):
        child_node_0 = LeafNode(tag = "a", value = "link text", props = {"href": "mylink.url"})
        child_node_1 = LeafNode(tag = "b", value = "bold text")
        child_node_2 = LeafNode(value = "naked text")
        node = ParentNode(children = [child_node_0, child_node_1, child_node_2], tag = "p", props = {"type": "container"})
        self.assertEqual(node.to_html(), '<p type="container"><a href="mylink.url">link text</a><b>bold text</b>naked text</p>')

if __name__ == "__main__":
    unittest.main()
