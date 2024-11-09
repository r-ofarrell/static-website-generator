#!/usr/bin/env python3

import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
from split_and_extract import split_nodes_delimiter, extract_markdown_images, extract_markdown_link, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.aohcc.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.aohcc.com")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_inequal_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_inequal_text(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_inequal_url(self):
        node = TextNode("This is a text", TextType.BOLD, "www.aohcc.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.aohcc.om")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TextType.TEXT, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_textype_conversion(self):
        node = TextNode("This is a text", TextType.BOLD, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_textype_bold(self):
        node = TextNode("This is bold", TextType.BOLD, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_textype_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": ""})

    def test_textype_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": node.url})

class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold text** alright", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" alright", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected_list)

    def test_code(self):
        node = TextNode("This is `code x = 100` alright", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code x = 100", TextType.CODE),
            TextNode(" alright", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected_list)

    def test_italic_and_bold(self):
        node = TextNode("This is *italic text* and **bolded stuff** alright", TextType.TEXT)
        # Bold must always be run first in order to properly split up nodes.
        # Doing italic first will strip a * from the bold text, messing up the
        # rest of the function.
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bolded stuff", TextType.BOLD),
            TextNode(" alright", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected_list)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        # Bold must always be run first in order to properly split up nodes.
        # Doing italic first will strip a * from the bold text, messing up the
        # rest of the function.
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

class TestExtracting(unittest.TestCase):
    def test_extract_image(self):
        image_markdown = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_image = extract_markdown_images(image_markdown)
        expected_results = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(extracted_image, expected_results)

    def test_extract_link(self):
        link_markdown = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_link = extract_markdown_link(link_markdown)
        expected_results = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    def text_no_image(self):
        markdown = "This text has some obi wan kenobi stuff with a link(https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(markdown)
        expected_results = []
        self.assertListEqual(result, expected_results)

    def text_no_link(self):
        markdown = "This is text with a link to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_link(markdown)
        expected_results = []
        self.assertListEqual(result, expected_results)

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is text with ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.IMAGE)
        split_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertListEqual(split_nodes, expected)

    def test_split_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.IMAGE)
        split_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertListEqual(split_nodes, expected)

    def test_split_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            )
        split_nodes = split_nodes_link([node])
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]




if __name__ == "__main__":
    unittest.main()
