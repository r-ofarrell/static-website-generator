#!/usr/bin/env python3

import unittest
from md_to_html_node import (
    markdown_to_html_node,
    markdown_to_block,
)
from src.htmlnode import HTMLNode, ParentNode, LeafNode

class TestParagraphToHTMLNode(unittest.TestCase):
    def markdown_to_block(self):
        markdown = """
        ## This is a heading

        With a paragraph
        on two lines

        ```Some code```

        > A quote
        > Another quote

        * One
        * Two


        1. Point1
        2. Point2
        """

        blocks = [
            "## This is a heading",
            "With a paragraph\non two lines",
            "```Some code```",
            "> A quote\n> Another quote",
            "* One\n* Two",
            "1. Point1\n2. Point2"
        ]

        self.assertListEqual(markdown_to_block(markdown), blocks)

    def test_markdown_to_html_node_heading_and_paragraph(self):
        markdown = """
## This is a heading

With a **bolded** paragraph
on two lines
        """
        expected = "<div><h2>This is a heading</h2><p>With a <b>bolded</b> paragraph on two lines</p></div>"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_markdown_to_html_node_lists(self):
        markdown = """
* One
* Two
* Three

1. Point1
2. Point2"""
        expected = "<div><ul><li>One</li><li>Two</li><li>Three</li></ul><ol><li>Point1</li><li>Point2</li></ol></div>"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, expected)

    def test_markdown_to_html_code_and_quote(self):
        markdown = """
```
x = 'I am a code block'
y = 'On a new line'
```

> I am quoted as saying
> This should work"""
        expected = "<div><pre><code>x = 'I am a code block' y = 'On a new line'</code></pre><blockquote>I am quoted as saying This should work</blockquote></div>"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_block_and_inline_markdown(self):
        markdown = """
# Heading1

Here is a paragraph with some `code` in it
And a **bolded** item as well as something in *italics*

## Heading2"""
        expected = "<div><h1>Heading1</h1><p>Here is a paragraph with some <code>code</code> in it And a <b>bolded</b> item as well as something in <i>italics</i></p><h2>Heading2</h2></div>"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, expected)
