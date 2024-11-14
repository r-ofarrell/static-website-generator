#!/usr/bin/env python3

import re
from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.textnode import text_node_to_html_node
from src.split_and_extract import text_to_textnodes
from src.convert_blocks import (
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
    children_nodes = []
    for block in blocks:
        children_nodes.append(block_to_html_node(block))

    div = ParentNode("div", children_nodes)
    return div

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(("p"), children)

def heading_to_html_node(block):
    if re.search(r"^#{7,}? ", block):
        raise ValueError(f"Invalid HTML: Invalid heading level")
    get_heading_level = re.search(r"^(#{1,6}) ", block)
    heading_level = len(get_heading_level.group(1))
    space_after_heading = 1
    text_with_heading_symbols_removed = block[heading_level + space_after_heading:]
    children = text_to_children(text_with_heading_symbols_removed)
    heading = f"h{heading_level}"
    return ParentNode(heading, children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid HTML: Code block not opened or closed")
    text_with_codeblock_symbols_removed = block[4:-3]
    lines = text_with_codeblock_symbols_removed.split("\n")
    lines = " ".join(lines).strip()
    children = text_to_children(lines)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid HTML: Missing quote markdown")
        new_lines.append(line.lstrip(">").strip())
    text_with_quote_ticks_removed = " ".join(new_lines)
    children = text_to_children(text_with_quote_ticks_removed)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        text_without_ul_markdown = item[2:]
        children = text_to_children(text_without_ul_markdown)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def ordered_list_to_html_node(block):
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        text_without_ol_markdown = re.sub(r"^[0-9]+\. ", "", item)
        children = text_to_children(text_without_ol_markdown)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
