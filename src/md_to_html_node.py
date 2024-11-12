#!/usr/bin/env python3

import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from split_and_extract import text_to_textnodes
from convert_blocks import (
    markdown_to_block,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
    )

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    block_type_dict = {
        "code": "code",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "paragraph": "p"
    }
    children_nodes = []

    div = ParentNode("div", children_nodes)
    return div

def remove_block_level_md(block):
    new_block = ""
    block_type = block_to_block_type(block)
    lines = block.split("\n")
    if block_type == block_type_heading:
        new_block = re.sub(r"^#{1,6} ", "", block)
        return new_block
    elif block_type == block_type_code:
        for i in range(len(lines)):
            if i == 0:
                lines[i] = lines[i].rstrip("```")
            elif i == len(lines) - 1:
                lines[i] = lines[i].lstrip("```")
    elif block_type == block_type_quote:
        for i in range(len(lines)):
            lines[i] = lines[i].lstrip("> ")
    elif block_type == block_type_unordered_list:
        for i in range(len(lines)):
            lines[i] = re.sub(r"^[-|*] ", "", lines[i])
    elif block_type == block_type_ordered_list:
        for i in range(len(lines)):
            lines[i] = re.sub(r"^[0-9]+. ", "", lines[i])

    new_block = " ".join(lines)
    return new_block

def text_to_children(text):
    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes

# TODO create separate functions to process heading, paragraph,
# blockquotes, code, unordered lists, and ordered lists

def paragraph_to_html_node(block):
    paragraph = remove_block_level_md(block)
    children = text_to_children(paragraph)
    return ParentNode(("p"), children)

def heading_to_html_node(block):
    if re.search(r"^#{7,}? ", block):
        raise ValueError(f"Invalid heading level")
    heading_level = re.search(r"^(#{1,6}) ", block)
    text = remove_block_level_md(block)
    children = text_to_children(text)
    heading = f"h{len(heading_level.group(1))}"
    return ParentNode(heading, children)

def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = remove_block_level_md(block)
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


if __name__ == "__main__":
    block = """
# Here is the heading

Here is some paragraph.
With more paragraph.

> A quote looks **good** here

1. Point *one*
2. Point *two*
3. Point *three*

    """
blocks = markdown_to_block(block)
# print(f"Here are the blocks: {blocks}")
# for block in blocks:
#     stripped_block = remove_block_level_md(block, block_to_block_type(block))
#     print(stripped_block)
#     children_nodes = text_to_children(stripped_block)
#     print(f"Children: {children_nodes}")

stripped_block = remove_block_level_md(blocks[0])
print(stripped_block)
print(heading_to_html_node(blocks[0]))
