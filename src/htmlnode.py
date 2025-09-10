class HTMLNode:
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("Subclasses must implement the 'to_html' method.")
    def props_to_html(self):
        temp = ""
        if not self.props:
            return ""
        for key, value in self.props.items():
            formated_string = f" {key}='{value}'"
            temp += formated_string
        return temp
    def __repr__(self):
        return f"Type is {self.tag} with value {self.value} and children {self.children}. Props={self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        else:
            if not self.props:
                self.props = ""
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        def render_childs(node_childrens):
            to_render = ""
            for child in node_childrens:
                to_render += child.to_html()
            return to_render
        if not self.tag:
            raise ValueError("Tag value is needed")
        if not self.children:
            raise ValueError("ParentNode must have a children")
        else:
            return f"<{self.tag}{super().props_to_html()}>{render_childs(self.children)}</{self.tag}>"

