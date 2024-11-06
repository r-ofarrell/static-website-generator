class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes = ""
        if self.props:
            for k, v in self.props.items():
                attributes += f' {k}="{v}"'

        return attributes

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value assigned to LeafNode value property")

        elif not self.tag:
            return self.value

        elif self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("HTML Error: No html tag")

        if not self.children:
            raise ValueError("HTML Error: No children nodes")

        children_nodes = [child.to_html() for child in self.children]

        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{''.join(children_nodes)}</{self.tag}>"

        return f"<{self.tag}>{''.join(children_nodes)}</{self.tag}>"
