import unittest
from block_transformation import *

class TestSplitMarkdownToBlocks(unittest.TestCase):
    def test_nicely_formatted_blocks(self):
        text_to_blockify = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        goal_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertListEqual (markdown_to_blocks(text_to_blockify), goal_blocks)    

    def test_not_as_nicely_formatted_blocks(self):
        text_to_blockify = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item"""
        goal_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertListEqual (markdown_to_blocks(text_to_blockify), goal_blocks)    


if __name__ == "__main__":
    unittest.main()
