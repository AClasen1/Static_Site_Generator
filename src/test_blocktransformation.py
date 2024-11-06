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

class TestBlockToBlockType(unittest.TestCase):
    def test_one_of_each(self):
        text_to_blockify = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. One
2. Two
3. Three
4. Four
5. Five

```SELECT COUNT(*) 
FROM rpt.AnnualMemberStats
WHERE Year = 2024```

>>>Who are you quoting?"""

        text_blocks = markdown_to_blocks(text_to_blockify)
        block_types = list(map(block_to_block_type, text_blocks))
        self.assertListEqual(block_types, ["heading", "paragraph", "unordered_list", "ordered_list", "code", "quote"])

    def test_headers(self):
        text_to_blockify = """# This is a heading

## This is a heading        

### This is a heading

#### This is a heading        

##### This is a heading        

###### This is a heading

#This is not

####### And neither is this
"""

        text_blocks = markdown_to_blocks(text_to_blockify)
        block_types = list(map(block_to_block_type, text_blocks))
        self.assertListEqual(block_types, ["heading", "heading", "heading", "heading", "heading", "heading", "paragraph", "paragraph"])

    def test_lists_and_quotes(self):
        text_to_blockify = """- One line unordered list

1. One line ordered list

* Mixed bullet
- Unordered list
* Still works

1. This
2. Is
3. An
4. Ordered
5. List

0. But
1. This
2. Is
3. Not

- And
-This
- Is
- Not
-An
- Unordered
- List

-And neither is this

>This is a quote

>These are
>quotes

>But
This
>isn't"""

        text_blocks = markdown_to_blocks(text_to_blockify)
        block_types = list(map(block_to_block_type, text_blocks))
        self.assertListEqual(block_types, ["unordered_list", "ordered_list", "unordered_list", "ordered_list", "paragraph", "paragraph", "paragraph", "quote", "quote", "paragraph"])

if __name__ == "__main__":
    unittest.main()
