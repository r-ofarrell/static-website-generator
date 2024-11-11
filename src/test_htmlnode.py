import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq1(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
            {"href": "https://www.boot.dev"},
        )
        htmlnode2 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
            {"href": "https://www.boot.dev"},
        )
        self.assertEqual(htmlnode1, htmlnode2)

    def test_eq2(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
        )
        htmlnode2 = HTMLNode(
            "<h1></h1>",
            "I am a value",
        )
        self.assertEqual(htmlnode1, htmlnode2)

    def test_inequal1(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
            {"href": "https://www.boot.dev"},
        )
        htmlnode2 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children", "And more children"],
            {"href": "https://www.boot.dev"},
        )
        self.assertNotEqual(htmlnode1, htmlnode2)

    def test_inequal2(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
            {"href": "https://www.boot.dev"},
        )
        htmlnode2 = HTMLNode(
            "<h1>a</h1>",
            "I am a value",
            ["I have children", "And more children"],
            {"href": "https://www.boot.dev"},
        )
        self.assertNotEqual(htmlnode1, htmlnode2)

    def test_props_to_html(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
            {"href": "https://www.boot.dev", "target": "_blank"},
        )
        props_str = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(htmlnode1.props_to_html(), props_str)

    def test_repr(self):
        htmlnode1 = HTMLNode(
            "<h1></h1>",
            "I am a value",
            ["I have children"],
        )
        repr_expected = "HTMLNode(<h1></h1>, I am a value, ['I have children'], None)"
        self.assertEqual(repr(htmlnode1), repr_expected)

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_props(self):
        leaf = LeafNode("p", "LeafNode", {"class": "leaves"})
        expected_text = '<p class="leaves">LeafNode</p>'
        self.assertEqual(leaf.to_html(), expected_text)

    def test_to_html_without_props(self):
        leaf = LeafNode("p", "LeafNode")
        expected_text = '<p>LeafNode</p>'
        self.assertEqual(leaf.to_html(), expected_text)

    def test_to_html_without_tag(self):
        leaf = LeafNode("", "LeafNode")
        expected_text = "LeafNode"
        self.assertEqual(leaf.to_html(), expected_text)

    def test_to_html_raise_exception(self):
        leaf = LeafNode("", "")
        self.assertRaises(ValueError, leaf.to_html)

    def test_repr(self):
        leaf = LeafNode("p", "LeafNode", {"class": "leaves"})
        expected_text = "LeafNode(p, LeafNode, {'class': 'leaves'})"
        self.assertEqual(repr(leaf), expected_text)

class TestParentNode(unittest.TestCase):
    def test_to_html_without_tag(self):
        parent = ParentNode("", ["Test children"])
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_without_children(self):
        parent = ParentNode("p", [])
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_without_props(self):
        parent = ParentNode(
            "ul",
            [LeafNode("li", "LeafNode1"),
             LeafNode("li", "LeafNode2")
             ])
        expected_text = "<ul><li>LeafNode1</li><li>LeafNode2</li></ul>"
        self.assertEqual(parent.to_html(), expected_text)

    def test_to_html_parent_props(self):
        parent = ParentNode(
            "ul",
            [
                LeafNode("li", "LeafNode1"),
                LeafNode("li", "LeafNode2")
             ],
            {
                "class" : "leaves",
                "target": "_blank"
            }
        )
        expected_text = '<ul class="leaves" target="_blank"><li>LeafNode1</li><li>LeafNode2</li></ul>'
        self.assertEqual(parent.to_html(), expected_text)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_children_props(self):
        parent = ParentNode(
            "ul",
            [
                LeafNode("li", "LeafNode1", {"class": "leaves", "target": "_blank"}),
                LeafNode("li", "LeafNode2", {"class": "leaves", "target": "_blank"})
             ]
        )
        expected_text = '<ul><li class="leaves" target="_blank">LeafNode1</li><li class="leaves" target="_blank">LeafNode2</li></ul>'
        self.assertEqual(parent.to_html(), expected_text)

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("span", "Grandchild", {"class": "leaves", "target": "_blank"})
        parent = ParentNode(
            "ul",
            [
                ParentNode("li", [grandchild]),
                LeafNode("li", "LeafNode2", {"class": "leaves", "target": "_blank"})
             ]
        )
        expected_text = '<ul><li><span class="leaves" target="_blank">Grandchild</span></li><li class="leaves" target="_blank">LeafNode2</li></ul>'
        self.assertEqual(parent.to_html(), expected_text)

    def test_inequal_to_html_children_props(self):
         parent = ParentNode(
            "ul",
            [
                LeafNode("li", "LeafNode1", {"class": "leaves", "target": "_blank"}),
                LeafNode("li", "LeafNode2", {"class": "leaves"})
             ]
        )
         inequal_text = '<ul><li class="leaves" target="_blank">LeafNode1</li><li class="leaves" target="_blank">LeafNode2</li></ul>'
         self.assertNotEqual(parent.to_html(), inequal_text)

    def test_inequal_to_html_parent_props(self):
        parent = ParentNode(
            "ul",
            [
                LeafNode("li", "LeafNode"),
                LeafNode("li", "LeafNode2")
             ],
            {
                "class" : "leaves",
                "target": "_blank"
            }
        )
        inequal_text = '<ul class="leaves" target="_blank"><li>LeafNode1</li><li>LeafNode2</li></ul>'
        self.assertNotEqual(parent.to_html(), inequal_text)

    def test_to_html_heading(self):
        child_nodes = [
            LeafNode(None, "Here is the heading"),
            LeafNode("b", "with some bolded text"),
            LeafNode("i", "and some italic text as well")
        ]
        node = ParentNode("h1", child_nodes)
        expected = "<h1>Here is the heading<b>with some bolded text</b><i>and some italic text as well</i></h1>"
        self.assertEqual(node.to_html(), expected)
