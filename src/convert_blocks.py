#!/usr/bin/env python3

import re

def markdown_to_block(markdown):
    processed_markdown = markdown.strip().split("\n\n")
    blocks = []
    for line in processed_markdown:
        if line == "":
            continue
        else:
            line = line.strip()
            blocks.append(line)
    return blocks

def block_to_block_type(markdown_block):
    if re.search(r"^#{1,6} \w", markdown_block):
        return "heading"
    elif re.search(r"^`{3}.*`{3}$", markdown_block):
        return "code"
    elif re.search(r"^>", markdown_block):
        return "quote"
    elif re.search(r"^[-*] ", markdown_block):
        return "unordered_list"
    elif re.search(r"^[0-9]+\. ", markdown_block):
        return "ordered_list"
    else:
        return "paragraph"
