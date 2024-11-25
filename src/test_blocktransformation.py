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

class TestStringHelperFunctions(unittest.TestCase):
    def test_header_tags(self):
        headers = """# This is a heading
## This is a heading
### This is a heading
#### This is a heading        
##### This is a heading        
###### This is a heading"""

        self.assertListEqual(list(map(get_header_tag, headers.split("\n"))), ["h1","h2","h3","h4","h5","h6"])

    def test_extract_title(self):
        markdown = """# This is a heading

## This is a heading
### This is a heading
#### This is a heading        
##### This is a heading        
###### This is a heading"""

        self.assertEqual("This is a heading", extract_title(markdown))

    def test_deprefixing(self):
        strings_to_deprefix = ["1. This is an ordered list item", "* This is an unordered list item", "### This is a header"]
        self.assertListEqual(list(map(deprefix_string, strings_to_deprefix)), ["This is an ordered list item", "This is an unordered list item", "This is a header"])

class TestMarkdownBlockToHtmlNode(unittest.TestCase):
    def test_all_types(self):
        markdown_to_nodify ="""# This is a heading

### This is also a heading

>This is a quote

>And
>This
>Is
>A
>Multi-line
>Quote

```This is a block of code:
SELECT COUNT(1)
FROM MyTable
WHERE EventDate >= '1/1/2024'
```

- This
* is
- an
* unordered
- list

1. This
2. is 
3. an
4. ordered
5. list

And this is just
a humble paragraph"""

        markdown_as_html_node = markdown_to_html_node(markdown_to_nodify)
        target_html = """<div><h1>This is a heading</h1><h3>This is also a heading</h3><blockquote>This is a quote</blockquote><blockquote>And This Is A Multi-line Quote</blockquote><pre><code>This is a block of code:
SELECT COUNT(1)
FROM MyTable
WHERE EventDate >= '1/1/2024'
</code></pre><ul><li>This</li><li>is</li><li>an</li><li>unordered</li><li>list</li></ul><ol><li>This</li><li>is </li><li>an</li><li>ordered</li><li>list</li></ol><p>And this is just a humble paragraph</p></div>"""
        self.assertEqual(markdown_as_html_node.to_html(), target_html)

    def test_empty_doc(self):
        markdown_as_html_node = markdown_to_html_node("")
        target_html = "<div></div>"
        self.assertEqual(markdown_as_html_node.to_html(), target_html)

if __name__ == "__main__":
    unittest.main()
