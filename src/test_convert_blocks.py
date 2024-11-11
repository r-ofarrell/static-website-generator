#!/usr/bin/env python3

import unittest

from convert_blocks import markdown_to_block, block_to_block_type


class TestMarkdownToBlock(unittest.TestCase):
    def test_three_blocks_one_line_separating(self):
        page = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_block(page)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(blocks, expected)

    def test_three_blocks_multiple_lines_separating(self):
        page = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_block(page)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(blocks, expected)

    def test_three_blocks_with_training_whitespace(self):
        page = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item

        """
        blocks = markdown_to_block(page)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(blocks, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### I am a header"
        result = block_to_block_type(block)
        self.assertEqual("heading", result)

    def test_code(self):
        block = "````I am code````"
        result = block_to_block_type(block)
        self.assertEqual("code", result)

    def test_quote(self):
        block = "> I am a quote"
        result = block_to_block_type(block)
        self.assertEqual("quote", result)

    def test_unordered_list(self):
        block = "* I am a unordered list"
        result = block_to_block_type(block)
        self.assertEqual("unordered_list", result)

    def test_ordered_list(self):
        block = "10. I am an ordered list"
        result = block_to_block_type(block)
        self.assertEqual("ordered_list", result)

    def test_paragraph(self):
        block = "I am just a plain ol' paragraph"
        result = block_to_block_type(block)
        self.assertEqual("paragraph", result)
