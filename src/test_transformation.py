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

class TestExtractLinksImages(unittest.TestCase):
    def test_one_image(self):
        input_text = "An image: ![The alt text](www.mysite.png)"
        extracted_images = extract_markdown_images(input_text)
        self.assertListEqual(extracted_images, [("The alt text", "www.mysite.png")])

    def test_two_images(self):
        input_text = "An image: ![The alt text](www.mysite.png), A second image: ![The second alt text](www.myothersite.com)"
        extracted_images = extract_markdown_images(input_text)
        self.assertListEqual(extracted_images, [("The alt text", "www.mysite.png"),("The second alt text", "www.myothersite.com")])

    def test_no_images(self):
        input_text = "This is just **bold text**, nothing to see here"
        extracted_images = extract_markdown_images(input_text)
        self.assertListEqual(extracted_images, [])

    def test_one_link(self):
        input_text = "A link: ![The anchor text](www.mysite.com)"
        extracted_images = extract_markdown_images(input_text)
        self.assertListEqual(extracted_images, [("The anchor text", "www.mysite.com")])

    def test_two_links(self):
        input_text = "A link: ![The anchor text](www.mysite.com), A second link: ![The second anchor text](www.myothersite.com)"
        extracted_images = extract_markdown_images(input_text)
        self.assertListEqual(extracted_images, [("The anchor text", "www.mysite.com"),("The second anchor text", "www.myothersite.com")])

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_one_image(self):
        starter_node = [TextNode("Here's ![an image](myimg.png) to split out", TextType.TEXT)]
        split_node = split_node_image(starter_node)
        split_goal = [TextNode("Here's ", TextType.TEXT), TextNode("an image", TextType.IMAGE, "myimg.png"), TextNode(" to split out", TextType.TEXT)]
        self.assertListEqual(split_node, split_goal)

    def test_one_link(self):
        starter_node = [TextNode("Here's [a link](mysite.com) to split out", TextType.TEXT)]
        split_node = split_node_link(starter_node)
        split_goal = [TextNode("Here's ", TextType.TEXT), TextNode("a link", TextType.LINK, "mysite.com"), TextNode(" to split out", TextType.TEXT)]
        self.assertListEqual(split_node, split_goal)

    def test_one_image_and_one_link(self):
        starter_node = [TextNode("Here's ![an image](myimg.png) and [a link](mysite.com) to split out", TextType.TEXT)]
        image_split_node = split_node_image(starter_node)
        link_split_node = split_node_link(image_split_node)
        split_goal = [TextNode("Here's ", TextType.TEXT), TextNode("an image", TextType.IMAGE, "myimg.png"), TextNode(" and ", TextType.TEXT), TextNode("a link", TextType.LINK, "mysite.com"), TextNode(" to split out", TextType.TEXT)]
        self.assertListEqual(link_split_node, split_goal)

    def test_no_link(self):
        starter_node = [TextNode("Here's some text to split out", TextType.TEXT)]
        split_node = split_node_link(starter_node)
        split_goal = [TextNode("Here's some text to split out", TextType.TEXT)]
        self.assertListEqual(split_node, split_goal)

    def test_same_image_twice(self):
        starter_node = [TextNode("Here's ![an image](myimg.png). It's just ![an image](myimg.png)", TextType.TEXT)]
        split_node = split_node_image(starter_node)
        split_goal = [TextNode("Here's ", TextType.TEXT), TextNode("an image", TextType.IMAGE, "myimg.png"), TextNode(". It's just ", TextType.TEXT), TextNode("an image", TextType.IMAGE, "myimg.png")]
        self.assertListEqual(split_node, split_goal)

    def test_two_different_links(self):
        starter_node = [TextNode("Here's [a link](mysite.com) and another one to [google](google.com), for comparison", TextType.TEXT)]
        split_node = split_node_link(starter_node)
        split_goal = [TextNode("Here's ", TextType.TEXT), TextNode("a link", TextType.LINK, "mysite.com"), TextNode(" and another one to ", TextType.TEXT), TextNode("google", TextType.LINK, "google.com"), TextNode(", for comparison", TextType.TEXT)]
        self.assertListEqual(split_node, split_goal)

class TestTextToTextNodes(unittest.TestCase):
    def split_out_everything(self):
        text_to_nodify = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_as_text_nodes = text_to_textnodes(text_to_nodify)
        node_goal = [TextNode("This is ", TextType.TEXT, None), TextNode("text", TextType.BOLD, None), TextNode(" with an ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word and a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" and an ", TextType.TEXT, None), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT, None), TextNode("link", TextType.LINK, "https://boot.dev")]
        self.assertListEqual(text_as_text_nodes, node_goal)

if __name__ == "__main__":
    unittest.main()
