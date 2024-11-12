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
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children_nodes = text_to_children(block, block_type)
        if block_type == block_type_heading:
            result = re.search(r"^(#{1,6})", block)
            heading_level = len(result.group())
            heading_tag = f"h{heading_level}"
            parent_node = ParentNode(heading_tag, children_nodes)
        elif block_type == block_type_code:
            code_node = ParentNode("code", children_nodes)
            parent_node = ParentNode("pre", [code_node])
        else:
            parent_node = ParentNode(block_type_dict[block_type], children_nodes)

        parent_nodes.append(parent_node)

    div = ParentNode("div", parent_nodes)
    return div

def remove_block_level_md(block, block_type):
    new_block = ""
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

    new_block = "\n".join(lines)
    return new_block

def text_to_children(text, block_type):
    html_nodes = []
    new_text = remove_block_level_md(text, block_type)
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

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
print(f"Here are the blocks: {blocks}")
for block in blocks:
    stripped_block = remove_block_level_md(block, block_to_block_type(block))
    print(stripped_block)
    children_nodes = text_to_children(stripped_block, block_to_block_type(block))
    print(f"Children: {children_nodes}")
