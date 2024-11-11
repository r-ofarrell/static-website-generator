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
    lines = markdown_block.split("\n")
    if re.search(r"^#{1,6} \w", markdown_block):
        return "heading"
    if if len(lines) == 1 and re.search(r"^`{3}.*`{3}$", markdown_block):
        return "code"
    if len(lines) > 1 and re.search(r"^`{3}", lines[0]) and re.search(r"`{3}$", lines[-1]):
        return "code"
    if re.search(r"^>", markdown_block):
        for line in lines:
            if not re.search(r"^>", line):
                return "paragraph"
        return "quote"
    if re.search(r"^[-*] ", markdown_block):
        for line in lines:
            if not re.search(r"^[-*] ", line):
                return "paragraph"
        return "unordered_list"
    if re.search(r"^[0-9]+\. ", markdown_block):
        for line in lines:
            if not re.search(r"^[0-9]+\. ", line):
                return "paragraph"
        return "ordered_list"

    return "paragraph"
