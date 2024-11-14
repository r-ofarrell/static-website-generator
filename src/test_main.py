#!/usr/bin/env python3

import unittest
import re
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_exract_title(self):
        markdown = """# The heading is here

        Here is some more text. Followed by more.
        And another one."""
        expected = "The heading is here"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_exception(self):
        markdown = """## The heading is here

        Here is some more text. Followed by more.
        And another one."""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
