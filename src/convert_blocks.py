#!/usr/bin/env python3

import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_block(markdown):
    """Returns the individual blocks in a markdown file."""
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
    """Iterates through a block of markdown and returns the type of markdown."""
    lines = markdown_block.split("\n")
    if re.search(r"^#{1,6} \w", markdown_block):
        return block_type_heading
    if len(lines) == 1 and re.search(r"^`{3}.*`{3}$", markdown_block):
        return block_type_code
    if (
        len(lines) > 1
        and re.search(r"^`{3}", lines[0])
        and re.search(r"`{3}$", lines[-1])
    ):
        return block_type_code
    if re.search(r"^>", markdown_block):
        for line in lines:
            if not re.search(r"^> ", line):
                return block_type_paragraph
        return "quote"
    if re.search(r"^\* ", markdown_block):
        for line in lines:
            if not re.search(r"^\* ", line):
                return block_type_paragraph
        return block_type_unordered_list
    if re.search(r"^- ", markdown_block):
        for line in lines:
            if not re.search(r"^- ", line):
                return block_type_paragraph
        return block_type_unordered_list
    if re.search(r"^[0-9]+\. ", markdown_block):
        num = 1
        for line in lines:
            if not line.startswith(f"{num}. "):
                return block_type_paragraph
            num += 1
        return block_type_ordered_list

    return block_type_paragraph
