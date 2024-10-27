from functools import *

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return reduce(lambda x, y: x + f' {y[0]}="{y[1]}"', self.props.items(), "")
    
    def __repr__(self):
        return f"HTMLNode: tag = {self.tag},\nvalue = {self.value},\n children = {self.children},\n props = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag, value, children = None, props = props)

    def to_html(self):
        if self.value is None:
            raise ValueError("A value is required in a leaf node")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, children, tag = None, props = None):
        super().__init__(tag, value = None, children = children, props = props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required for ParentNode")
        if self.children is None:
            raise ValueError("Parent node must have child node")
        child_html = reduce(lambda x, y: x + y.to_html(), self.children, "")
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"